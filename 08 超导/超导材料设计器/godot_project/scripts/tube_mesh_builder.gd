extends RefCounted
class_name TubeMeshBuilder

# 3D管道网格生成器
# 将3D点序列转换为带粗细的实体管道几何
# 支持变半径、平滑连接、球关节

# 从点序列生成管道段变换列表（用于MultiMesh渲染）

static func generate_tube_segments(points: Array, radius: float, closed: bool = false) -> Array:
	var segments: Array = []
	if points.size() < 2:
		return segments
	var n = points.size()
	var end = n if closed else n - 1
	for i in range(end):
		var a = points[i]
		var b = points[(i + 1) % n]
		var mid = (a + b) / 2.0
		var diff = b - a
		var length = diff.length()
		if length < 0.001:
			continue
		var dir = diff / length
		var basis = _basis_y_along(dir)
		var t = Transform3D(basis, mid)
		segments.append({
			"transform": t,
			"length": length,
			"radius": radius,
			"start": a,
			"end": b
		})
	return segments

# 从点序列生成完整管道Mesh（用于单Mesh渲染）

static func build_tube_mesh(points: Array, radius: float, segments_per_ring: int = 12, closed: bool = false) -> Mesh:
	if points.size() < 2:
		return null
	var st = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var n = points.size()
	var ring_count = n if closed else n
	for i in range(ring_count):
		var p = points[i]
		var tangent = _compute_tangent(points, i, closed)
		var normal = _compute_normal(tangent)
		var binormal = tangent.cross(normal).normalized()
		for j in range(segments_per_ring):
			var angle = float(j) / segments_per_ring * TAU
			var offset = (normal * cos(angle) + binormal * sin(angle)) * radius
			st.add_vertex(p + offset)
	for i in range(ring_count - (0 if closed else 1)):
		var i_next = (i + 1) % ring_count
		for j in range(segments_per_ring):
			var j_next = (j + 1) % segments_per_ring
			var v0 = i * segments_per_ring + j
			var v1 = i * segments_per_ring + j_next
			var v2 = i_next * segments_per_ring + j_next
			var v3 = i_next * segments_per_ring + j
			st.add_index(v0)
			st.add_index(v1)
			st.add_index(v2)
			st.add_index(v0)
			st.add_index(v2)
			st.add_index(v3)
	if closed:
		var i = ring_count - 1
		var i_next = 0
		for j in range(segments_per_ring):
			var j_next = (j + 1) % segments_per_ring
			var v0 = i * segments_per_ring + j
			var v1 = i * segments_per_ring + j_next
			var v2 = i_next * segments_per_ring + j_next
			var v3 = i_next * segments_per_ring + j
			st.add_index(v0)
			st.add_index(v1)
			st.add_index(v2)
			st.add_index(v0)
			st.add_index(v2)
			st.add_index(v3)
	st.generate_normals()
	return st.commit()

# 生成球关节变换列表（用于管道连接处平滑）

static func generate_joints(points: Array, radius: float, closed: bool = false) -> Array:
	var joints: Array = []
	var n = points.size()
	var start_idx = 0 if closed else 1
	var end_idx = n if closed else n - 1
	for i in range(start_idx, end_idx):
		joints.append({
			"position": points[i],
			"radius": radius
		})
	if not closed and n > 0:
		joints.append({"position": points[0], "radius": radius})
		joints.append({"position": points[n - 1], "radius": radius})
	return joints

# 生成变半径管道段（半径随弧长变化）

static func generate_variable_radius_tube(points: Array, base_radius: float,
										 radius_variation: float = 0.0, closed: bool = false) -> Array:
	var segments: Array = []
	if points.size() < 2:
		return segments
	var n = points.size()
	var total_len = 0.0
	for i in range(n - 1):
		total_len += points[i].distance_to(points[i + 1])
	if total_len < 0.001:
		return segments
	var accum_len = 0.0
	var end = n if closed else n - 1
	for i in range(end):
		var a = points[i]
		var b = points[(i + 1) % n]
		var mid = (a + b) / 2.0
		var diff = b - a
		var length = diff.length()
		if length < 0.001:
			continue
		var dir = diff / length
		var basis = _basis_y_along(dir)
		var t = Transform3D(basis, mid)
		var s = accum_len / total_len
		var radius = base_radius * (1.0 + radius_variation * sin(s * TAU))
		segments.append({
			"transform": t,
			"length": length,
			"radius": max(0.01, radius),
			"start": a,
			"end": b
		})
		accum_len += length
	return segments

# 生成MultiMesh渲染数据

static func build_multimesh_data(strokes: Array, base_radius: float) -> Dictionary:
	var all_segments: Array = []
	var all_joints: Array = []
	var colors: Array = []
	for stroke in strokes:
		var pts = stroke.get("points", [])
		if pts.size() < 2:
			continue
		var radius = stroke.get("radius", base_radius)
		var closed = stroke.get("closed", false)
		var segments = generate_tube_segments(pts, radius, closed)
		var joints = generate_joints(pts, radius, closed)
		var color = stroke.get("color", Color(0.3, 0.85, 0.4))
		for s in segments:
			all_segments.append(s)
			colors.append(color)
		for j in joints:
			all_joints.append(j)
			colors.append(color)
	return {
		"segments": all_segments,
		"joints": all_joints,
		"colors": colors,
		"segment_count": all_segments.size(),
		"joint_count": all_joints.size()
	}

# 辅助函数

static func _basis_y_along(dir: Vector3) -> Basis:
	var y = dir.normalized()
	var x: Vector3
	if abs(y.x) < 0.9:
		x = y.cross(Vector3(1, 0, 0)).normalized()
	else:
		x = y.cross(Vector3(0, 1, 0)).normalized()
	var z = x.cross(y).normalized()
	return Basis(x, y, z)

static func _compute_tangent(points: Array, i: int, closed: bool) -> Vector3:
	var n = points.size()
	if n < 2:
		return Vector3(0, 1, 0)
	var prev_idx = i - 1 if i > 0 else (n - 1 if closed else 0)
	var next_idx = i + 1 if i < n - 1 else (0 if closed else n - 1)
	var tangent = (points[next_idx] - points[prev_idx]).normalized()
	if tangent.length() < 0.001:
		return Vector3(0, 1, 0)
	return tangent

static func _compute_normal(tangent: Vector3) -> Vector3:
	var n: Vector3
	if abs(tangent.x) < 0.9:
		n = tangent.cross(Vector3(1, 0, 0)).normalized()
	else:
		n = tangent.cross(Vector3(0, 1, 0)).normalized()
	return n

# 计算管道体积（用于物理分析）

static func compute_tube_volume(points: Array, radius: float, closed: bool = false) -> float:
	var volume = 0.0
	var cross_section = PI * radius * radius
	var n = points.size()
	var end = n if closed else n - 1
	for i in range(end):
		var a = points[i]
		var b = points[(i + 1) % n]
		volume += a.distance_to(b) * cross_section
	var joint_volume = float(points.size()) * (4.0 / 3.0) * PI * radius * radius * radius
	volume += joint_volume
	return volume

# 计算管道表面积

static func compute_tube_surface_area(points: Array, radius: float, closed: bool = false) -> float:
	var area = 0.0
	var circumference = TAU * radius
	var n = points.size()
	var end = n if closed else n - 1
	for i in range(end):
		var a = points[i]
		var b = points[(i + 1) % n]
		area += a.distance_to(b) * circumference
	var joint_area = float(points.size()) * 4.0 * PI * radius * radius
	area += joint_area
	return area