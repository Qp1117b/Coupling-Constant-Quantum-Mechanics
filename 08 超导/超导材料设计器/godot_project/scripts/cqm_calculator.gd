extends RefCounted
class_name CQMCalculator

## CQM 超导计算引擎
## 计算链: 分子嘉当矩阵 → 谱分析 → 态密度 → 耦合 → McMillan/BCS-CQM Tc →
##          临界场 → 涌现积分 → 分步相变 → GL 自由能 → 三大作用量
## 数值物理专业化:
##   - 德拜温度优先取文献值 (SCData, Kittel/NIST/McMillan 编译), 无文献时回落到估算公式
##   - ω_log 以 θD 为代理 (文档注明近似)
##   - 每个输出量附证据等级 (evidence_levels)
##   - HIGH 精度模式启用全布里渊区 k 网格积分

const HBAR = 1.055e-34
const BOLTZMANN = 1.381e-23
const SPEED_OF_LIGHT = 2.998e8
const PLANCK_LENGTH = 1.616e-35
const FLUX_QUANTUM = 2.067e-15
const ELECTRON_MASS = 9.109e-31
const ELECTRON_CHARGE = 1.602e-19
const MU_0 = 1.257e-6
const EV_TO_K = 11604.5

enum PairingSymmetry { S_WAVE, D_WAVE, P_WAVE, EXTENDED_S }
enum Precision { FAST, NORMAL, HIGH }

const PAIRING_NAMES: Array = ["s波", "d波 (dx²-y²)", "p波", "扩展s波"]
const PAIRING_TC_SCALE: Array = [1.0, 0.85, 0.75, 0.95]

# 证据等级: lean_verified = Lean 形式化定理数值; literature = 文献输入;
#          semi_empirical = 半经验模型; phenomenological = 唯像实现; open_gap = 未闭合理论缺口
const EVIDENCE_LEVELS: Dictionary = {
	"A4_eigenvalues": "lean_verified",
	"spectral_gap": "lean_verified",
	"bcs_prefactor": "lean_verified",
	"universal_gap_ratio": "lean_verified",
	"causal_cutoff": "semi_empirical",
	"debye_temperature": "literature_or_estimate",
	"coupling": "semi_empirical",
	"tc_estimate": "semi_empirical",
	"critical_fields": "phenomenological",
	"emergence_integral": "phenomenological",
	"stepwise_transition": "semi_empirical",
	"gl_free_energy": "phenomenological",
	"actions": "phenomenological",
	"regge_cartan_G16": "lean_bridge_numeric",
	"regge_cartan_G17": "lean_bridge_numeric",
	"isotope_exponent": "semi_empirical",
}

static var _result_cache: Dictionary = {}
const CACHE_LIMIT := 32

static func causal_cutoff_temperature(sgap: float) -> float:
	var C = CQMConfig.get_spectral_quantum_c()
	var base = C * SPEED_OF_LIGHT / PLANCK_LENGTH
	var a4_gap = CQMConfig.get_spectral_gap()
	var correction = sgap / a4_gap if a4_gap > 0 else 1.0
	var omega = base * correction
	return HBAR * omega / BOLTZMANN

static func compute_dos_from_eigenvalues(eigenvalues: Array, ef: float = NAN, sigma: float = 0.1) -> float:
	if eigenvalues.is_empty():
		return 0.5
	if is_nan(ef):
		var sorted = eigenvalues.duplicate()
		sorted.sort()
		ef = sorted[sorted.size() / 2]
	var dos = 0.0
	var norm = 1.0 / (sqrt(2.0 * PI) * sigma)
	var two_sigma_sq = 2.0 * sigma * sigma
	for ev in eigenvalues:
		dos += norm * exp(-(ef - float(ev)) * (ef - float(ev)) / two_sigma_sq)
	return dos

## 德拜温度: 文献值优先, 回落到质量-半径估算
static func estimate_debye_temperature(symbol: String) -> float:
	var lit = SCData.get_debye_temperature(symbol)
	if not is_nan(lit):
		return lit
	var data = ElementDB.get_element(symbol)
	var mass = float(data.get("atomic_mass", 1.0))
	var covalent_r = float(data.get("covalent_radius_pm", 31))
	mass = max(mass, 0.1)
	covalent_r = max(covalent_r, 1.0)
	return 400.0 * sqrt(1.0 / mass) * (31.0 / covalent_r)

static func debye_source(symbols: Array) -> String:
	var lit_count = 0
	for sym in symbols:
		if not is_nan(SCData.get_debye_temperature(str(sym))):
			lit_count += 1
	if symbols.is_empty():
		return "无数据"
	if lit_count == 0:
		return "估算 (质量-半径公式)"
	if lit_count == symbols.size():
		return "文献值 (Kittel/NIST/McMillan 编译)"
	return "混合 (%d/%d 文献值)" % [lit_count, symbols.size()]

static func estimate_coupling_from_structure(eigenvalues: Array, dos_fermi: float, bonds: Array) -> float:
	if eigenvalues.is_empty() or bonds.is_empty():
		return 0.0
	var coupling_sum = 0.0
	for bond in bonds:
		var length = float(bond.get("length", 1.0))
		var r_a = float(bond.get("r_a", 0.5))
		var r_b = float(bond.get("r_b", 0.5))
		var r0 = r_a + r_b
		var beta = float(bond.get("order", 1)) * exp(-1.5 * abs(length - r0))
		coupling_sum += beta
	var avg_coupling = coupling_sum / bonds.size()
	return dos_fermi * avg_coupling

## 结构耦合与文献 λ 融合 (覆盖度加权, 文献 λ 作为锚点修正标度)
static func blend_literature_coupling(structure_coupling: float, symbols: Array) -> Dictionary:
	var lit = SCData.average_lambda_epc(symbols)
	if not lit.any_literature or structure_coupling <= 0:
		return {"coupling": structure_coupling, "lambda_literature": NAN, "coverage": 0.0}
	var lam_lit = float(lit.value)
	var coverage = float(lit.coverage)
	# 标度修正: 结构耦合按文献锚点的几何平均重标 (保留结构间相对差异)
	var rescaled = structure_coupling * pow(lam_lit / max(0.3, structure_coupling), 0.5 * coverage)
	return {
		"coupling": clamp(rescaled, 0.01, 4.0),
		"lambda_literature": lam_lit,
		"coverage": coverage
	}

static func mcmillan_tc(omega_log: float, coupling: float, mu_star: float) -> float:
	if coupling <= 0:
		return 0.0
	var denom = coupling - mu_star * (1.0 + 0.62 * coupling)
	if denom <= 0:
		return 0.0
	var exponent = -1.04 * (1.0 + coupling) / denom
	return (omega_log / 1.2) * exp(exponent)

## Allen–Dynes (1975) 完整公式: Tc = f1·f2·(ωlog/1.2)·exp[−1.04(1+λ)/(λ−μ*(1+0.62λ))]
## 修正因子 (原文式 23a/23b):
##   f1 = [1 + (λ/Λ1)^(3/2)]^(-1/3),  Λ1 = 2.46(1+3.8μ*)
##   f2 = 1 + [(√⟨ω²⟩/ωlog − 1)·λ^1.5] / (λ^1.5 + Λ2),  Λ2 = 1.82(1+3.0μ*)
## 返回 {tc, f1, f2}; 无声子谱时 √⟨ω²⟩ 以德拜模型关系近似
static func allen_dynes_tc(omega_log: float, sqrt_omega2: float,
		coupling: float, mu_star: float) -> Dictionary:
	var base = mcmillan_tc(omega_log, coupling, mu_star)
	if base <= 0:
		return {"tc": 0.0, "f1": 1.0, "f2": 1.0}
	var lam_15 = pow(coupling, 1.5)
	var lam1 = 2.46 * (1.0 + 3.8 * mu_star)
	var lam2 = 1.82 * (1.0 + 3.0 * mu_star)
	var f1 = pow(1.0 + pow(coupling / lam1, 1.5), -1.0 / 3.0)
	var f2 = 1.0
	if omega_log > 0:
		f2 = 1.0 + (sqrt_omega2 / omega_log - 1.0) * lam_15 / (lam_15 + lam2)
	return {"tc": base * f1 * f2, "f1": f1, "f2": f2}

## 德拜模型声子矩: g(ω) ∝ ω² 在 [0, ωD] 上
##   ωlog = ωD·exp(−1/3) (对数平均),  √⟨ω²⟩ = ωD·√(3/5) (二阶矩)
const DEBYE_OMEGA_LOG_FACTOR := 0.716531  # exp(-1/3)
const DEBYE_SQRT_OMEGA2_FACTOR := 0.774597  # sqrt(3/5)

## 化合物声子矩 (位点加权对数平均, 内部近似):
## α²F(Ω) ≈ Σᵢ wᵢ·α²Fᵢ(Ω) 可加 → ω_log = exp[Σᵢ wᵢ ln ω_log,i], ⟨ω²⟩ = Σᵢ wᵢ⟨ω²⟩ᵢ
## 权重 wᵢ: 元素文献 λᵢ (电声贡献权重) 有则归一化用之; 否则等权 (原子分数)
static func phonon_moments(atoms: Array) -> Dictionary:
	if atoms.is_empty():
		return {"omega_log": 400.0 * DEBYE_OMEGA_LOG_FACTOR,
			"sqrt_omega2": 400.0 * DEBYE_SQRT_OMEGA2_FACTOR,
			"debye_avg": 400.0, "weights": "默认"}
	var thetas: Array = []
	var lam_weights: Array = []
	var has_lambda := false
	var sum_debye := 0.0
	for a in atoms:
		var sym = a.get("symbol", "H") if a is Dictionary else a.element_symbol
		var th = estimate_debye_temperature(sym)
		thetas.append(th)
		sum_debye += th
		var lam = SCData.get_lambda_epc(sym)
		if is_nan(lam) or lam <= 0:
			lam_weights.append(0.0)
		else:
			lam_weights.append(lam)
			has_lambda = true
	var w_sum := 0.0
	for w in lam_weights:
		w_sum += w
	var n = atoms.size()
	var log_sum := 0.0
	var w2_sum := 0.0
	var lam_count := 0
	for w in lam_weights:
		if w > 0:
			lam_count += 1
	for i in range(n):
		var w = lam_weights[i] / w_sum if has_lambda and w_sum > 0 else 1.0 / n
		log_sum += w * log(thetas[i] * DEBYE_OMEGA_LOG_FACTOR)
		w2_sum += w * pow(thetas[i] * DEBYE_SQRT_OMEGA2_FACTOR, 2.0)
	return {
		"omega_log": exp(log_sum),
		"sqrt_omega2": sqrt(w2_sum),
		"debye_avg": sum_debye / n,
		"weights": "λ加权 (%d/%d 元素有文献λ)" % [lam_count, n],
	}

## 同位素指数 α 快速估计 (McMillan 链内两点数值导数):
## θD ∝ M^(−1/2) → ωlog ∝ M^(−1/2), λ 视为与 M 无关 → α = −dlnTc/dlnM
static func isotope_exponent_quick(omega_log: float, coupling: float, mu_star: float) -> float:
	var t1 = mcmillan_tc(omega_log, coupling, mu_star)
	var t2 = mcmillan_tc(omega_log * sqrt(1.0 / 1.05), coupling, mu_star)
	if t1 <= 0 or t2 <= 0:
		return NAN
	return log(t1 / t2) / log(1.05)

## McMillan/Allen-Dynes Tc 对 μ* 的敏感性 (文献惯例: 0.10/0.13/0.16 三列)
static func tc_mu_star_sensitivity(omega_log: float, sqrt_omega2: float,
		coupling: float) -> Dictionary:
	var out := {}
	for mus in [0.10, 0.13, 0.16]:
		out["%.2f" % mus] = allen_dynes_tc(omega_log, sqrt_omega2, coupling, mus).tc
	return out

## Allen-Dynes 强耦合条件 (公式有效域): λ > μ*(1+0.62λ)
static func mcmillan_valid(coupling: float, mu_star: float) -> bool:
	return coupling > mu_star * (1.0 + 0.62 * coupling)

static func estimate_tc(sgap: float, dos_fermi: float,
						  pressure: float = 0.0) -> Dictionary:
	var T_causal = causal_cutoff_temperature(sgap)
	var coupling = estimate_coupling(sgap, dos_fermi)
	if coupling <= 0:
		return {"tc": 0.0, "reason": "非正耦合", "coupling": 0.0}

	var bcs_exp = exp(-1.0 / coupling)
	var prefactor = CQMConfig.get_bcs_prefactor()
	var tc = prefactor * T_causal * bcs_exp

	if pressure > 0:
		tc *= 1.0 + 0.3 * log(1.0 + pressure / 50.0) / log(10.0)

	var mc_factor = _multicomponent_correction(sgap)
	tc *= mc_factor

	return {
		"tc": tc,
		"T_causal": T_causal,
		"coupling": coupling,
		"bcs_exp": bcs_exp,
		"pressure_factor": 1.0 + 0.3 * log(1.0 + pressure / 50.0) / log(10.0) if pressure > 0 else 1.0,
		"multicomponent_factor": mc_factor
	}

static func _multicomponent_correction(sgap: float) -> float:
	var eigenvalues = CQMCartanBuilder.A4_eigenvalues()
	if eigenvalues.size() < 4:
		return 1.0
	var sum_sq = 0.0
	for ev in eigenvalues:
		sum_sq += ev * ev
	if sgap <= 0:
		return 1.0
	return sum_sq / (4.0 * sgap * sgap)

static func order_parameters(tc: float, temperature: float, pairing: int = PairingSymmetry.S_WAVE) -> Array:
	if tc <= 0 or temperature >= tc:
		return []

	var gap_ratio = CQMConfig.get_universal_gap_ratio()
	if pairing == PairingSymmetry.D_WAVE:
		gap_ratio *= 0.8
	elif pairing == PairingSymmetry.P_WAVE:
		gap_ratio *= 0.7
	var delta_0 = gap_ratio * BOLTZMANN * tc / 2.0
	var temp_ratio = temperature / tc
	var temp_correction = sqrt(max(0.0, 1.0 - temp_ratio))
	delta_0 *= temp_correction

	var eigenvalues = CQMCartanBuilder.A4_eigenvalues()
	var params = []
	for k in range(min(4, eigenvalues.size())):
		var lambda_k = eigenvalues[k]
		var amplitude = delta_0 * sqrt(lambda_k)
		var phase = k * PI / 4.0
		if pairing == PairingSymmetry.D_WAVE:
			phase += PI / 2.0
		elif pairing == PairingSymmetry.P_WAVE:
			phase += PI / 3.0
		params.append({
			"channel": k + 1,
			"eigenvalue": lambda_k,
			"amplitude": amplitude,
			"phase": phase
		})
	return params

static func confidence_score(coupling: float, sgap: float, atom_count: int) -> float:
	var score = 0.0
	if coupling > 0:
		score += 0.3 * min(1.0, coupling)
	var a4_gap = CQMConfig.get_spectral_gap()
	var gap_ratio = sgap / a4_gap if a4_gap > 0 else 0.0
	score += 0.3 * min(1.0, gap_ratio)
	var atom_factor = 1.0 - abs(atom_count - 10) / 20.0
	score += 0.2 * clamp(atom_factor, 0.0, 1.0)
	score += 0.2
	return clamp(score, 0.0, 1.0)

static func evaluate_molecule(atoms: Array, bonds: Array,
								params: Dictionary = {}) -> Dictionary:
	var cache_key = _cache_key(atoms, bonds, params)
	if _result_cache.has(cache_key):
		var cached: Dictionary = _result_cache[cache_key]
		cached["from_cache"] = true
		return cached

	var t0 = Time.get_ticks_usec()
	var temperature = float(params.get("temperature", 4.2))
	var pressure = float(params.get("pressure_mag", 0.0))
	var mag_field = float(params.get("mag_field_mag", 0.0))
	var strain = params.get("strain", [0.0,0.0,0.0,0.0,0.0,0.0])
	var efield = params.get("efield", Vector3.ZERO)
	var doping = float(params.get("doping", 0.0))
	var spin_orbit = float(params.get("spin_orbit", 0.0))
	var mu_star = float(params.get("mu_star", SCData.get_typical_mu_star()))
	var pairing = int(params.get("pairing_symmetry", PairingSymmetry.S_WAVE))
	var precision = int(params.get("precision", Precision.NORMAL))

	var mol_cartan = _build_molecular_cartan(atoms, bonds)
	var mol_eigenvalues = mol_cartan.get("eigenvalues", [])
	var gap = float(mol_cartan.get("spectral_gap", 0.0))
	if gap <= 0.0:
		gap = CQMCartanBuilder.spectral_gap()

	var dos_f = compute_dos_from_eigenvalues(mol_eigenvalues)
	if dos_f <= 0:
		dos_f = 0.5

	gap = apply_electric_field(gap, efield)
	dos_f = apply_doping(dos_f, doping)
	var strain_factor = apply_strain_full(strain, pairing)
	gap *= strain_factor

	var enriched_bonds = _enrich_bonds(atoms, bonds)
	var coupling = estimate_coupling_from_structure(mol_eigenvalues, dos_f, enriched_bonds)
	coupling = apply_spin_orbit(coupling, spin_orbit)
	if coupling <= 0:
		coupling = estimate_coupling(gap, dos_f)

	var symbols: Array = []
	for i in range(atoms.size()):
		symbols.append(_get_atom_symbol(atoms, i))
	var blended = blend_literature_coupling(coupling, symbols)
	coupling = float(blended.coupling)

	# 德拜温度: 文献值优先 (Kittel/NIST/McMillan 编译)
	# 化合物声子矩: 位点加权对数平均 (phonon_moments), 替代简单算术平均
	var pm = phonon_moments(atoms)
	var avg_debye = float(pm.debye_avg)
	var omega_log_temp = float(pm.omega_log)
	var sqrt_omega2_temp = float(pm.sqrt_omega2)
	var phonon_weights = str(pm.weights)
	var ad = allen_dynes_tc(omega_log_temp, sqrt_omega2_temp, coupling, mu_star)
	var tc_mcmillan = float(ad.tc)
	var mcmillan_ok = mcmillan_valid(coupling, mu_star)
	var tc_bcs = estimate_tc(gap, dos_f, pressure)
	var use_mcmillan = tc_mcmillan > 0 and mcmillan_ok
	var tc = tc_mcmillan if use_mcmillan else tc_bcs.tc
	var tc_method = "Allen-Dynes 1975" if use_mcmillan else "BCS-CQM修正"

	if pressure > 0 and use_mcmillan:
		tc *= 1.0 + 0.3 * log(1.0 + pressure / 50.0) / log(10.0)

	tc *= PAIRING_TC_SCALE[pairing] if pairing < PAIRING_TC_SCALE.size() else 1.0

	tc = apply_magnetic_field(tc, mag_field, temperature)
	var confidence = confidence_score(coupling, gap, atoms.size())
	var verdict = _make_verdict(tc, temperature, confidence)

	var delta_0 = CQMConfig.get_universal_gap_ratio() * BOLTZMANN * tc / 2.0
	var critical = compute_critical_fields(tc, temperature, delta_0, pairing)

	var order_params = order_parameters(tc, temperature, pairing)
	var topology_factor = CQMTopologyFactor.compute_from_spectral_gap(gap)
	var emergence = CQMEmergenceIntegral.evaluate(mol_eigenvalues, gap, temperature, dos_f, tc,
			CQMEmergenceIntegral.Precision.NORMAL, topology_factor)

	# HIGH 精度: 全布里渊区 k 网格数值积分 (16^3 = 4096 点)
	var emergence_full: Dictionary = {}
	if precision == Precision.HIGH and mol_cartan.has("matrix"):
		var dim = int(mol_cartan.get("dimension", 0))
		if dim > 0 and dim <= 256:
			emergence_full = CQMEmergenceIntegral.evaluate_full_bz(
				mol_cartan["matrix"], dim, temperature, tc, gap, 16)

	var stepwise = CQMStepwiseTransition.compute(mol_eigenvalues, tc)
	var condensate = CQMStepwiseTransition.condensate_state(temperature, stepwise.transitions)
	var gl = CQMGLFreeEnergy.compute(order_params, temperature, tc)
	var bcs_path = CQMEmergenceIntegral.bcs_degradation(mol_eigenvalues, gap, dos_f, tc)

	# 三大作用量 (理论 §3; Regge-嘉当耦合为唯像实现, 严格化见缺口 G16/G17)
	var actions = _compute_actions(atoms, bonds, order_params, mol_eigenvalues, temperature,
			topology_factor, delta_0, pressure)

	var result = {
		"verdict": verdict,
		"tc_estimate": tc,
		"confidence": confidence,
		"eigenvalues": mol_eigenvalues,
		"spectral_gap": gap,
		"causal_cutoff_temp": tc_bcs.get("T_causal", 0.0),
		"coupling": coupling,
		"lambda_literature": blended.get("lambda_literature", NAN),
		"lambda_coverage": blended.get("coverage", 0.0),
		"dos_fermi": dos_f,
		"debye_temp": avg_debye,
		"debye_source": debye_source(symbols),
		"omega_log_temp": omega_log_temp,
		"sqrt_omega2_temp": sqrt_omega2_temp,
		"phonon_weights": phonon_weights,
		"ad_f1": float(ad.f1),
		"ad_f2": float(ad.f2),
		"mu_star": mu_star,
		"mcmillan_valid": mcmillan_ok,
		"tc_method": tc_method,
		"tc_mu_star_sensitivity": tc_mu_star_sensitivity(omega_log_temp, sqrt_omega2_temp, coupling) if mcmillan_ok else {},
		"isotope_alpha": isotope_exponent_quick(omega_log_temp, coupling, mu_star),
		"n0v_product": dos_f * (1.0 / (1.0 + gap / CQMConfig.get_spectral_gap())) if CQMConfig.get_spectral_gap() > 0 else NAN,
		"pairing_symmetry": pairing,
		"gap_0": delta_0,
		"gap_0_meV": delta_0 * 1000.0 / ELECTRON_CHARGE,
		"order_parameters": order_params,
		"atom_count": atoms.size(),
		"bond_count": bonds.size(),
		"temperature": temperature,
		"pressure": pressure,
		"mag_field": mag_field,
		"strain_factor": strain_factor,
		"doping": doping,
		"spin_orbit": spin_orbit,
		"critical_fields": critical,
		"cqm_emergence": emergence,
		"cqm_emergence_full": emergence_full,
		"cqm_topology_factor": topology_factor,
		"cqm_stepwise": stepwise,
		"cqm_condensate": condensate,
		"cqm_gl_free_energy": gl,
		"cqm_bcs_degradation": bcs_path,
		"cqm_actions": actions,
		"evidence_levels": EVIDENCE_LEVELS,
		"precision": precision,
		"compute_time_ms": 0.0,
		"from_cache": false,
	}

	result.compute_time_ms = (Time.get_ticks_usec() - t0) / 1000.0
	_cache_store(cache_key, result)
	return result

## 三大 CQM 作用量数值实现 (§3.1 约束 / §3.3 再生产 / §3.4 电子)
static func _compute_actions(atoms: Array, bonds: Array, order_params: Array,
								eigenvalues: Array, temperature: float,
								topology_factor: float, energy_gap: float,
								pressure: float) -> Dictionary:
	var positions: Array = []
	for i in range(atoms.size()):
		positions.append(_get_atom_position(atoms, i))
	var pairs: Array = []
	for bond in bonds:
		pairs.append([int(bond.get("a", 0)), int(bond.get("b", 0))])

	# 关系网络 R_ij: 键连接强度 (距离衰减)
	var relation_network = _build_relation_network(positions, pairs)

	# Regge 四面体 (作为约束作用量几何骨架)
	var regge = ReggeCalculator.compute_regge_3d(positions, pairs, 1)
	var s_constraint = CQMConstraintAction.compute(regge.get("tetrahedra", []), relation_network, pressure)

	# G16/G17: Regge-嘉当耦合数值桥接 (严格化对应 Lean 形式化)
	var g16 = ReggeCartanBridge.compute_g16(regge, atoms)
	var g17 = ReggeCartanBridge.compute_g17(regge, atoms, positions)

	# 因果潜能张量 T_T: 由 A₄ 四通道序参量构成对角张量
	var causal_tensor = _causal_tensor_from_order_params(order_params)
	var s_reproduction = CQMReproductionAction.compute(causal_tensor, eigenvalues, temperature,
			topology_factor, energy_gap)

	# 电子态: 序参量幅值作为旋量范数代理
	var electron_states: Array = []
	for op in order_params:
		electron_states.append(float(op.get("amplitude", 0.0)))
	var a4 = CQMCartanBuilder.A4()
	var s_electron = CQMElectronAction.compute(electron_states, causal_tensor, a4,
			relation_network, Vector3.ZERO)

	return {
		"S_constraint": s_constraint,
		"S_reproduction": s_reproduction,
		"S_electron": s_electron,
		"regge_action": regge.get("regge_action", 0.0),
		"tetrahedra_count": regge.get("tetrahedra_count", 0),
		"G16_ricci": g16,
		"G17_newtonian": g17,
	}

static func _build_relation_network(positions: Array, pairs: Array) -> Array:
	var n = positions.size()
	if n == 0:
		return []
	var network: Array = []
	for i in range(n):
		var row: Array = []
		row.resize(n)
		row.fill(0.0)
		network.append(row)
	for pair in pairs:
		var a = int(pair[0])
		var b = int(pair[1])
		if a >= 0 and a < n and b >= 0 and b < n:
			var d = (positions[a] as Vector3).distance_to(positions[b])
			var strength = exp(-1.5 * max(0.0, d - 1.0)) if d > 0 else 1.0
			network[a][b] = strength
			network[b][a] = strength
	return network

static func _causal_tensor_from_order_params(order_params: Array) -> Array:
	var tensors: Array = []
	for op in order_params:
		var amp = float(op.get("amplitude", 0.0))
		var row_idx = int(op.get("channel", 1)) - 1
		var t: Array = []
		for i in range(4):
			var row: Array = []
			for j in range(4):
				row.append(amp if (i == row_idx and i == j) else 0.0)
			t.append(row)
		tensors.append(t)
	return tensors

static func _build_molecular_cartan(atoms: Array, bonds: Array) -> Dictionary:
	var enriched_atoms: Array = []
	for a in atoms:
		var sym = a.get("symbol", "H") if a is Dictionary else a.element_symbol
		var data = ElementDB.get_element(sym)
		var z = int(data.get("atomic_number", 1))
		var iso = int(a.get("isotope", 1)) if a is Dictionary else int(a.isotope_mass)
		var n_count = iso - z
		var defect = CQMCartanBuilder.neutron_defect(n_count, sym)
		enriched_atoms.append({"neutron_defect": defect})
	var enriched_bonds = _enrich_bonds(atoms, bonds)
	return MolecularCartan.compute_molecular_cartan(enriched_atoms, enriched_bonds)

static func _enrich_bonds(atoms: Array, bonds: Array) -> Array:
	var result: Array = []
	for bond in bonds:
		var a_idx = int(bond.get("a", 0))
		var b_idx = int(bond.get("b", 0))
		var order = int(bond.get("order", 1))
		var pos_a = _get_atom_position(atoms, a_idx)
		var pos_b = _get_atom_position(atoms, b_idx)
		var length = pos_a.distance_to(pos_b)
		var sym_a = _get_atom_symbol(atoms, a_idx)
		var sym_b = _get_atom_symbol(atoms, b_idx)
		var data_a = ElementDB.get_element(sym_a)
		var data_b = ElementDB.get_element(sym_b)
		var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
		var r_b = float(data_b.get("covalent_radius_pm", 50)) / 100.0
		result.append({
			"a": a_idx, "b": b_idx, "order": order,
			"length": length, "r_a": r_a, "r_b": r_b
		})
	return result

static func _get_atom_position(atoms: Array, idx: int) -> Vector3:
	if idx < 0 or idx >= atoms.size():
		return Vector3.ZERO
	var a = atoms[idx]
	if a is Dictionary:
		return a.get("position", Vector3.ZERO)
	return a.position

static func _get_atom_symbol(atoms: Array, idx: int) -> String:
	if idx < 0 or idx >= atoms.size():
		return "H"
	var a = atoms[idx]
	if a is Dictionary:
		return a.get("symbol", "H")
	return a.element_symbol

static func _avg_debye_temperature(atoms: Array) -> float:
	if atoms.is_empty():
		return 400.0
	var sum = 0.0
	for a in atoms:
		var sym = a.get("symbol", "H") if a is Dictionary else a.element_symbol
		sum += estimate_debye_temperature(sym)
	return sum / atoms.size()

static func compute_critical_fields(tc: float, temperature: float, delta: float, _pairing: int = 0) -> Dictionary:
	if tc <= 0 or delta <= 0:
		return {"hc1": 0.0, "hc2": 0.0, "hc": 0.0, "kappa": 0.0, "xi": 0.0, "lambda_L": 0.0}
	var vf = 1.0e6
	var xi_0 = HBAR * vf / (PI * delta)
	var n_s = 1.0e28
	var lambda_L = sqrt(ELECTRON_MASS / (MU_0 * n_s * ELECTRON_CHARGE * ELECTRON_CHARGE))
	var t_ratio = temperature / tc if tc > 0 else 0.0
	var temp_factor = sqrt(max(0.0, 1.0 - t_ratio))
	var xi = xi_0 / temp_factor if temp_factor > 0 else xi_0
	var lambda_t = lambda_L / sqrt(max(0.0, 1.0 - pow(t_ratio, 4))) if t_ratio < 1.0 else lambda_L
	var hc2 = FLUX_QUANTUM / (2.0 * PI * xi * xi)
	var hc1 = FLUX_QUANTUM / (4.0 * PI * lambda_t * lambda_t) * log(lambda_t / xi) if lambda_t > xi else 0.0
	var hc = FLUX_QUANTUM / (2.0 * sqrt(2.0) * PI * lambda_t * xi)
	var kappa = lambda_t / xi
	var gamma = 5.0
	var hc2_ab = hc2
	var hc2_c = hc2 / (gamma * gamma)
	return {
		"hc1": hc1, "hc2": hc2, "hc": hc,
		"kappa": kappa, "xi": xi, "lambda_L": lambda_t,
		"hc2_ab": hc2_ab, "hc2_c": hc2_c, "gamma": gamma,
		"type": "II型" if kappa > 1.0 / sqrt(2.0) else "I型"
	}

static func apply_magnetic_field(tc: float, b_magnitude: float, temperature: float) -> float:
	if tc <= 0 or b_magnitude <= 0:
		return tc
	var delta_0 = CQMConfig.get_universal_gap_ratio() * BOLTZMANN * tc / 2.0
	var vf = 1.0e6
	var xi_0 = HBAR * vf / (PI * delta_0)
	var t_ratio = temperature / tc if tc > 0 else 0.0
	var xi = xi_0 / sqrt(max(0.0, 1.0 - t_ratio)) if t_ratio < 1.0 else xi_0
	var hc2 = FLUX_QUANTUM / (2.0 * PI * xi * xi)
	if b_magnitude >= hc2:
		return 0.0
	var suppression = sqrt(1.0 - b_magnitude / hc2)
	return tc * suppression

static func apply_strain_full(strain: Array, pairing: int = 0) -> float:
	var trace = 0.0
	for i in range(min(3, strain.size())):
		trace += float(strain[i])
	var volumetric = trace / 3.0
	var factor = 1.0 + volumetric * 0.5
	if pairing == PairingSymmetry.D_WAVE and strain.size() >= 2:
		var shear = float(strain[0]) - float(strain[1])
		factor += 0.3 * shear * shear
	return factor

static func apply_strain(strain: Array) -> float:
	return apply_strain_full(strain, PairingSymmetry.S_WAVE)

static func apply_electric_field(gap: float, efield) -> float:
	var e_mag = 0.0
	if efield is Vector3:
		e_mag = efield.length()
	else:
		e_mag = float(efield)
	if e_mag <= 0:
		return gap
	var stark_shift = 0.001 * sqrt(e_mag)
	return gap * (1.0 + stark_shift)

static func apply_doping(dos_f: float, doping: float) -> float:
	return clamp(dos_f * (1.0 + doping * 0.5), 0.01, 10.0)

static func apply_spin_orbit(coupling: float, spin_orbit: float) -> float:
	return coupling * (1.0 + spin_orbit * 0.3)

static func estimate_coupling(sgap: float, dos_fermi: float) -> float:
	if sgap <= 0:
		return 0.0
	var a4_gap = CQMConfig.get_spectral_gap()
	var V0 = 1.0 / (1.0 + sgap / a4_gap)
	return dos_fermi * V0

static func _make_verdict(tc: float, target_temp: float, confidence: float) -> String:
	if confidence < 0.2:
		return "insufficient"
	if tc <= 0:
		return "normal"
	if tc > target_temp * 1.2:
		return "superconducting"
	if tc > target_temp * 0.8:
		return "borderline"
	return "normal"

# === 参数扫描 (高通量工具) ===

## 压强扫描: 返回 [{pressure_GPa, tc, verdict}]
static func sweep_pressure(atoms: Array, bonds: Array, base_params: Dictionary,
							p_min: float, p_max: float, steps: int = 12) -> Array:
	var results: Array = []
	if steps < 2 or p_max < p_min:
		return results
	for i in range(steps):
		var p = p_min + (p_max - p_min) * float(i) / float(steps - 1)
		var params = base_params.duplicate(true)
		params["pressure_mag"] = p
		params["precision"] = Precision.FAST
		var r = evaluate_molecule(atoms, bonds, params)
		results.append({
			"pressure_GPa": p,
			"tc": r.get("tc_estimate", 0.0),
			"verdict": r.get("verdict", ""),
			"coupling": r.get("coupling", 0.0),
		})
	return results

## 同位素质量扫描: mass_scale ∈ [scale_min, scale_max], 返回 [{mass_scale, avg_mass, tc}]
## 同位素效应指数 α 由 Tc ∝ M^(-α) 拟合
static func sweep_isotope(atoms: Array, bonds: Array, base_params: Dictionary,
							scale_min: float = 0.5, scale_max: float = 3.0,
							steps: int = 11) -> Dictionary:
	var sweep: Array = []
	if steps < 2:
		return {"points": sweep, "alpha": NAN}
	var base_mass = _average_isotope_mass(atoms)
	for i in range(steps):
		var s = scale_min + (scale_max - scale_min) * float(i) / float(steps - 1)
		var scaled_atoms: Array = []
		for a in atoms:
			if a is Dictionary:
				var dup = a.duplicate(true)
				dup["isotope"] = int(round(float(dup.get("isotope", 1)) * s))
				scaled_atoms.append(dup)
			else:
				scaled_atoms.append(a)
		var params = base_params.duplicate(true)
		params["precision"] = Precision.FAST
		var r = evaluate_molecule(scaled_atoms, bonds, params)
		sweep.append({
			"mass_scale": s,
			"avg_mass": base_mass * s,
			"tc": r.get("tc_estimate", 0.0),
		})
	var alpha = fit_isotope_exponent(sweep)
	return {"points": sweep, "alpha": alpha, "base_mass": base_mass}

## 二元合金成分扫描: B 元素摩尔分数 x ∈ [0,1], 返回 {points, symbols}
## 结构: 简立方格点 (化学理想间距), B 原子按 Bresenham 型确定性均匀分布 (无随机数, 可复现)
static func sweep_composition(symbol_a: String, symbol_b: String, total_atoms: int,
		base_params: Dictionary, steps: int = 11) -> Dictionary:
	var points: Array = []
	if steps < 2 or total_atoms < 2 or symbol_a == symbol_b:
		return {"points": points, "symbols": [symbol_a, symbol_b]}
	total_atoms = mini(total_atoms, 64)
	var spacing = ChemValidator.ideal_bond_length(symbol_a, symbol_b)
	if spacing <= 0:
		spacing = 2.5
	var template = _build_sc_alloy(symbol_a, symbol_b, total_atoms, 1, spacing)
	var bonds = _sc_bonds(template, spacing)
	for i in range(steps):
		var x = float(i) / float(steps - 1)
		var count_b = int(round(x * total_atoms))
		var alloy = _build_sc_alloy(symbol_a, symbol_b, total_atoms, count_b, spacing)
		var params = base_params.duplicate(true)
		params["precision"] = Precision.FAST
		var r = evaluate_molecule(alloy, bonds, params)
		points.append({
			"x": x,
			"count_b": count_b,
			"formula": "%s%.2f%s%.2f" % [symbol_a, 1.0 - x, symbol_b, x],
			"tc": r.get("tc_estimate", 0.0),
			"coupling": r.get("coupling", 0.0),
			"debye_temp": r.get("debye_temp", 0.0),
			"verdict": r.get("verdict", ""),
		})
	# 最优成分点
	var best = {}
	var best_tc = -1.0
	for p in points:
		if float(p.get("tc", 0.0)) > best_tc:
			best_tc = float(p.get("tc", 0.0))
			best = p
	return {"points": points, "symbols": [symbol_a, symbol_b], "best": best}

## 简立方合金结构: count_b 个 B 原子按确定性均匀分布 (Bresenham 型)
static func _build_sc_alloy(symbol_a: String, symbol_b: String, total: int,
		count_b: int, spacing: float) -> Array:
	var side = int(ceil(pow(total, 1.0 / 3.0)))
	var atoms: Array = []
	var idx = 0
	for ix in range(side):
		for iy in range(side):
			for iz in range(side):
				if idx >= total:
					break
				var is_b = (floor(float(idx + 1) * count_b / float(total))
					> floor(float(idx) * count_b / float(total)))
				var sym = symbol_b if is_b else symbol_a
				atoms.append({
					"symbol": sym,
					"position": Vector3(ix, iy, iz) * spacing,
				})
				idx += 1
	return atoms

## 简立方最近邻键 (6 配位)
static func _sc_bonds(atoms: Array, spacing: float) -> Array:
	var bonds: Array = []
	var n = atoms.size()
	var cutoff = spacing * 1.3
	for i in range(n):
		var pi = atoms[i].get("position", Vector3.ZERO)
		for j in range(i + 1, n):
			var d = pi.distance_to(atoms[j].get("position", Vector3.ZERO))
			if d < cutoff:
				bonds.append({"a": i, "b": j, "order": 1})
	return bonds

static func _average_isotope_mass(atoms: Array) -> float:
	if atoms.is_empty():
		return 1.0
	var sum = 0.0
	for a in atoms:
		var sym = a.get("symbol", "H") if a is Dictionary else a.element_symbol
		var iso = float(a.get("isotope", 1)) if a is Dictionary else float(a.isotope_mass)
		var iso_data = ElementDB.get_isotope(sym, int(iso))
		if not iso_data.is_empty():
			sum += float(iso_data.get("mass_da", iso))
		else:
			var ed = ElementDB.get_element(sym)
			sum += float(ed.get("atomic_mass", iso))
	return sum / atoms.size()

## 同位素指数 α 拟合: log Tc = -α log M + c (最小二乘)
static func fit_isotope_exponent(points: Array) -> float:
	var valid: Array = []
	for p in points:
		var m = float(p.get("avg_mass", 0.0))
		var tc = float(p.get("tc", 0.0))
		if m > 0 and tc > 0:
			valid.append([log(m), log(tc)])
	if valid.size() < 2:
		return NAN
	var n = float(valid.size())
	var sx = 0.0
	var sy = 0.0
	var sxx = 0.0
	var sxy = 0.0
	for p in valid:
		sx += p[0]
		sy += p[1]
		sxx += p[0] * p[0]
		sxy += p[0] * p[1]
	var denom = n * sxx - sx * sx
	if abs(denom) < 1e-12:
		return NAN
	var slope = (n * sxy - sx * sy) / denom
	return -slope

# === 结果缓存 ===

static func _cache_key(atoms: Array, bonds: Array, params: Dictionary) -> String:
	var parts: Array = []
	for i in range(atoms.size()):
		var a = atoms[i]
		if a is Dictionary:
			var pos = a.get("position", Vector3.ZERO)
			parts.append("%s|%d|%.3f,%.3f,%.3f" % [a.get("symbol", "?"),
				int(a.get("isotope", 0)), pos.x, pos.y, pos.z])
		else:
			parts.append("%s|%d" % [a.element_symbol, int(a.isotope_mass)])
	var bond_parts: Array = []
	for b in bonds:
		bond_parts.append("%d-%d:%d" % [int(b.get("a", 0)), int(b.get("b", 0)), int(b.get("order", 1))])
	var param_parts: Array = []
	for key in ["temperature", "pressure_mag", "mag_field_mag", "doping", "spin_orbit",
				"mu_star", "pairing_symmetry", "precision"]:
		param_parts.append("%s=%s" % [key, str(params.get(key, ""))])
	var strain = params.get("strain", [])
	param_parts.append("strain=%s" % str(strain))
	var efield = params.get("efield", Vector3.ZERO)
	param_parts.append("efield=%.3f" % (efield.length() if efield is Vector3 else float(efield)))
	return "|".join(parts) + "#" + ";".join(bond_parts) + "#" + ";".join(param_parts)

static func _cache_store(key: String, result: Dictionary) -> Dictionary:
	if _result_cache.size() >= CACHE_LIMIT:
		var first_key = _result_cache.keys()[0]
		_result_cache.erase(first_key)
	result["from_cache"] = false
	_result_cache[key] = result
	return result

static func clear_cache() -> void:
	_result_cache.clear()

static func cache_size() -> int:
	return _result_cache.size()
