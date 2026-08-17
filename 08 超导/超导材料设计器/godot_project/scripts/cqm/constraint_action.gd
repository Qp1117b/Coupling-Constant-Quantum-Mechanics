extends RefCounted
class_name CQMConstraintAction

# CQM 约束作用量 S_constraint — §3.1
# A4-Regge几何骨架 + 压强-距离结构
# S = Σ_T Σ_h tr(Θ_h[Γ_T] ∘ M_h[R]) + Σ_<TT'> tr(P(d_TT') ∘ Γ_TT')
#
# Θ_h[Γ_T]    : 绕hinge h的矩阵和乐(holonomy), A4嘉当矩阵路径排序乘积
# M_h[R]      : 关系网络R在面h上的关联模式矩阵
# P(d_TT')    : 压强-距离张量, d_TT' = |ln(r_T/r_T')|
# Γ_TT'       : 超级嘉当矩阵T-T'块连接子矩阵 (块间耦合 = -β·I₄, molecular_cartan.gd)
#
# 严格化实现 (对应 G16/G17 桥接):
#   Θ_h = |∏_{环路跃迁} w_i · tr(P4^N)| / 4, P4 = A4/(2+√2) 谱半径归一化
#         环路跃迁权重取环绕四面体对面顶点间的关系网络关联 R_{c_i d_i}
#         P4 本征值 {3-2√2, 2-√2, 2-√2, 1} ⊂ (0,1], 幂次有界, 和乐良定义
#   M_h[R] = ½·(R_ab + R̄_环路): hinge 面直接关联与环绕间接关联的模式混合
#   S_holonomy = Σ_h ε_h · Θ_h · M_h — Regge 亏角与嘉当矩阵和乐的耦合
#
# 压强真实作用：压缩晶格间距和精细引力结构，不压缩电磁场

const SPECTRAL_RADIUS_A4 = 3.414213562373095  # 2+√2, A4 嘉当矩阵谱半径

static func compute(tetrahedra: Array, relation_network: Array,
					pressure: float = 0.0) -> Dictionary:
	var s_holonomy = _compute_holonomy_term(tetrahedra, relation_network)
	var s_pressure = _compute_pressure_term(tetrahedra, pressure)
	var s_total = s_holonomy + s_pressure
	return {
		"S_constraint": s_total,
		"S_holonomy": s_holonomy,
		"S_pressure": s_pressure,
		"tetrahedra_count": tetrahedra.size(),
	}

## 和乐项: 按全局唯一 hinge 去重计算 (同一 hinge 属于多个四面体, 仅计一次)
static func _compute_holonomy_term(tetrahedra: Array, relation_network: Array) -> float:
	if tetrahedra.is_empty():
		return 0.0
	var seen: Dictionary = {}
	var total := 0.0
	var hinges: Array = []
	for tet in tetrahedra:
		for h in tet.get("hinges", []):
			var key = str(h.get("key", ""))
			if not seen.has(key):
				seen[key] = true
				hinges.append(h)
	for h in hinges:
		var eps = float(h.get("deficit_angle", 0.0))
		if absf(eps) < 1e-9:
			continue
		var holonomy = matrix_holonomy(h, relation_network)
		var mode = association_mode(h, relation_network)
		total += eps * holonomy * mode
	return total

## Θ_h[Γ_T]: 绕 hinge 的矩阵和乐
## 环路 = 环绕四面体序列的对面对顶点链, 每个四面体贡献一段跃迁,
## 跃迁矩阵 = w_i·P4 (w_i 为对面顶点对的关系网络关联, P4 为谱半径归一化 A4 块)
## 块对角近似下路径乘积 = (∏ w_i)·P4^N, 和乐取归一化迹
static func matrix_holonomy(hinge: Dictionary, relation_network: Array) -> float:
	var n = int(hinge.get("tet_count", 0))
	if n <= 0:
		return 0.0
	var weight_prod := 1.0
	var opposite: Array = hinge.get("opposite_verts", [])
	for pair in opposite:
		if pair.size() < 2:
			continue
		var c = int(pair[0]); var d = int(pair[1])
		weight_prod *= _relation(relation_network, c, d)
	# 几何平均防指数爆炸/消失: (∏w)^{1/N}·|tr(P4^N)|^{1/N} 的有界代理
	# |w_prod| ≤ 1 (关系网络 ∈ [0,1]), tr(P4^N)/4 ∈ [¼·(3-2√2)^N…1] 有界
	return pow(absf(weight_prod), 1.0 / float(n)) * _a4_trace_norm(n)

## tr(P4^N)/4, P4 = A4/(2+√2), 本征值 {3-2√2, 2-√2, 2-√2, 1}
static func _a4_trace_norm(n: int) -> float:
	var lam_min = 3.0 - 2.0 * sqrt(2.0)   # (2-√2)/(2+√2)
	var lam_mid = 2.0 - sqrt(2.0)         # 2/(2+√2), 二重
	var t = pow(lam_min, float(n)) + 2.0 * pow(lam_mid, float(n)) + 1.0
	return t / 4.0

## M_h[R]: 关系网络在 hinge 面 (a,b) 上的关联模式
## = ½·(hinge 直接关联 R_ab + 环绕四面体对面关联均值)
static func association_mode(hinge: Dictionary, relation_network: Array) -> float:
	var e: Array = hinge.get("edge", [])
	if e.size() < 2:
		return 0.0
	var direct = _relation(relation_network, int(e[0]), int(e[1]))
	var opposite: Array = hinge.get("opposite_verts", [])
	if opposite.is_empty():
		return direct
	var loop_sum := 0.0
	for pair in opposite:
		if pair.size() < 2:
			continue
		loop_sum += _relation(relation_network, int(pair[0]), int(pair[1]))
	return 0.5 * (direct + loop_sum / opposite.size())

static func _relation(relation_network: Array, i: int, j: int) -> float:
	if i < 0 or j < 0 or i >= relation_network.size() or j >= relation_network.size():
		return 0.0
	return float(relation_network[i][j])

static func _compute_pressure_term(tetrahedra: Array, pressure: float) -> float:
	if pressure <= 0 or tetrahedra.is_empty():
		return 0.0
	var total := 0.0
	for i in range(tetrahedra.size()):
		for j in range(i + 1, tetrahedra.size()):
			var r_i = _tet_radius(tetrahedra[i])
			var r_j = _tet_radius(tetrahedra[j])
			if r_i > 0 and r_j > 0:
				var d = abs(log(r_i / r_j))
				total += pressure * d
	return total

static func _tet_radius(tet: Dictionary) -> float:
	return float(tet.get("circumradius", 1.0))

static func compute_stiffness_matrix(_tetrahedra: Array, relation_network: Array) -> Array:
	var n = min(relation_network.size(), 4)
	if n == 0:
		return []
	var matrix: Array = []
	for i in range(n):
		var row: Array = []
		for j in range(n):
			if i == j:
				row.append(1.0 + 0.1 * float(i))
			else:
				row.append(0.01 / (1.0 + abs(i - j)))
		matrix.append(row)
	return matrix

static func bcs_degradation() -> Dictionary:
	return {"S_constraint": 0.0, "S_holonomy": 0.0, "S_pressure": 0.0}
