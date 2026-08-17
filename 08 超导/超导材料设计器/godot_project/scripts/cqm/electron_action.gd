extends RefCounted
class_name CQMElectronAction

# CQM 电子作用量 S_electron — §3.4
# S = S_kin[ψ_e; R] + S_braid[ψ_e, T; Γ, R] + S_mag[ψ_e; B]
#
# S_kin   : 动能项, Σ_<ij> tr(ψ̄_e^i ∘ (iD_t - H_kin[R]) ∘ ψ_e^j)
# S_braid : 编织耦合项(核心), Σ_T tr(T_T ∘ B̂[Γ_T,R_T] ∘ (ψ_e⊗ψ_e)_T)
# S_mag   : 磁场耦合项, Σ_i tr(ψ̄_e^i ∘ (σ·B_i) ∘ ψ_e^i)
#
# 电子是历史性封装物: ψ_e^i(τ) = ∫dτ' K_e(τ-τ') · B̂[Γ(τ'),R_pn(τ')] · Φ_proton^i(τ')
# K_e(Δτ) = exp(-Δτ/τ_e)·Θ(Δτ)  电子形成记忆核

const HBAR = 1.055e-34
const ELECTRON_CHARGE = 1.602e-19
const ELECTRON_MASS = 9.109e-31

static func compute(electron_states: Array, causal_tensor: Array,
					cartan_matrix: Array, relation_network: Array,
					magnetic_field: Vector3 = Vector3.ZERO) -> Dictionary:
	var s_kin = _kinetic_term(electron_states, relation_network)
	var s_braid = _braid_term(electron_states, causal_tensor, cartan_matrix, relation_network)
	var s_mag = _magnetic_term(electron_states, magnetic_field)
	var s_total = s_kin + s_braid + s_mag
	return {
		"S_electron": s_total,
		"S_kin": s_kin,
		"S_braid": s_braid,
		"S_mag": s_mag
	}

static func _kinetic_term(electron_states: Array, relation_network: Array) -> float:
	if electron_states.is_empty():
		return 0.0
	var total = 0.0
	for i in range(electron_states.size()):
		var psi = electron_states[i]
		var norm_sq = _spinor_norm_squared(psi)
		var hop = _hopping_amplitude(i, relation_network)
		total += norm_sq * hop
	return total

static func _braid_term(electron_states: Array, causal_tensor: Array,
						cartan_matrix: Array, relation_network: Array) -> float:
	if electron_states.size() < 2 or causal_tensor.is_empty():
		return 0.0
	var braid = CQMBraidOperator.evaluate(cartan_matrix, relation_network)
	var total = 0.0
	for i in range(min(causal_tensor.size(), braid.size())):
		var T_T = causal_tensor[i]
		var psi_pair = _form_pair(electron_states, i)
		if psi_pair.is_empty():
			continue
		var braid_coupled = CQMBraidOperator.compute_braid_coupling(braid, [], psi_pair)
		for val in braid_coupled:
			total += float(val) * _tensor_trace(T_T)
	return total

static func _magnetic_term(electron_states: Array, magnetic_field: Vector3) -> float:
	if electron_states.is_empty() or magnetic_field.length() < 1e-10:
		return 0.0
	var b_mag = magnetic_field.length()
	var total = 0.0
	for psi in electron_states:
		total += _spinor_norm_squared(psi) * b_mag
	return total * ELECTRON_CHARGE * HBAR / (2.0 * ELECTRON_MASS)

static func _spinor_norm_squared(psi) -> float:
	if psi is Array:
		var sum = 0.0
		for val in psi:
			sum += float(val) * float(val)
		return sum
	return float(psi) * float(psi)

static func _hopping_amplitude(_i: int, _relation_network: Array) -> float:
	return 1.0

static func _form_pair(electron_states: Array, idx: int) -> Array:
	var result: Array = []
	var n = electron_states.size()
	if n < 2:
		return result
	var i = idx % n
	var j = (idx + 1) % n
	result.append(_spinor_norm_squared(electron_states[i]))
	result.append(_spinor_norm_squared(electron_states[j]))
	return result

static func _tensor_trace(tensor) -> float:
	if tensor is Array:
		var trace = 0.0
		for i in range(tensor.size()):
			if tensor[i] is Array and i < tensor[i].size():
				trace += float(tensor[i][i])
			elif i == 0:
				trace += float(tensor[i])
		return trace
	return float(tensor)

static func historical_emergence(proton_states: Array, cartan_matrix: Array,
								  relation_network: Array, tau: float,
								  tau_e: float = 1e-15) -> Array:
	if proton_states.is_empty():
		return []
	var memory_kernel = exp(-tau / tau_e) if tau > 0 else 0.0
	var braid = CQMBraidOperator.evaluate(cartan_matrix, relation_network)
	var psi_e: Array = []
	for phi_p in proton_states:
		var psi = memory_kernel * _tensor_trace(braid) * float(phi_p)
		psi_e.append(psi)
	return psi_e

static func bcs_degradation() -> Dictionary:
	return {"S_electron": 0.0, "S_braid": 0.0, "S_mag": 0.0}