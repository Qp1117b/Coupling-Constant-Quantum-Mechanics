extends RefCounted
class_name CQMElectronAction

# CQM 电子作用量 S_electron — §5(精细引力纤维丛涌现激发)
# S = S_kin[ψ_e; R] + S_mag[ψ_e; B]
#
# S_kin : 动能项, Σ_<ij> tr(ψ̄_e^i ∘ (iD_t - H_kin[R]) ∘ ψ_e^j)
# S_mag : 磁场耦合项, Σ_i tr(ψ̄_e^i ∘ (σ·B_i) ∘ ψ_e^i)
#
# 注: 配对通道由耦合空间曲率机制 (§7-9) 给出:
#     Regge 角亏 δ_v → 固有时流速 dτ/dt = 1+βδ_v → 耦合动量 p_u → Δu≥ln4
#     相关代码见 lean:Superconductivity.CouplingSpace。
#
# 电子是FG纤维丛涌现激发: ψ_e^i(τ) = ∫dτ' K_e(τ-τ') · Φ_proton^i(τ')
# K_e(Δτ) = exp(-Δτ/τ_e)·Θ(Δτ)  电子形成记忆核

const HBAR = 1.055e-34
const ELECTRON_CHARGE = 1.602e-19
const ELECTRON_MASS = 9.109e-31

static func compute(electron_states: Array, causal_tensor: Array,
					cartan_matrix: Array, relation_network: Array,
					magnetic_field: Vector3 = Vector3.ZERO) -> Dictionary:
	var s_kin = _kinetic_term(electron_states, relation_network)
	var s_mag = _magnetic_term(electron_states, magnetic_field)
	var s_total = s_kin + s_mag
	return {
		"S_electron": s_total,
		"S_kin": s_kin,
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

static func _magnetic_term(electron_states: Array, magnetic_field: Vector3) -> float:
	if electron_states.is_empty() or magnetic_field.length() < 1e-10:
		return 0.0
	var b_mag = magnetic_field.length()
	var total = 0.0
	for psi in electron_states:
		total += _spinor_norm_squared(psi) * b_mag
	return total * ELECTRON_CHARGE * HBAR / (2.0 * ELECTRON_MASS)

static func _hopping_amplitude(i: int, relation_network: Array) -> float:
	if relation_network.is_empty():
		return 1.0
	if i >= relation_network.size():
		return 1.0
	var row = relation_network[i]
	if row is Array:
		var total = 0.0
		for val in row:
			total += absf(float(val))
		return total / float(row.size()) if row.size() > 0 else 1.0
	return 1.0

static func _spinor_norm_squared(psi) -> float:
	if psi is Array:
		var sum = 0.0
		for val in psi:
			sum += float(val) * float(val)
		return sum
	return float(psi) * float(psi)

static func historical_emergence(proton_states: Array, cartan_matrix: Array,
								  relation_network: Array, tau: float,
								  tau_e: float = 1e-15) -> Array:
	# 电子由质子态经记忆核 K_e(Δτ) 形成;
	# 配对/超导判据由 §7-9 耦合空间曲率机制 (Superconductivity.CouplingSpace) 给出。
	if proton_states.is_empty():
		return []
	var memory_kernel = exp(-tau / tau_e) if tau > 0 else 0.0
	var psi_e: Array = []
	for phi_p in proton_states:
		var psi = memory_kernel * float(phi_p)
		psi_e.append(psi)
	return psi_e

static func bcs_degradation() -> Dictionary:
	return {"S_electron": 0.0, "S_kin": 0.0, "S_mag": 0.0}