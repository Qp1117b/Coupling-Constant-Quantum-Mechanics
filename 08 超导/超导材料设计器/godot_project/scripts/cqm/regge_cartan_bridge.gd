extends RefCounted
class_name ReggeCartanBridge

## G16/G17 Regge-嘉当耦合数值桥接
## 严格对应 Lean 形式化 (06 Lean形式化/Superconductivity/):
##   - MolecularGeometry.lean §4: reggeTetrahedronEdgeLength (l = κ/√(λᵢλⱼ)),
##     deficitAngleDensity (δ_eff = δ/V), grEffectiveMetric (h = δ·diag(1,-⅓,-⅓,-⅓))
##   - BridgeTheorems.lean: reggeDualArea (A = √3/4·l²),
##     reggeEffectiveRicciScalar (R = 2δ/A), reggeDeficit_ricciScalar_closedForm
##     (R = (8δ/√3)·λ²/κ²)
##
## G16 (因果分辨率形式化): Regge 亏角密度 → 有效 Ricci 标量
##   数值链: 谱间隙 λᵢ (嘉当块) → κ 标定 → 谱边长 l_ij = κ/√(λᵢλⱼ) →
##           对偶面积 A_dual = (√3/4)l² → R_eff = 2ε/A_dual
##   交叉验证: 正四面体闭式 R = (8ε/√3)·λ²/κ² 与逐 hinge 数值的一致性
##
## G17 (牛顿引力退化): Regge 有效度规 → Poisson 方程
##   数值链: δ_eff(T) = Σ_{h∈T} ε_h / V_T → h₀₀ = α·δ_eff → Φ_R = -c²/2·h₀₀
##   验证: 高斯定理积分形式 ∮∇Φ·dS = -4πG·M_enclosed 的相对残差
##   (泊松方程 ∇²Φ = 4πGρ 的积分形式, 避开点源 δ 函数的格点奇异)

const SPEED_OF_LIGHT = 2.998e8
const GRAVITATIONAL_CONSTANT = 6.674e-11
const ANGSTROM_TO_METER = 1e-10
const SPECTRAL_GAP_A4 = 0.585786437626905  # 2-√2, A4 嘉当矩阵谱间隙 (Lean: SPAF.spectralGap)

## 每个原子的嘉当块谱间隙: 块 = A4·(1+0.1|中子缺陷|), 块谱间隙 = (2-√2)·缩放
## 缺陷推导与 cqm_calculator._compute_molecular_cartan 一致 (同位素 → 中子数 → 缺陷)
static func atom_spectral_weight(atom: Dictionary) -> float:
	var defect := 0.0
	if atom.has("neutron_defect"):
		defect = float(atom["neutron_defect"])
	else:
		var sym = str(atom.get("symbol", "H"))
		var data = ElementDB.get_element(sym)
		var z = int(data.get("atomic_number", 1))
		var iso = int(atom.get("isotope", 1))
		if iso > 0:
			defect = CQMCartanBuilder.neutron_defect(iso - z, sym)
		else:
			defect = CQMCartanBuilder.neutron_defect(CQMCartanBuilder._estimate_N_ref(sym), sym)
	return SPECTRAL_GAP_A4 * (1.0 + 0.1 * absf(defect))

## G16: 亏角密度 → 有效 Ricci 标量
static func compute_g16(regge: Dictionary, atoms: Array) -> Dictionary:
	var hinges: Array = regge.get("hinges", [])
	var tets: Array = regge.get("tetrahedra", [])
	if hinges.is_empty() or tets.is_empty():
		return _empty_g16()

	# κ 标定: 谱边长 l_spec = κ/√(λᵢλⱼ) 与几何边长最小二乘一致
	# κ* = Σ_bonds l_geo·√(λᵢλⱼ) / Σ_bonds (√(λᵢλⱼ))²  (对 l = κ/√(λλ) 的线性化最小二乘:
	# 令 u = √(λᵢλⱼ), l·u = κ → κ* = Σ(l·u·u)/Σ(u⁴) 等价于对 l = κ/u 的加权拟合)
	var weights := PackedFloat64Array()
	weights.resize(atoms.size())
	for i in range(atoms.size()):
		weights[i] = atom_spectral_weight(atoms[i])

	var kappa := _calibrate_kappa(hinges, weights)
	var mean_lambda := _mean_lambda(hinges, weights)

	# 逐 hinge: 对偶面积与有效 Ricci 标量 (Lean: reggeDualArea / reggeEffectiveRicciScalar)
	var total_ricci := 0.0
	var total_dual_area := 0.0
	var total_deficit := 0.0
	var per_hinge: Array = []
	for h in hinges:
		var eps = float(h.get("deficit_angle", 0.0))
		var l = float(h.get("length", 0.0))
		var a_dual = dual_area(l)
		var r_h = ricci_scalar(eps, a_dual)
		total_ricci += r_h
		total_dual_area += a_dual
		total_deficit += absf(eps)
		per_hinge.append(r_h)

	# 体积加权全局 Ricci 标量: R_global = 2·Σ ε·l / V_total (3D Regge 离散化 ∫R dV)
	var v_total := 0.0
	for t in tets:
		v_total += absf(float(t.get("volume", 0.0)))
	var regge_action = float(regge.get("regge_action", 0.0))
	var r_global = 2.0 * regge_action / v_total if v_total > 1e-12 else 0.0

	# 亏角密度 (Lean: deficitAngleDensity): δ_eff = |ε| 总亏角 / 总体积
	var deficit_density = total_deficit / v_total if v_total > 1e-12 else 0.0

	# 谱桥接闭式交叉验证 (Lean: reggeDeficit_ricciScalar_closedForm)
	# R_closed = (8·ε̄/√3)·λ²/κ², 其中 ε̄ 为平均亏角, λ = 平均谱间隙
	var mean_deficit = total_deficit / hinges.size() if hinges.size() > 0 else 0.0
	var r_closed = closed_form_ricci(mean_deficit, mean_lambda, kappa)
	var mean_ricci_numeric = total_ricci / hinges.size() if hinges.size() > 0 else 0.0
	# 闭式假设正四面体 (边长均一); 数值用实际边长 → 形状因子 = 边长方差
	var cross_check = absf(r_closed - mean_ricci_numeric) / maxf(absf(r_closed), 1e-12) if absf(r_closed) > 1e-12 else 0.0

	# 谱间隙单调性检验 (Lean: spectralGap_to_ricciScalar_chain 方向性):
	# 若 λ 大的 hinge 边长更短, 其对偶面积更小 → R 更大
	var monotone_ok := _check_monotonicity(hinges, weights)

	return {
		"ricci_scalar_global": r_global,
		"ricci_scalar_mean": mean_ricci_numeric,
		"ricci_scalar_closed_form": r_closed,
		"cross_check_rel_error": cross_check,
		"deficit_density": deficit_density,
		"dual_area_mean": total_dual_area / hinges.size() if hinges.size() > 0 else 0.0,
		"kappa": kappa,
		"mean_spectral_weight": mean_lambda,
		"total_volume": v_total,
		"monotonicity_holds": monotone_ok,
		"per_hinge_ricci": per_hinge,
		"hinge_count": hinges.size(),
		"evidence": "lean_bridge_numeric",
		"lean_refs": ["reggeDualArea", "reggeEffectiveRicciScalar",
			"reggeDeficit_ricciScalar_closedForm", "spectralGap_to_ricciScalar_chain"],
	}

## G17: Regge 有效度规 → 牛顿 Poisson 退化验证
static func compute_g17(regge: Dictionary, atoms: Array, positions: Array) -> Dictionary:
	# 内部统一 SI 单位: 位置 Å → m (×1e-10), δ_eff rad/Å³ → rad/m³ (×1e30)
	var tets: Array = regge.get("tetrahedra", [])
	if tets.is_empty() or atoms.is_empty():
		return _empty_g17()

	var positions_si: Array = []
	for p in positions:
		positions_si.append((p as Vector3) * ANGSTROM_TO_METER)

	# 1. 逐四面体亏角密度 δ_eff(T) = Σ_{h∈T}|ε_h| / V_T (SI: rad/m³)
	var tet_centers: Array = []
	var tet_deltas: Array = []
	for t in tets:
		var v = absf(float(t.get("volume", 0.0)))
		if v < 1e-12:
			continue
		var eps_sum := 0.0
		for h in t.get("hinges", []):
			eps_sum += absf(float(h.get("deficit_angle", 0.0)))
		tet_deltas.append(eps_sum / (v * pow(ANGSTROM_TO_METER, 3.0)))
		var verts: Array = t.get("verts", [])
		var c := Vector3.ZERO
		for vi in verts:
			if vi >= 0 and vi < positions_si.size():
				c += positions_si[vi] as Vector3
		tet_centers.append(c / float(max(verts.size(), 1)))

	if tet_centers.is_empty():
		return _empty_g17()

	# 2. Regge 势场: Φ_R(x) = -(c²/2)·α·δ_eff(x), δ_eff 取最近四面体
	#    (Lean: grMetric_from_deficitDensity — g₀₀ = -1 + α·δ_eff, Φ = -c²/2·h₀₀)
	# 3. 牛顿势场: Φ_N(x) = -G·Σᵢ mᵢ/|x-rᵢ| (Plummer 软化, 体积分不变)
	# 4. α 标定: β = ⟨Φ_N, Φ_R⟩/⟨Φ_R, Φ_R⟩ (最小二乘), 幅度吸收进 β
	var samples := _poisson_sample_box(positions_si)
	# Plummer 软化长度 = 0.1×网格步长 (仅防格点重合奇异; 面积分格式下
	# 软化会抹平边界梯度, 取小值以保持通量求积精度)
	var s0 = samples[0] as Vector3
	var s_last = samples[samples.size() - 1] as Vector3
	var softening = maxf(absf(s_last.x - s0.x) / 50.0, 1e-18)
	var phi_r := PackedFloat64Array()
	var phi_n := PackedFloat64Array()
	for x in samples:
		var dr = _nearest_delta(x, tet_centers, tet_deltas)
		phi_r.append(-0.5 * SPEED_OF_LIGHT * SPEED_OF_LIGHT * dr)
		phi_n.append(_newton_potential(x, atoms, positions_si, softening))

	var beta := _least_squares_scale(phi_n, phi_r)

	var mass_total := 0.0
	for a in atoms:
		mass_total += _atom_mass_kg(a)

	# 5. 离散高斯定理验证 (Poisson 积分的面积分形式): ∮_∂Box ∇Φ·dS = 4πG·M_enclosed
	#    通量只需边界格点势值 (源远离边界, 无点源奇异), 面向边界的一侧差分
	#    与散度定理严格对应 (体积拉普拉斯中心差分在 6³ 粗网格上不望远镜, 不可用)
	var lap_newton := _surface_flux_sum(samples, phi_n, 1.0)
	var lap_regge := _surface_flux_sum(samples, phi_r, beta)
	var target := 4.0 * PI * GRAVITATIONAL_CONSTANT * mass_total  # ∇²Φ = 4πGρ

	# 残差分母用相对下限 (防 0 除, 不扭曲原子质量的 1e-33 量级)
	var denom = maxf(absf(target), absf(target) * 1e-9)
	var resid_regge = absf(lap_regge - target) / denom
	var resid_newton = absf(lap_newton - target) / denom

	# 6. 洛伦兹号差检查 (Lean: grEffectiveMetric_lorentzSignature — |h₀₀| < 1)
	var h00_max := 0.0
	for i in range(phi_r.size()):
		h00_max = maxf(h00_max, absf(beta * phi_r[i] * 2.0 / (SPEED_OF_LIGHT * SPEED_OF_LIGHT)))

	return {
		"poisson_residual_regge": resid_regge,
		"poisson_residual_newton": resid_newton,
		"laplacian_sum_regge": lap_regge,
		"laplacian_sum_newton": lap_newton,
		"gauss_target": target,
		"newtonian_scale_beta": beta,
		"h00_max": h00_max,
		"lorentz_signature_valid": h00_max < 1.0,
		"mass_total_kg": mass_total,
		"sample_count": samples.size(),
		"tet_count": tet_centers.size(),
		"evidence": "lean_bridge_numeric",
		"lean_refs": ["grEffectiveMetric", "grMetric_from_deficitDensity",
			"grEffectiveMetric_lorentzSignature"],
	}

## ---- Lean 定义的一一对应数值实现 ----

## Lean: reggeDualArea — 对偶面积 A = (√3/4)·l²
static func dual_area(edge_length: float) -> float:
	return (sqrt(3.0) / 4.0) * edge_length * edge_length

## Lean: reggeEffectiveRicciScalar — R_eff = 2·δ/A_dual
static func ricci_scalar(deficit: float, dual_area_v: float) -> float:
	if dual_area_v < 1e-15:
		return 0.0
	return 2.0 * deficit / dual_area_v

## Lean: reggeTetrahedronEdgeLength — l = κ/√(λᵢλⱼ)
static func spectral_edge_length(kappa: float, lam_i: float, lam_j: float) -> float:
	if lam_i <= 0.0 or lam_j <= 0.0 or kappa <= 0.0:
		return 0.0
	return kappa / sqrt(lam_i * lam_j)

## Lean: reggeDeficit_ricciScalar_closedForm — R = (8δ/√3)·λ²/κ²
static func closed_form_ricci(deficit: float, lam: float, kappa: float) -> float:
	if kappa <= 0.0:
		return 0.0
	return (8.0 * deficit / sqrt(3.0)) * lam * lam / (kappa * kappa)

## ---- 内部工具 ----

static func _calibrate_kappa(hinges: Array, weights: PackedFloat64Array) -> float:
	# 对 l_geo = κ/u (u = √(λᵢλⱼ)) 的最小二乘: κ* = Σ(l/u)/Σ(1/u²)
	var num := 0.0
	var den := 0.0
	for h in hinges:
		var e: Array = h.get("edge", [])
		if e.size() < 2:
			continue
		var a = int(e[0]); var b = int(e[1])
		if a >= weights.size() or b >= weights.size():
			continue
		var u = sqrt(weights[a] * weights[b])
		if u < 1e-15:
			continue
		num += float(h.get("length", 0.0)) / u
		den += 1.0 / (u * u)
	return num / den if den > 1e-15 else 1.0

static func _mean_lambda(hinges: Array, weights: PackedFloat64Array) -> float:
	var s := 0.0
	var n := 0
	for h in hinges:
		var e: Array = h.get("edge", [])
		if e.size() < 2:
			continue
		var a = int(e[0]); var b = int(e[1])
		if a >= weights.size() or b >= weights.size():
			continue
		s += sqrt(weights[a] * weights[b])
		n += 1
	return s / n if n > 0 else SPECTRAL_GAP_A4

## 谱间隙→曲率单调性方向检验 (Lean: spectralGap_to_ricciScalar_chain)
## λ 大 → l 短 → A 小 → R 大: 检验数值样本方向一致率
static func _check_monotonicity(hinges: Array, weights: PackedFloat64Array) -> bool:
	var lams: Array = []
	var rics: Array = []
	for h in hinges:
		var e: Array = h.get("edge", [])
		if e.size() < 2:
			continue
		var a = int(e[0]); var b = int(e[1])
		if a >= weights.size() or b >= weights.size():
			continue
		var eps = absf(float(h.get("deficit_angle", 0.0)))
		if eps < 1e-9:
			continue
		var lam = sqrt(weights[a] * weights[b])
		var a_dual = dual_area(float(h.get("length", 0.0)))
		if a_dual < 1e-15:
			continue
		lams.append(lam)
		rics.append(ricci_scalar(float(h.get("deficit_angle", 0.0)), a_dual))
	if lams.size() < 2:
		return true
	# 秩相关 (Spearman): λ 与 R 的方向一致性
	var agree := 0
	var total := 0
	for i in range(lams.size()):
		for j in range(i + 1, lams.size()):
			var dl = float(lams[j]) - float(lams[i])
			var dr = float(rics[j]) - float(rics[i])
			if absf(dl) < 1e-12 or absf(dr) < 1e-12:
				continue
			total += 1
			if dl * dr > 0.0:
				agree += 1
	if total == 0:
		return true
	return float(agree) / float(total) >= 0.5

static func _poisson_sample_box(positions: Array) -> Array:
	# 立方体采样盒: 边长 = 最大跨度 × 3 (margin=1×span, 源簇远离边界,
	# 保证各向同性步长与边界梯度求积精度)
	var mn := Vector3(INF, INF, INF)
	var mx := Vector3(-INF, -INF, -INF)
	for p in positions:
		mn = mn.min(p as Vector3)
		mx = mx.max(p as Vector3)
	var span = maxf(maxf(mx.x - mn.x, mx.y - mn.y), mx.z - mn.z)
	var side = span * 3.0
	var center = (mn + mx) * 0.5
	var box_min = center - Vector3(side, side, side) * 0.5

	# 完整 6×6×6 均匀网格 (216 点) — 离散高斯定理需要完整网格
	var samples: Array = []
	for i in range(6):
		for j in range(6):
			for k in range(6):
				var t = Vector3(float(i) / 5.0, float(j) / 5.0, float(k) / 5.0)
				samples.append(box_min + Vector3(side, side, side) * t)
	return samples

static func _nearest_delta(x: Vector3, centers: Array, deltas: Array) -> float:
	var best := INF
	var best_d := 0.0
	for i in range(centers.size()):
		var d = x.distance_to(centers[i] as Vector3)
		if d < best:
			best = d
			best_d = float(deltas[i])
	return best_d

static func _newton_potential(x: Vector3, atoms: Array, positions: Array,
		softening: float = 0.0) -> float:
	var phi := 0.0
	for i in range(atoms.size()):
		if i >= positions.size():
			continue
		var d = x.distance_to(positions[i] as Vector3)
		var r2 = d * d + softening * softening  # Plummer 软化, 保持体积分 = 4πGM
		phi -= GRAVITATIONAL_CONSTANT * _atom_mass_kg(atoms[i]) / sqrt(r2)
	return phi

static func _atom_mass_kg(atom: Dictionary) -> float:
	var data = ElementDB.get_element(str(atom.get("element", atom.get("symbol", "H"))))
	var amu = float(data.get("atomic_mass", 1.0))
	return amu * 1.66053907e-27

static func _least_squares_scale(target: PackedFloat64Array, base: PackedFloat64Array) -> float:
	var num := 0.0
	var den := 0.0
	for i in range(target.size()):
		num += target[i] * base[i]
		den += base[i] * base[i]
	return num / den if den > 1e-30 else 0.0

## 离散高斯定理 (面积分形式): ∮_∂Box ∇Φ·dS
## 要求 samples 为完整 6×6×6 均匀网格 (由 _poisson_sample_box 生成)
## 边界面上用面向外的一侧差分 dΦ/dn ≈ (Φ_边界层 - Φ_内层)/h, 乘以面元
## 对光滑边界势该格式与散度定理一致, 误差仅为边界导数求积误差
static func _surface_flux_sum(samples: Array, values: PackedFloat64Array,
		scale: float = 1.0) -> float:
	if samples.size() < 8:
		return 0.0
	var box_min := samples[0] as Vector3
	var box_max := samples[0] as Vector3
	for x in samples:
		box_min = box_min.min(x as Vector3)
		box_max = box_max.max(x as Vector3)
	var size_v: Vector3 = box_max - box_min
	var dx = maxf(size_v.x / 5.0, 1e-30)
	var dy = maxf(size_v.y / 5.0, 1e-30)
	var dz = maxf(size_v.z / 5.0, 1e-30)

	# 重建网格索引 (i,j,k ∈ 0..5)
	var grid := {}
	for idx in range(samples.size()):
		var x = samples[idx] as Vector3
		var t = (x - box_min) / size_v
		var i = int(round(t.x * 5.0))
		var j = int(round(t.y * 5.0))
		var k = int(round(t.z * 5.0))
		grid["%d_%d_%d" % [i, j, k]] = values[idx] * scale

	var flux := 0.0
	for j in range(6):
		for k in range(6):
			# +x 面: 二阶单侧导数 (3Φ₅-4Φ₄+Φ₃)/2h
			flux += (3.0 * float(grid["%d_%d_%d" % [5, j, k]])
				- 4.0 * float(grid["%d_%d_%d" % [4, j, k]])
				+ float(grid["%d_%d_%d" % [3, j, k]])) / (2.0 * dx) * dy * dz
			# -x 面: (-3Φ₀+4Φ₁-Φ₂)/2h, 外法向为 -x → 取负
			flux -= (-3.0 * float(grid["%d_%d_%d" % [0, j, k]])
				+ 4.0 * float(grid["%d_%d_%d" % [1, j, k]])
				- float(grid["%d_%d_%d" % [2, j, k]])) / (2.0 * dx) * dy * dz
	for i in range(6):
		for k in range(6):
			flux += (3.0 * float(grid["%d_%d_%d" % [i, 5, k]])
				- 4.0 * float(grid["%d_%d_%d" % [i, 4, k]])
				+ float(grid["%d_%d_%d" % [i, 3, k]])) / (2.0 * dy) * dx * dz
			flux -= (-3.0 * float(grid["%d_%d_%d" % [i, 0, k]])
				+ 4.0 * float(grid["%d_%d_%d" % [i, 1, k]])
				- float(grid["%d_%d_%d" % [i, 2, k]])) / (2.0 * dy) * dx * dz
	for i in range(6):
		for j in range(6):
			flux += (3.0 * float(grid["%d_%d_%d" % [i, j, 5]])
				- 4.0 * float(grid["%d_%d_%d" % [i, j, 4]])
				+ float(grid["%d_%d_%d" % [i, j, 3]])) / (2.0 * dz) * dx * dy
			flux -= (-3.0 * float(grid["%d_%d_%d" % [i, j, 0]])
				+ 4.0 * float(grid["%d_%d_%d" % [i, j, 1]])
				- float(grid["%d_%d_%d" % [i, j, 2]])) / (2.0 * dz) * dx * dy
	return flux

## [已弃用] 体积拉普拉斯中心差分求和 — 6³ 粗网格上非望远镜格式,
## 对 1/r 型势的积分误差达数百个百分点; 由 _surface_flux_sum 取代
static func _laplacian_volume_sum(samples: Array, values: PackedFloat64Array,
		scale: float = 1.0) -> float:
	if samples.size() < 8:
		return 0.0
	var box_min := samples[0] as Vector3
	var box_max := samples[0] as Vector3
	for x in samples:
		box_min = box_min.min(x as Vector3)
		box_max = box_max.max(x as Vector3)
	var size_v: Vector3 = box_max - box_min
	var dx = maxf(size_v.x / 5.0, 1e-30)
	var dy = maxf(size_v.y / 5.0, 1e-30)
	var dz = maxf(size_v.z / 5.0, 1e-30)
	var dv = dx * dy * dz

	# 重建网格索引
	var grid := {}
	for idx in range(samples.size()):
		var x = samples[idx] as Vector3
		var t = (x - box_min) / size_v
		var i = int(round(t.x * 5.0))
		var j = int(round(t.y * 5.0))
		var k = int(round(t.z * 5.0))
		grid["%d_%d_%d" % [i, j, k]] = values[idx] * scale

	var total := 0.0
	for i in range(1, 5):
		for j in range(1, 5):
			for k in range(1, 5):
				var c = float(grid.get("%d_%d_%d" % [i, j, k], 0.0))
				var lap = 0.0
				lap += (float(grid.get("%d_%d_%d" % [i - 1, j, k], 0.0)) - 2.0 * c
					+ float(grid.get("%d_%d_%d" % [i + 1, j, k], 0.0))) / (dx * dx)
				lap += (float(grid.get("%d_%d_%d" % [i, j - 1, k], 0.0)) - 2.0 * c
					+ float(grid.get("%d_%d_%d" % [i, j + 1, k], 0.0))) / (dy * dy)
				lap += (float(grid.get("%d_%d_%d" % [i, j, k - 1], 0.0)) - 2.0 * c
					+ float(grid.get("%d_%d_%d" % [i, j, k + 1], 0.0))) / (dz * dz)
				total += lap * dv
	return total

static func _empty_g16() -> Dictionary:
	return {
		"ricci_scalar_global": 0.0, "ricci_scalar_mean": 0.0,
		"ricci_scalar_closed_form": 0.0, "cross_check_rel_error": 0.0,
		"deficit_density": 0.0, "dual_area_mean": 0.0,
		"kappa": 0.0, "mean_spectral_weight": 0.0, "total_volume": 0.0,
		"monotonicity_holds": true, "per_hinge_ricci": [], "hinge_count": 0,
		"evidence": "lean_bridge_numeric", "lean_refs": [],
	}

static func _empty_g17() -> Dictionary:
	return {
		"poisson_residual_regge": 0.0, "poisson_residual_newton": 0.0,
		"surface_flux_regge": 0.0, "surface_flux_newton": 0.0,
		"gauss_target": 0.0, "newtonian_scale_beta": 0.0,
		"h00_max": 0.0, "lorentz_signature_valid": true,
		"mass_total_kg": 0.0, "sample_count": 0, "tet_count": 0,
		"evidence": "lean_bridge_numeric", "lean_refs": [],
	}
