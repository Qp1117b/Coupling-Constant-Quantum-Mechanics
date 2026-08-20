extends RefCounted
class_name GravitationalField

## 晶胞分布→FG退相干场（角亏场直接给出因果约束强度）
## 理论: FG是GR在深度层级的非吸引力效应, 不走Regge→GR连续极限路径
## CQM超导: 晶粒中质子-中子关系网络→FG退相干场→因果约束→库珀对涌现
## 因果截断频率: ω_causal = Γ_φ · |τ|  (Γ_φ由Regge角亏决定)
## 更新: FG是GR的层级非吸引力效应(§2.3), 网络依赖(§5), 退相干两阶段(§4.3)

static func compute_causal_field(regge_result: Dictionary, grain_distribution: String = "single_crystal", temperature: float = 0.0) -> Dictionary:
	var regge_action = float(regge_result.get("regge_action", 0.0))
	var total_deficit = float(regge_result.get("total_deficit", 0.0))
	var mean_curvature = float(regge_result.get("mean_curvature", 0.0))
	var gamma_phi = _compute_causal_decay_rate(regge_action, mean_curvature)
	var omega_causal = _compute_causal_frequency(gamma_phi, temperature)
	var field_strength = _compute_field_strength(regge_action, grain_distribution)
	var decoherence = _compute_decoherence_field(gamma_phi, total_deficit, grain_distribution)
	var topology = _classify_topology(grain_distribution, total_deficit)
	return {
		"gamma_phi": gamma_phi,
		"omega_causal": omega_causal,
		"field_strength": field_strength,
		"decoherence_field": decoherence,
		"topology": topology,
		"grain_distribution": grain_distribution,
		"temperature": temperature,
		"regge_action": regge_action,
		"mean_curvature": mean_curvature
	}

static func compute_from_cartan_chain(chain_result: Dictionary, grain_distribution: String = "single_crystal", temperature: float = 0.0) -> Dictionary:
	var regge_data = chain_result.get("regge", {})
	var spectral_gap = float(regge_data.get("spectral_gap", 0.0))
	var deficit_angles: Array = regge_data.get("deficit_angles", [])
	var total_deficit = 0.0
	for d in deficit_angles:
		total_deficit += d
	var has_lattice = bool(chain_result.get("has_lattice", false))
	var n_neighbors = int(chain_result.get("n_neighbors", 1))
	var n_formula_units = int(chain_result.get("n_formula_units", 1))
	var gamma_phi = spectral_gap * 0.1
	var omega_causal = gamma_phi / max(temperature, 0.01)
	var field_strength = abs(total_deficit) * spectral_gap
	var decoherence = _compute_decoherence_field(gamma_phi, total_deficit, grain_distribution)
	var topology = _classify_topology(grain_distribution, total_deficit)
	var mol_dim = int(chain_result.get("dimensions", [0,0,0,0,0])[2])
	var cell_dim = int(chain_result.get("dimensions", [0,0,0,0,0])[3])
	var lattice_coupling_ratio = float(cell_dim) / max(float(mol_dim), 1.0)
	var elem_data = chain_result.get("element", {})
	var Z = int(elem_data.get("Z", 0))
	var N = int(elem_data.get("N", 0))
	var network_satisfied = N > 0
	return {
		"gamma_phi": gamma_phi,
		"omega_causal": omega_causal,
		"field_strength": field_strength,
		"decoherence_field": decoherence,
		"topology": topology,
		"grain_distribution": grain_distribution,
		"temperature": temperature,
		"spectral_gap": spectral_gap,
		"total_deficit": total_deficit,
		"source": "cartan_chain",
		"has_lattice": has_lattice,
		"n_neighbors": n_neighbors,
		"n_formula_units": n_formula_units,
		"lattice_coupling_ratio": lattice_coupling_ratio,
		"Z": Z,
		"N": N,
		"network_satisfied": network_satisfied
	}

## FG是GR的层级非吸引力效应: 嘉当矩阵同时分化为两个输出 (§4.1)
## FG = 离散Regge几何 (如何连接) — GR的深度层级效应
## GR = 能动张量T_μν近似 (有多少能量) — 比FG更基础
## 网络依赖: 无中子(N=0)则FG=0, GR=0 (§5)
static func compute_dual_gravity(chain_result: Dictionary, grain_distribution: String = "single_crystal", temperature: float = 0.0) -> Dictionary:
	var elem_data = chain_result.get("element", {})
	var Z = int(elem_data.get("Z", 0))
	var N = int(elem_data.get("N", 0))
	var network_satisfied = N > 0
	var regge_data = chain_result.get("regge", {})
	var spectral_gap = float(regge_data.get("spectral_gap", 0.0))
	var deficit_angles: Array = regge_data.get("deficit_angles", [])
	var total_deficit = 0.0
	for d in deficit_angles:
		total_deficit += d
	var stage_I = {
		"description": "退相干I: QG→禁闭边界, 产生A4(质子)+D(中子缺陷)",
		"Z": Z,
		"N": N,
		"cartan_dimension": int(elem_data.get("dimension", 0)),
		"spectral_gap": float(elem_data.get("spectral_gap", 0.0))
	}
	var fg_output: Dictionary
	var gr_output: Dictionary
	if not network_satisfied:
		fg_output = {
			"regge_action": 0.0,
			"total_deficit": 0.0,
			"hinge_count": 0,
			"topology": "trivial",
			"field_strength": 0.0,
			"reason": "无中子: 单质子无铰链网络, FG=0 (§5.1)"
		}
		gr_output = {
			"energy_density": 0.0,
			"pressure": 0.0,
			"trace_T": 0.0,
			"has_spacetime": false,
			"reason": "无中子: 无FG网络→经典时空不涌现→T_μν无定义, GR=0 (§5.2)"
		}
	else:
		var regge_action = abs(total_deficit) * spectral_gap * float(N)
		var hinge_count = deficit_angles.size()
		var topology = _classify_topology(grain_distribution, total_deficit)
		var fg_field_strength = abs(total_deficit) * spectral_gap
		fg_output = {
			"regge_action": regge_action,
			"total_deficit": total_deficit,
			"hinge_count": hinge_count,
			"topology": topology,
			"field_strength": fg_field_strength,
			"source": "Cartan矩阵→离散Regge几何 (如何连接)"
		}
		var total_energy = spectral_gap * float(Z + N)
		var coupling_energy = spectral_gap * float(N) * 0.5
		var energy_density = total_energy
		var pressure = coupling_energy / 3.0
		var trace_T = energy_density - 3.0 * pressure
		gr_output = {
			"energy_density": energy_density,
			"pressure": pressure,
			"trace_T": trace_T,
			"has_spacetime": true,
			"source": "Cartan矩阵→能动张量T_μν (有多少能量)"
		}
	var stage_II = {
		"description": "退相干II: A4+D铰链网络→FG/GR同时涌现",
		"fg_active": network_satisfied,
		"gr_active": network_satisfied,
		"simultaneous": network_satisfied
	}
	var gamma_phi = spectral_gap * 0.1
	var omega_causal = gamma_phi / max(temperature, 0.01)
	var decoherence = _compute_decoherence_field(gamma_phi, total_deficit, grain_distribution)
	return {
		"fg_output": fg_output,
		"gr_output": gr_output,
		"stage_I": stage_I,
		"stage_II": stage_II,
		"network_satisfied": network_satisfied,
		"Z": Z,
		"N": N,
		"gamma_phi": gamma_phi,
		"omega_causal": omega_causal,
		"decoherence_field": decoherence,
		"grain_distribution": grain_distribution,
		"temperature": temperature,
		"spectral_gap": spectral_gap,
		"has_lattice": bool(chain_result.get("has_lattice", false)),
		"n_neighbors": int(chain_result.get("n_neighbors", 1)),
		"n_formula_units": int(chain_result.get("n_formula_units", 1))
	}

static func compute_superconductivity_condition(field: Dictionary, tc_estimate: float = 0.0) -> Dictionary:
	var gamma_phi = float(field.get("gamma_phi", 0.0))
	var omega_causal = float(field.get("omega_causal", 0.0))
	var decoherence = float(field.get("decoherence_field", 0.0))
	var field_strength = float(field.get("field_strength", 0.0))
	var has_lattice = bool(field.get("has_lattice", false))
	var n_neighbors = int(field.get("n_neighbors", 1))
	var n_formula_units = int(field.get("n_formula_units", 1))
	var lattice_size = n_neighbors * n_formula_units
	var regge_action = float(field.get("regge_action", 0.0))
	var geometry_factor = float(field.get("geometry_factor", 1.0))
	var lattice_coupling_ratio = float(field.get("lattice_coupling_ratio", 1.0))
	var network_satisfied = bool(field.get("network_satisfied", true))
	var N = int(field.get("N", 1))
	var causal_constraint_satisfied = network_satisfied and has_lattice and gamma_phi > 0.05 and omega_causal > 1.0
	var decoherence_sufficient = network_satisfied and has_lattice and decoherence > 0.5 and regge_action > 70.0
	var pairing_condition = network_satisfied and has_lattice and field_strength > 1.0 and causal_constraint_satisfied and geometry_factor > 1.6
	var topology = field.get("topology", "trivial")
	var topology_favorable = network_satisfied and has_lattice and topology != "trivial" and topology != "near_trivial"
	var emergence_score = 0.0
	if causal_constraint_satisfied:
		emergence_score += 0.3
	if decoherence_sufficient:
		emergence_score += 0.3
	if pairing_condition:
		emergence_score += 0.2
	if topology_favorable:
		emergence_score += 0.2
	var lattice_factor = min(float(lattice_size) / 12.0, 1.0)
	var geometry_factor_norm = min(geometry_factor / 2.0, 1.0)
	emergence_score *= lattice_factor * geometry_factor_norm
	if not network_satisfied:
		emergence_score = 0.0
	return {
		"causal_constraint": causal_constraint_satisfied,
		"decoherence_sufficient": decoherence_sufficient,
		"pairing_condition": pairing_condition,
		"topology_favorable": topology_favorable,
		"emergence_score": emergence_score,
		"superconductivity_likely": emergence_score >= 0.6,
		"tc_estimate": tc_estimate,
		"has_lattice": has_lattice,
		"lattice_size": lattice_size,
		"regge_action": regge_action,
		"geometry_factor": geometry_factor,
		"network_satisfied": network_satisfied,
		"neutron_count": N,
		"mechanism": _describe_mechanism(causal_constraint_satisfied, decoherence_sufficient, pairing_condition, topology_favorable, has_lattice, network_satisfied)
	}

static func _compute_causal_decay_rate(regge_action: float, mean_curvature: float) -> float:
	return abs(regge_action) * 0.01 + abs(mean_curvature) * 0.1

static func _compute_causal_frequency(gamma_phi: float, temperature: float) -> float:
	if temperature < 0.01:
		return gamma_phi * 100.0
	return gamma_phi / max(temperature, 0.01)

static func _compute_field_strength(regge_action: float, grain: String) -> float:
	var grain_factor = 1.0
	match grain:
		"single_crystal": grain_factor = 1.0
		"polycrystal": grain_factor = 0.7
		"film": grain_factor = 0.85
		"wire": grain_factor = 0.9
		"powder": grain_factor = 0.5
	return abs(regge_action) * grain_factor

static func _compute_decoherence_field(gamma_phi: float, total_deficit: float, grain: String) -> float:
	var base = gamma_phi * abs(total_deficit)
	var grain_enhancement = 1.0
	match grain:
		"single_crystal": grain_enhancement = 1.2
		"polycrystal": grain_enhancement = 0.8
		"film": grain_enhancement = 1.0
		"wire": grain_enhancement = 1.1
		"powder": grain_enhancement = 0.6
	return base * grain_enhancement

static func _classify_topology(grain: String, total_deficit: float) -> String:
	if abs(total_deficit) < 1e-6:
		return "trivial"
	match grain:
		"single_crystal":
			return "topological" if abs(total_deficit) > 0.1 else "near_trivial"
		"polycrystal":
			return "complex_boundary" if abs(total_deficit) > 0.05 else "near_trivial"
		"film":
			return "topological" if abs(total_deficit) > 0.08 else "near_trivial"
		"wire":
			return "topological" if abs(total_deficit) > 0.08 else "near_trivial"
		"powder":
			return "complex_boundary" if abs(total_deficit) > 0.03 else "near_trivial"
	return "near_trivial"

static func _describe_mechanism(causal: bool, decoh: bool, pairing: bool, topo: bool, has_lattice: bool = true, network_satisfied: bool = true) -> String:
	if not network_satisfied:
		return "网络依赖不满足: 无中子→无A4+D铰链→FG=0,GR=0,无超导 (§5)"
	if not has_lattice:
		return "无晶格结构: 单个分子不具备超导性，需要晶胞分布(L4)信息"
	var parts: Array = []
	if causal:
		parts.append("因果约束(Regge曲率→因果截断)")
	if decoh:
		parts.append("精细引力退相干(质子-中子关系网络→电子)")
	if pairing:
		parts.append("库珀对涌现(因果约束+退相干→配对)")
	if topo:
		parts.append("拓扑保护(非平庸拓扑→稳定超导)")
	if parts.is_empty():
		return "晶格结构存在但条件不满足"
	return " + ".join(parts)