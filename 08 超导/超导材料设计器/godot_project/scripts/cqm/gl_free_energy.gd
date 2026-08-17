extends RefCounted
class_name CQMGLFreeEnergy

# CQM 非平庸Ginzburg-Landau自由能 — §10.2
# A4根系张量GL自由能:
# F_GL = Σ_{αβ}[ α_{αβ}|T_{αβ}|² + β_{αβ}/2|T_{αβ}|⁴ + 1/(2m*_{αβ})|(-iℏ∇-2eA)T_{αβ}|² ] + F_cubic[T]
#
# F_cubic[T]: 立方项, 允许一阶相变(非平庸GL理论)
# 16复分量 = 32实自由度, 各分量可独立凝聚
#
# 平庸极限: F_cubic→0, 退化为标准GL(二阶相变)

const HBAR = 1.055e-34
const ELECTRON_CHARGE = 1.602e-19

static func compute(order_parameters: Array, temperature: float, tc: float,
					vector_potential: Vector3 = Vector3.ZERO,
					include_cubic: bool = true) -> Dictionary:
	if order_parameters.is_empty() or tc <= 0:
		return {"F_GL": 0.0, "F_quadratic": 0.0, "F_quartic": 0.0, "F_gradient": 0.0, "F_cubic": 0.0}

	var F_quad = 0.0
	var F_quart = 0.0
	var F_grad = 0.0
	var F_cubic = 0.0

	for param in order_parameters:
		var amplitude = float(param.get("amplitude", 0.0))
		var channel = int(param.get("channel", 1))
		var alpha = _alpha_coefficient(channel, temperature, tc)
		var beta = _beta_coefficient(channel)
		var m_star = _effective_mass(channel)

		var abs_sq = amplitude * amplitude
		F_quad += alpha * abs_sq
		F_quart += 0.5 * beta * abs_sq * abs_sq

		var grad_term = _gradient_term(amplitude, vector_potential, m_star)
		F_grad += grad_term

	if include_cubic and order_parameters.size() >= 3:
		F_cubic = _cubic_term(order_parameters)

	var F_total = F_quad + F_quart + F_grad + F_cubic

	return {
		"F_GL": F_total,
		"F_quadratic": F_quad,
		"F_quartic": F_quart,
		"F_gradient": F_grad,
		"F_cubic": F_cubic,
		"has_cubic": include_cubic and F_cubic != 0.0,
		"transition_order": "first" if abs(F_cubic) > 0.01 * abs(F_quart) else "second"
	}

static func _alpha_coefficient(channel: int, temperature: float, tc: float) -> float:
	var tc_channel = tc * sqrt(float(channel) / 4.0)
	return (temperature - tc_channel) / tc_channel if tc_channel > 0 else 1.0

static func _beta_coefficient(channel: int) -> float:
	return 1.0 + 0.1 * float(channel)

static func _effective_mass(channel: int) -> float:
	return 1.0 + 0.2 * float(channel)

static func _gradient_term(amplitude: float, A: Vector3, m_star: float) -> float:
	var A_sq = A.length_squared()
	var hbar_sq = HBAR * HBAR
	var _e = ELECTRON_CHARGE
	return hbar_sq * A_sq * amplitude * amplitude / (2.0 * m_star)

static func _cubic_term(order_parameters: Array) -> float:
	if order_parameters.size() < 3:
		return 0.0
	var a1 = float(order_parameters[0].get("amplitude", 0.0))
	var a2 = float(order_parameters[1].get("amplitude", 0.0))
	var a3 = float(order_parameters[2].get("amplitude", 0.0))
	var gamma = 0.1
	return gamma * (a1 * a2 * a3 + a1 * a1 * a2 - a2 * a2 * a3)

static func phase_transition_type(temperature: float, tc: float,
								   order_parameters: Array) -> String:
	var gl = compute(order_parameters, temperature, tc)
	return gl.transition_order

static func meissner_screening(order_parameters: Array, tc: float,
							   temperature: float) -> Dictionary:
	if order_parameters.is_empty() or tc <= 0 or temperature >= tc:
		return {"lambda_L": 0.0, "screening": false}

	var sum_abs_sq = 0.0
	for param in order_parameters:
		var amp = float(param.get("amplitude", 0.0))
		sum_abs_sq += amp * amp

	if sum_abs_sq <= 0:
		return {"lambda_L": 0.0, "screening": false}

	var n_s = sum_abs_sq
	var mu_0 = 1.257e-6
	var m_e = 9.109e-31
	var e = ELECTRON_CHARGE
	var lambda_L = sqrt(m_e / (mu_0 * n_s * e * e))

	return {
		"lambda_L": lambda_L,
		"screening": true,
		"n_s": n_s,
		"topology_enhanced": true
	}

static func bcs_degradation(order_parameters: Array, temperature: float, tc: float) -> Dictionary:
	return compute(order_parameters, temperature, tc, Vector3.ZERO, false)