extends RefCounted
class_name PhysicsNotation

# 物理符号专业化显示
# LaTeX风格符号、SI单位、不确定度传播、科学记数法

# === 物理常数 (CODATA 2018) ===
const C = 2.99792458e8          # 光速 (m/s, 精确)
const H = 6.62607015e-34        # 普朗克常数 (J·s, 精确)
const HBAR = 1.054571817e-34    # 约化普朗克常数 (J·s, 精确)
const KB = 1.380649e-23         # 玻尔兹曼常数 (J/K, 精确)
const E = 2.718281828459045     # 自然对数底
const PI_VAL = 3.141592653589793
const EULER_GAMMA = 0.5772156649015329  # 欧拉-马歇罗尼常数
const PHI = 1.6180339887498949  # 黄金比例

# 电子常数
const E_CHARGE = 1.602176634e-19  # 电子电荷 (C, 精确)
const ME = 9.1093837015e-31       # 电子质量 (kg)
const MP = 1.67262192369e-27      # 质子质量 (kg)
const MN = 1.67492749804e-27      # 中子质量 (kg)

# 超导相关常数
const PHI_0 = 2.067833848e-15     # 磁通量子 h/2e (Wb)
const BCS_PREF = 1.1339           # 2e^γ/π
const UNIV_GAP_RATIO = 3.5278     # 2πe^{-γ}
const A4_GAP = 0.38196601125      # (3-√5)/2

# CQM 特有常数
const SPECTRAL_C = 0.02309570897  # 谱量子 ξ'(1)/ξ(1)

# === LaTeX 风格符号 ===

static func symbol_tc() -> String:
	return "T_c"

static func symbol_delta() -> String:
	return "Δ"

static func symbol_lambda() -> String:
	return "λ"

static func symbol_mu_star() -> String:
	return "μ*"

static func symbol_omega_causal() -> String:
	return "ω_causal"

static func symbol_omega_debye() -> String:
	return "ω_D"

static func symbol_psi() -> String:
	return "ψ"

static func symbol_cartan() -> String:
	return "𝒞"

static func symbol_topo() -> String:
	return "𝐹[Top]"

# === SI 单位格式化 ===

## 科学计数法 (GDScript 的 % 运算符不支持 %e, 手动实现)
static func sci(value: float, precision: int = 2) -> String:
	if value == 0.0 or is_nan(value) or is_inf(value):
		return str(value)
	var neg = value < 0.0
	var av = absf(value)
	var exp10 = int(floor(log(av) / log(10.0)))
	var mant = av / pow(10.0, exp10)
	var mant_str = "%.*f" % [precision, mant]
	if abs(float(mant_str)) >= 10.0:
		exp10 += 1
		mant_str = "%.*f" % [precision, av / pow(10.0, exp10)]
	return ("-" if neg else "") + mant_str + "e" + str(exp10)

static func format_temperature(kelvin: float, precision: int = 2) -> String:
	if abs(kelvin) >= 1e6:
		return sci(kelvin, 2) + " K"
	if abs(kelvin) >= 1000:
		return "%.1f K" % kelvin
	if abs(kelvin) >= 1:
		return "%.*f K" % [precision, kelvin]
	if abs(kelvin) >= 0.001:
		return "%.3f K" % kelvin
	return sci(kelvin, 2) + " K"

static func format_pressure(gpa: float, precision: int = 1) -> String:
	if abs(gpa) >= 1000:
		return "%.2f TPa" % (gpa / 1000.0)
	if abs(gpa) >= 1:
		return "%.*f GPa" % [precision, gpa]
	if abs(gpa) >= 0.001:
		return "%.2f MPa" % (gpa * 1000.0)
	return sci(gpa * 1e9, 3) + " Pa"

static func format_magnetic_field(tesla: float, precision: int = 3) -> String:
	if abs(tesla) >= 100:
		return "%.1f T" % tesla
	if abs(tesla) >= 1:
		return "%.*f T" % [precision, tesla]
	if abs(tesla) >= 0.001:
		return "%.3f T" % tesla
	return sci(tesla, 2) + " T"

static func format_energy(ev: float, precision: int = 4) -> String:
	if abs(ev) >= 1000:
		return "%.2f keV" % (ev / 1000.0)
	if abs(ev) >= 1:
		return "%.*f eV" % [precision, ev]
	if abs(ev) >= 0.001:
		return "%.3f meV" % (ev * 1000.0)
	return sci(ev, 2) + " eV"

static func format_length(angstrom: float, precision: int = 3) -> String:
	if abs(angstrom) >= 10000:
		return "%.2f μm" % (angstrom * 1e-4)
	if abs(angstrom) >= 100:
		return "%.2f nm" % (angstrom * 10.0)
	if abs(angstrom) >= 0.01:
		return "%.*f Å" % [precision, angstrom]
	return sci(angstrom, 2) + " Å"

static func format_frequency(hz: float, precision: int = 3) -> String:
	if abs(hz) >= 1e15:
		return "%.3f PHz" % (hz * 1e-15)
	if abs(hz) >= 1e12:
		return "%.3f THz" % (hz * 1e-12)
	if abs(hz) >= 1e9:
		return "%.3f GHz" % (hz * 1e-9)
	if abs(hz) >= 1e6:
		return "%.3f MHz" % (hz * 1e-6)
	if abs(hz) >= 1e3:
		return "%.3f kHz" % (hz * 1e-3)
	return "%.*f Hz" % [precision, hz]

static func format_coupling(value: float, precision: int = 4) -> String:
	return "%.*f" % [precision, value]

# === 不确定度传播 ===

static func _log10(x: float) -> float:
	return log(x) / log(10.0)

static func format_with_uncertainty(value: float, uncertainty: float, unit: String = "", precision: int = 2) -> String:
	if uncertainty <= 0:
		return "%.*f %s" % [precision, value, unit]
	var digits = max(0, int(-_log10(uncertainty)) + 1)
	digits = min(digits, 6)
	var fmt = "%%.%df" % digits
	var v_str = fmt % value
	var u_str = fmt % uncertainty
	if unit.is_empty():
		return "%s ± %s" % [v_str, u_str]
	return "(%s ± %s) %s" % [v_str, u_str, unit]

static func propagate_add(a: float, da: float, b: float, db: float) -> Dictionary:
	return {"value": a + b, "uncertainty": sqrt(da * da + db * db)}

static func propagate_mul(a: float, da: float, b: float, db: float) -> Dictionary:
	var val = a * b
	var unc = abs(val) * sqrt((da / a) ** 2 + (db / b) ** 2) if a != 0 and b != 0 else 0.0
	return {"value": val, "uncertainty": unc}

static func propagate_div(a: float, da: float, b: float, db: float) -> Dictionary:
	var val = a / b if b != 0 else 0.0
	var unc = abs(val) * sqrt((da / a) ** 2 + (db / b) ** 2) if a != 0 and b != 0 else 0.0
	return {"value": val, "uncertainty": unc}

static func propagate_pow(base: float, dbase: float, exponent: float) -> Dictionary:
	var val = pow(base, exponent)
	var unc = abs(exponent * val * dbase / base) if base != 0 else 0.0
	return {"value": val, "uncertainty": unc}

# === 科学记数法 ===

static func format_scientific(value: float, precision: int = 4) -> String:
	if value == 0:
		return "0"
	var exp10 = int(_log10(abs(value)))
	var mantissa = value / pow(10, exp10)
	if exp10 == 0:
		return "%.*f" % [precision, mantissa]
	return "%.*f×10^%d" % [precision, mantissa, exp10]

static func format_scientific_unicode(value: float, precision: int = 4) -> String:
	if value == 0:
		return "0"
	var exp10 = int(_log10(abs(value)))
	var mantissa = value / pow(10, exp10)
	if exp10 == 0:
		return "%.*f" % [precision, mantissa]
	var exp_str = str(exp10)
	var superscript = ""
	for ch in exp_str:
		match ch:
			"0": superscript += "⁰"
			"1": superscript += "¹"
			"2": superscript += "²"
			"3": superscript += "³"
			"4": superscript += "⁴"
			"5": superscript += "⁵"
			"6": superscript += "⁶"
			"7": superscript += "⁷"
			"8": superscript += "⁸"
			"9": superscript += "⁹"
			"-": superscript += "⁻"
	return "%.*f×10%s" % [precision, mantissa, superscript]

# === 物理量格式化 ===

static func format_tc(tc: float, confidence: float = 0.0) -> String:
	if tc <= 0:
		return "T_c = 0 (非超导)"
	var unc = tc * (1.0 - confidence) if confidence > 0 else 0.0
	if unc > 0:
		return "T_c = %s" % format_with_uncertainty(tc, unc, "K", 1)
	return "T_c = %.2f K" % tc

static func format_gap(delta: float, tc: float = 0.0) -> String:
	if delta <= 0:
		return "Δ₀ = 0"
	var mev = delta * 1000.0 / E_CHARGE
	if tc > 0:
		var ratio = 2.0 * delta / (KB * tc)
		return "Δ₀ = %.4f meV  (2Δ₀/k_BT_c = %.3f, BCS: %.3f)" % [mev, ratio, UNIV_GAP_RATIO]
	return "Δ₀ = %.4f meV" % mev

static func format_hc(hc: float, hc_type: String = "Hc") -> String:
	if hc <= 0:
		return "%s = 0" % hc_type
	return "%s = %s" % [hc_type, format_magnetic_field(hc)]

static func format_penetration_depth(lambda_l: float) -> String:
	if lambda_l <= 0:
		return "λ_L = ∞"
	return "λ_L = %.1f nm" % (lambda_l * 1e9)

static func format_coherence_length(xi: float) -> String:
	if xi <= 0:
		return "ξ = 0"
	return "ξ = %.1f nm" % (xi * 1e9)

static func format_ginzburg_landau(kappa: float) -> String:
	if kappa <= 0:
		return "κ = —"
	var sc_type = "II型" if kappa > 1.0 / sqrt(2.0) else "I型"
	return "κ = %.3f (%s超导体)" % [kappa, sc_type]

static func format_coupling_constant(lambda_val: float, mu_star: float = 0.0) -> String:
	var regime = "弱耦合"
	if lambda_val > 1.5:
		regime = "强耦合"
	elif lambda_val > 0.5:
		regime = "中等耦合"
	return "λ = %.4f, μ* = %.4f (%s)" % [lambda_val, mu_star, regime]

static func format_eigenvalues(eigenvalues: Array) -> String:
	if eigenvalues.is_empty():
		return "—"
	var parts: Array = []
	for i in range(min(eigenvalues.size(), 4)):
		parts.append("%.4f" % float(eigenvalues[i]))
	if eigenvalues.size() > 4:
		parts.append("...")
	return "[" + ", ".join(parts) + "]"

static func format_spectral_gap(gap: float) -> String:
	if gap <= 0:
		return "λ₁ = 0 (无谱间隙)"
	var ratio = gap / A4_GAP
	return "λ₁ = %.6f  (λ₁/λ₁(A₄) = %.4f)" % [gap, ratio]

static func format_verdict(verdict: String, tc: float, confidence: float) -> String:
	var icon = ""
	var color_tag = ""
	match verdict:
		"superconducting":
			icon = "✓"
			color_tag = "[color=green]"
		"borderline":
			icon = "≈"
			color_tag = "[color=yellow]"
		"normal":
			icon = "✗"
			color_tag = "[color=red]"
		"insufficient":
			icon = "?"
			color_tag = "[color=gray]"
		_:
			icon = "?"
	return "%s %s判定: Tc=%.1fK, 置信度=%.0f%%" % [icon, color_tag, tc, confidence * 100]

# === CQM 理论专用格式化 ===

static func format_causal_cutoff(omega: float) -> String:
	var t_causal = HBAR * omega / KB
	return "ω_causal = %s  (T_causal = %s K)" % [format_frequency(omega), sci(t_causal, 2)]

static func format_emergence_integral(psi: float, components: Dictionary = {}) -> String:
	var result = "ψ = " + sci(psi, 6)
	if not components.is_empty():
		result += "\n  D_lattice = %.4f" % components.get("D_lattice", 0)
		result += "\n  P_electron = %.4f" % components.get("P_electron", 0)
		result += "\n  C_triple = %.4f" % components.get("C_triple", 0)
		result += "\n  K_causal = %.4f" % components.get("K_causal", 0)
		result += "\n  F_topo = %.4f" % components.get("F_topo", 1.0)
	return result

static func format_bcs_degradation(path: Dictionary) -> String:
	var result = "BCS退化路径:\n"
	result += "  CQM完整:     Tc = %.2f K\n" % path.get("cqm_full", 0)
	result += "  CQM一阶:     Tc = %.2f K\n" % path.get("cqm_first_order", 0)
	result += "  标准BCS:     Tc = %.2f K\n" % path.get("bcs_standard", 0)
	var deviation = 0.0
	if path.has("cqm_full") and path.has("bcs_standard") and path["bcs_standard"] > 0:
		deviation = (path["cqm_full"] - path["bcs_standard"]) / path["bcs_standard"] * 100.0
	result += "  CQM偏离BCS: %.1f%%" % deviation
	return result

static func format_pairing_symmetry(symmetry: int) -> String:
	match symmetry:
		0: return "s波 (全对称, 无节点)"
		1: return "d波 (x²-y², 四节点)"
		2: return "p波 (三重态, 拓扑)"
		3: return "扩展s波 (s±, 无节点但变号)"
		_: return "未知配对对称性"

# === 单位转换 ===

static func ev_to_kelvin(ev: float) -> float:
	return ev * E_CHARGE / KB

static func kelvin_to_ev(k: float) -> float:
	return k * KB / E_CHARGE

static func ev_to_joule(ev: float) -> float:
	return ev * E_CHARGE

static func joule_to_ev(j: float) -> float:
	return j / E_CHARGE

static func angstrom_to_meter(a: float) -> float:
	return a * 1e-10

static func meter_to_angstrom(m: float) -> float:
	return m * 1e10

static func gpa_to_pa(gpa: float) -> float:
	return gpa * 1e9

static func pa_to_gpa(pa: float) -> float:
	return pa * 1e-9
# === 学术公式与富文本排版 ===

## Allen–Dynes (1975) 完整 Tc 公式 (展示用)
const FORMULA_ALLEN_DYNES := "Tc = f₁·f₂·(ω_log/1.2)·exp[−1.04(1+λ)/(λ−μ*(1+0.62λ))]"
## BCS 弱耦合能隙通用比
const FORMULA_GAP_RATIO := "2Δ₀/kBTc = 3.53 (BCS弱耦合)"
## Hopfield/McMillan λ 形式
const FORMULA_LAMBDA_HOPFIELD := "λ = N(0)⟨I²⟩/(M⟨ω²⟩)"

## 通用数值格式化 (自动有效数字, 避免 Godot 对 <1e-10 浮点打印为 0 的问题)
static func format_number(v: float, sig: int = 3) -> String:
	if is_nan(v):
		return "—"
	if v == 0.0:
		return "0"
	var mag = absf(v)
	if mag >= 1e5 or mag < 1e-3:
		# 科学计数法 (Godot %e 不支持, 手动构造)
		var exp10 = int(floor(log(mag) / log(10.0)))
		var mant = v / pow(10.0, exp10)
		return "%.*f×10^%d" % [sig - 1, mant, exp10]
	var decimals = maxi(0, sig - 1 - int(floor(log(mag) / log(10.0))))
	return "%.*f" % [decimals, v]

## 下标化: "T_c" → "T꜀"(可用则Unicode下标), 数字下标一律可用
## Unicode 下标字母仅限 ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ; 其余字母(如 c, D)回退为普通小写
static func unicode_subscript(text: String) -> String:
	const SUB_LETTERS := {"a":"ₐ","e":"ₑ","h":"ₕ","i":"ᵢ","j":"ⱼ","k":"ₖ","l":"ₗ",
		"m":"ₘ","n":"ₙ","o":"ₒ","p":"ₚ","r":"ᵣ","s":"ₛ","t":"ₜ","u":"ᵤ","v":"ᵥ","x":"ₓ"}
	const SUB_DIGITS := {"0":"₀","1":"₁","2":"₂","3":"₃","4":"₄","5":"₅","6":"₆","7":"₇","8":"₈","9":"₉"}
	var out := ""
	var i := 0
	while i < text.length():
		var c := text[i]
		if c == "_" and i + 1 < text.length():
			var j = i + 1
			var sub := ""
			while j < text.length():
				var ch = text[j]
				if SUB_LETTERS.has(ch):
					sub += SUB_LETTERS[ch]
				elif SUB_DIGITS.has(ch):
					sub += SUB_DIGITS[ch]
				elif ch == ch.to_lower() and (ch.is_valid_identifier() or ch == "*"):
					sub += ch  # 无 Unicode 下标, 保留原字符
				else:
					break
				j += 1
			if sub != "":
				out += sub
				i = j
				continue
		out += c
		i += 1
	return out

## BBCode 富文本: "T_c" → "T[sub]c[/sub]", "^-3"/"^{ab}" → "[sup]...[/sup]"
## 用于 RichTextLabel (bbcode_enabled)
static func rich(text: String) -> String:
	var out := text
	# 上标 ^{...} (花括号形式, 最长优先)
	var re_brace := RegEx.new()
	re_brace.compile("\\^\\{([^}]+)\\}")
	out = re_brace.sub(out, "[sup]$1[/sup]", true)
	# 上标 ^-3 / ^12 (裸记号)
	var re_sup := RegEx.new()
	re_sup.compile("\\^(-?[0-9]+)")
	out = re_sup.sub(out, "[sup]$1[/sup]", true)
	# 下标 (跳过已处理的 BBCode 标签内容里的下划线不存在, 安全)
	var re_sub := RegEx.new()
	re_sub.compile("_([A-Za-z0-9*]+)")
	out = re_sub.sub(out, "[sub]$1[/sub]", true)
	return out
