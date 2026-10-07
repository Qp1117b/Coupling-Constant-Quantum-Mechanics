extends RefCounted
class_name MeasurementTool

# 测量工具：距离、角度、二面角
# 选中2个原子→距离，3个→角度，4个→二面角

static func measure_distance(a_pos: Vector3, b_pos: Vector3) -> Dictionary:
	var dist = a_pos.distance_to(b_pos)
	return {
		"type": "distance",
		"value": dist,
		"unit": "Å",
		"label": "距离 = %.4f Å" % dist
	}

static func measure_angle(a_pos: Vector3, b_pos: Vector3, c_pos: Vector3) -> Dictionary:
	var v1 = a_pos - b_pos
	var v2 = c_pos - b_pos
	var angle_deg = rad_to_deg(v1.angle_to(v2))
	return {
		"type": "angle",
		"value": angle_deg,
		"unit": "°",
		"label": "角度 = %.2f°" % angle_deg
	}

static func measure_dihedral(a_pos: Vector3, b_pos: Vector3, c_pos: Vector3, d_pos: Vector3) -> Dictionary:
	var b1 = b_pos - a_pos
	var b2 = c_pos - b_pos
	var b3 = d_pos - c_pos
	var n1 = b1.cross(b2)
	var n2 = b2.cross(b3)
	var m1 = n1.cross(b2.normalized())
	var x = n1.dot(n2)
	var y = m1.dot(n2)
	var angle_deg = rad_to_deg(atan2(y, x))
	return {
		"type": "dihedral",
		"value": angle_deg,
		"unit": "°",
		"label": "二面角 = %.2f°" % angle_deg
	}

static func measure(atoms: Array) -> Dictionary:
	match atoms.size():
		2:
			return measure_distance(atoms[0], atoms[1])
		3:
			return measure_angle(atoms[0], atoms[1], atoms[2])
		4:
			return measure_dihedral(atoms[0], atoms[1], atoms[2], atoms[3])
		_:
			return {"type": "none", "label": "选中2-4个原子测量"}

static func compute_bond_order(distance: float, ideal_distance: float) -> float:
	if ideal_distance <= 0:
		return 1.0
	var ratio = distance / ideal_distance
	if ratio < 0.85:
		return 3.0
	elif ratio < 0.95:
		return 2.0
	else:
		return 1.0

static func center_of_mass(positions: Array) -> Vector3:
	if positions.is_empty():
		return Vector3.ZERO
	var sum = Vector3.ZERO
	for p in positions:
		sum += p
	return sum / positions.size()

static func bounding_box(positions: Array) -> Dictionary:
	if positions.is_empty():
		return {"min": Vector3.ZERO, "max": Vector3.ZERO, "size": Vector3.ZERO, "center": Vector3.ZERO}
	var mn = positions[0]
	var mx = positions[0]
	for p in positions:
		mn = mn.min(p)
		mx = mx.max(p)
	return {
		"min": mn,
		"max": mx,
		"size": mx - mn,
		"center": (mx + mn) * 0.5
	}

static func principal_moments(positions: Array) -> Dictionary:
	if positions.size() < 2:
		return {"eigenvalues": [0, 0, 0], "eigenvectors": [Vector3.RIGHT, Vector3.UP, Vector3.BACK]}
	var com = center_of_mass(positions)
	var ixx = 0.0; var iyy = 0.0; var izz = 0.0
	var ixy = 0.0; var ixz = 0.0; var iyz = 0.0
	for p in positions:
		var d = p - com
		ixx += d.y * d.y + d.z * d.z
		iyy += d.x * d.x + d.z * d.z
		izz += d.x * d.x + d.y * d.y
		ixy -= d.x * d.y
		ixz -= d.x * d.z
		iyz -= d.y * d.z
	var n = positions.size()
	ixx /= n; iyy /= n; izz /= n; ixy /= n; ixz /= n; iyz /= n
	return {
		"ixx": ixx, "iyy": iyy, "izz": izz,
		"ixy": ixy, "ixz": ixz, "iyz": iyz,
		"center": com
	}