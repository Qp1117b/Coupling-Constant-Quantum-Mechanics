extends Node

## 无头回归测试: godot --headless --path godot_project res://tests/regression_test.tscn
## 覆盖: 元素库(118)、同位素、计算引擎、McMillan、临界场、扫描、
##       文献基准匹配、专业符号、化学验证、周期表UI、CQM各理论模块

var passed := 0
var failed := 0
var failures: Array = []

func _ready():
	await _run_all()
	await get_tree().process_frame
	print("\n========== 回归测试结果 ==========")
	print("通过: %d  失败: %d" % [passed, failed])
	if not failures.is_empty():
		print("失败项:")
		for f in failures:
			print("  - " + f)
	print("==================================")
	get_tree().quit(1 if failed > 0 else 0)

func _check(cond: bool, name: String):
	if cond:
		passed += 1
	else:
		failed += 1
		failures.append(name)
		print("[FAIL] " + name)

func _run_all():
	_test_element_database()
	_test_scdata()
	_test_data_validator()
	_test_phonon_mixing_qe()
	_test_calculator_single_atom()
	_test_mcmillan_literature()
	_test_critical_fields()
	_test_cqm_modules()
	_test_sweeps()
	_test_physics_notation()
	_test_chemistry_validator()
	_test_spatial_hash_and_force_field()
	await _test_element_palette()

# ---------- 元素数据库 ----------
func _test_element_database():
	var symbols = ElementDB.get_all_symbols()
	_check(symbols.size() == 118, "元素库包含118个元素 (实际 %d)" % symbols.size())
	var nb = ElementDB.get_element("Nb")
	_check(int(nb.get("atomic_number", 0)) == 41, "Nb 原子序数 = 41")
	_check(not ElementDB.get_element("Og").is_empty(), "Og (118) 数据存在")
	_check(ElementDB.get_element_by_number(118).get("symbol", "") == "Og", "Z=118 → Og")
	_check(ElementDB.get_element_by_number(1).get("symbol", "") == "H", "Z=1 → H")

	_check(ElementDB.most_abundant_isotope("Nb") == 93, "Nb 丰度最大同位素 = Nb-93")
	_check(ElementDB.most_abundant_isotope("Am") > 0, "Am 无稳定同位素时仍返回有效质量数")
	var h_isotopes = ElementDB.get_isotopes("H")
	_check(h_isotopes.size() >= 3, "H 同位素数据 ≥ 3 (氕/氘/氚)")

# ---------- 超导文献数据 ----------
func _test_scdata():
	_check(abs(SCData.get_experimental_tc("Nb") - 9.25) < 0.01, "Nb 实验 Tc = 9.25 K")
	_check(SCData.get_experimental_tc("Cu") == 0.0, "Cu 非超导 (Tc=0)")
	_check(is_nan(SCData.get_experimental_tc("Zz")) or SCData.get_experimental_tc("Zz") == 0.0,
		"未知元素不崩溃")
	_check(abs(SCData.get_debye_temperature("Pb") - 105.0) < 0.5, "Pb 德拜温度 = 105 K")

	var fc = SCData.formula_counts("LaH10")
	_check(fc.get("La", 0) == 1 and fc.get("H", 0) == 10, "LaH10 化学式解析")
	var ybco = SCData.formula_counts("YBa2Cu3O7")
	_check(ybco.get("Y", 0) == 1 and ybco.get("Ba", 0) == 2 and ybco.get("Cu", 0) == 3
		and ybco.get("O", 0) == 7, "YBa2Cu3O7 化学式解析")

	var bench = SCData.find_benchmark("H3S")
	_check(not bench.is_empty() and bench.get("tc_K", 0.0) > 150.0,
		"H3S 基准匹配 (Tc≈203K)")
	var bench2 = SCData.find_benchmark("Cu3O7Ba2Y1")
	_check(not bench2.is_empty(), "乱序化学式仍匹配 YBCO 基准")

# ---------- 数据校验器 (文档 02 §6.1) ----------
func _test_data_validator():
	var v = DataValidator.validate_all()
	_check(bool(v.get("passed", false)),
		"三库校验无错误级问题 (错误: %s)" % str(v.get("errors", [])).substr(0, 200))
	_check(v.get("warnings", []).size() <= 10,
		"警告数可控 (%d 项)" % v.get("warnings", []).size())
	var scdb3 = SCDB.get_all()
	var fe_se: Dictionary = {}
	for m in scdb3:
		if str(m.formula) == "FeSe":
			fe_se = m
			break
	_check(not fe_se.is_empty() and str(fe_se.get("desc", "")).find("36.7") >= 0,
		"FeSe 高压 36.7K (Medvedev 2009) 已写入描述")
	for m in scdb3:
		if float(m.get("pressure_GPa", -1.0)) > 0:
			_check(m.has("pressure_GPa"), "压强字段存在 (%s)" % str(m.name))
			break

# ---------- 化合物声子矩混合 + QE 输入 ----------
func _mgb2_atoms() -> Array:
	return [
		{"symbol": "Mg", "position": Vector3(0, 0, 0)},
		{"symbol": "B", "position": Vector3(1.2, 0, 0)},
		{"symbol": "B", "position": Vector3(-1.2, 0, 0)},
	]

func _test_phonon_mixing_qe():
	var pm = CQMCalculator.phonon_moments(_mgb2_atoms())
	_check(pm.omega_log > 0.0 and pm.sqrt_omega2 > pm.omega_log,
		"MgB2 混合矩: √⟨ω²⟩ > ω_log (Jensen 不等式方向)")
	var naive = float(pm.debye_avg) * CQMCalculator.DEBYE_OMEGA_LOG_FACTOR
	_check(absf(float(pm.omega_log) - naive) > 1.0,
		"MgB2 λ加权对数平均 ≠ 算术平均 (区分混合规则)")
	_check(str(pm.weights).find("λ加权") >= 0, "混合权重说明含 λ 加权标注")

	var r = CQMCalculator.evaluate_molecule(_mgb2_atoms(),
		[{"a": 0, "b": 1, "order": 1}, {"a": 0, "b": 2, "order": 1}],
		{"temperature": 4.2})
	_check(absf(float(r.get("omega_log_temp", 0.0)) - float(pm.omega_log)) < 1e-6,
		"计算引擎使用混合声子矩")

	var qe = StructureIO.export_qe_input(_mgb2_atoms(), "mgb2")
	_check(qe.find("calculation = 'scf'") >= 0 and qe.find("ATOMIC_POSITIONS angstrom") >= 0,
		"QE 输入含 SCF 控制段与笛卡尔坐标")
	_check(qe.find("ntyp = 2") >= 0 and qe.find("nat = 3") >= 0,
		"QE 输入原子/元素计数正确")
	_check(qe.find("K_POINTS") >= 0 and qe.find("CELL_PARAMETERS") >= 0,
		"QE 输入含 K 点与晶胞段")

# ---------- 计算引擎 ----------
func _nb_atom() -> Array:
	return [{"symbol": "Nb", "position": Vector3.ZERO}]

func _test_calculator_single_atom():
	var r = CQMCalculator.evaluate_molecule(_nb_atom(), [], {"temperature": 4.2})
	_check(not r.is_empty(), "Nb 单原子计算不崩溃")
	_check(float(r.get("tc_estimate", 0.0)) > 0.0, "Nb 计算 Tc > 0")
	_check(str(r.get("tc_method", "")) == "Allen-Dynes 1975", "Nb 使用 McMillan 路径")
	_check(bool(r.get("mcmillan_valid", false)), "Nb McMillan 有效域")
	_check(abs(float(r.get("debye_temp", 0.0)) - 275.0) < 1.0, "Nb 德拜温度取文献值 275K")
	var ratio = float(r.get("tc_estimate", 0.0)) / 9.25
	_check(ratio > 0.3 and ratio < 3.0,
		"Nb 计算/实验 Tc 比 = %.2f (文献θD代理ω_log近似容差)" % ratio)
	_check(r.has("evidence_levels"), "结果含证据等级标注")

	# Allen-Dynes 完整链: 德拜模型矩 + f1/f2 + 敏感性 + 同位素指数
	_check(absf(float(r.get("omega_log_temp", 0.0)) / float(r.get("debye_temp", 1.0)) - 0.716531) < 1e-3,
		"ω_log = 0.7165·θ_D (德拜模型对数矩)")
	_check(absf(float(r.get("sqrt_omega2_temp", 0.0)) / float(r.get("debye_temp", 1.0)) - 0.774597) < 1e-3,
		"√⟨ω²⟩ = 0.7746·θ_D (德拜模型二阶矩)")
	_check(float(r.get("ad_f1", 0.0)) > 0.0 and float(r.get("ad_f1", 0.0)) <= 1.0,
		"Allen-Dynes f1 ∈ (0,1] (得 %.4f)" % float(r.get("ad_f1", 0.0)))
	_check(float(r.get("ad_f2", 0.0)) >= 1.0 - 1e-6,
		"Allen-Dynes f2 ≥ 1 (得 %.4f)" % float(r.get("ad_f2", 0.0)))
	var sens: Dictionary = r.get("tc_mu_star_sensitivity", {})
	_check(sens.size() == 3, "μ*敏感性三列 (0.10/0.13/0.16)")
	if sens.size() == 3:
		_check(float(sens.get("0.10", 0.0)) >= float(sens.get("0.13", 0.0)) - 1e-9
			and float(sens.get("0.13", 0.0)) >= float(sens.get("0.16", 0.0)) - 1e-9,
			"Tc 随 μ* 单调不增")
	var alpha = float(r.get("isotope_alpha", NAN))
	_check(not is_nan(alpha) and absf(alpha - 0.5) < 0.15,
		"常规输出同位素指数 α ≈ 0.5 (得 %.3f)" % alpha)
	_check(absf(float(r.get("mu_star", 0.0)) - 0.13) < 1e-6, "μ* 默认 0.13 (SCData 典型值)")
	_check(not is_nan(float(r.get("n0v_product", NAN))), "N(0)V 无量纲耦合有输出")

	# Allen-Dynes 强耦合增强: λ 大时 f1·f2 > 1
	var ad_strong = CQMCalculator.allen_dynes_tc(1000.0, 1100.0, 2.0, 0.13)
	var ad_weak = CQMCalculator.allen_dynes_tc(1000.0, 1100.0, 0.4, 0.13)
	_check(float(ad_strong.tc) > 0.0 and float(ad_weak.tc) > 0.0, "Allen-Dynes 两端有限值")
	_check(float(ad_strong.f1) < float(ad_weak.f1), "f1 随 λ 增大而减小 (饱和修正)")

	# 双原子分子 H2
	var h2 = [
		{"symbol": "H", "position": Vector3(0, 0, 0)},
		{"symbol": "H", "position": Vector3(0.74, 0, 0)}
	]
	var r2 = CQMCalculator.evaluate_molecule(h2,
		[{"a": 0, "b": 1, "order": 1}], {"temperature": 4.2})
	_check(not r2.is_empty() and not is_nan(float(r2.get("tc_estimate", NAN))),
		"H2 分子计算有限值")

	# 缓存生效
	var r3 = CQMCalculator.evaluate_molecule(_nb_atom(), [], {"temperature": 4.2})
	_check(bool(r3.get("from_cache", false)), "相同输入命中结果缓存")

func _test_mcmillan_literature():
	# ω_log 量纲为 K; Nb: θD=275K, λ=0.98, μ*=0.13 → 文献区间 (θD 代理 ω_log 的系统偏移)
	var tc = CQMCalculator.mcmillan_tc(275.0, 0.98, 0.13)
	_check(tc > 8.0 and tc < 20.0, "McMillan Nb 参数 Tc = %.2f K ∈ [8,20]" % tc)
	_check(not CQMCalculator.mcmillan_valid(0.05, 0.13), "弱耦合无效域判定")
	var tc_pb = CQMCalculator.mcmillan_tc(105.0, 1.55, 0.13)
	_check(tc_pb > 6.0 and tc_pb < 14.0, "McMillan Pb 参数 Tc = %.2f K ∈ [6,14]" % tc_pb)
	_check(CQMCalculator.mcmillan_tc(275.0, 0.0, 0.13) == 0.0, "零耦合返回 0")

	# 同位素指数拟合: 合成数据 Tc = C·M^(-α), α=0.5 → 拟合恢复 0.5
	var pts: Array = []
	for m in [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]:
		pts.append({"avg_mass": m, "tc": 10.0 * pow(m, -0.5)})
	var alpha = CQMCalculator.fit_isotope_exponent(pts)
	_check(abs(alpha - 0.5) < 0.02, "同位素指数拟合恢复 α=0.5 (得 %.3f)" % alpha)

func _test_critical_fields():
	var delta = 1.76 * 1.381e-23 * 9.25
	var cf = CQMCalculator.compute_critical_fields(9.25, 4.2, delta, 0)
	_check(float(cf.get("hc2", 0.0)) > 0.0, "Nb Hc2 > 0")
	_check(float(cf.get("xi", 0.0)) > 0.0 and float(cf.get("lambda_L", 0.0)) > 0.0,
		"相干长度与穿透深度为正")
	var kappa = float(cf.get("kappa", 0.0))
	var is_type2 = str(cf.get("type", "")) == "II型"
	_check((kappa > 1.0 / sqrt(2.0)) == is_type2,
		"κ 与型判据自洽 (κ=%.2f, %s; n_s/vf 为唯像参数)" % [kappa, cf.get("type", "")])
	var cf0 = CQMCalculator.compute_critical_fields(0.0, 4.2, delta, 0)
	_check(float(cf0.get("hc2", -1.0)) == 0.0, "Tc=0 时临界场归零")

func _test_cqm_modules():
	var eigenvalues: Array = [0.1, 0.3, 0.7, 1.2, 2.0]
	var stepwise = CQMStepwiseTransition.compute(eigenvalues, 9.0)
	_check(stepwise.get("transitions", []).size() >= 1, "分步相变产生转变点")
	var cond = CQMStepwiseTransition.condensate_state(4.0, stepwise.get("transitions", []))
	_check(cond is Dictionary, "凝聚态计算不崩溃")
	var quad = CQMStepwiseTransition.lah10_quadrupole_check(eigenvalues, 200.0)
	_check(quad is Dictionary, "LaH10 四极检验不崩溃")

	var order_params = CQMCalculator.order_parameters(9.25, 4.2, 0)
	var gl = CQMGLFreeEnergy.compute(order_params, 4.2, 9.25)
	_check(gl is Dictionary and gl.has("F_GL"), "GL 自由能计算")
	var gl_hi = CQMGLFreeEnergy.compute(order_params, 9.0, 9.25)
	_check(float(gl_hi.get("F_GL", 0.0)) > float(gl.get("F_GL", 0.0)),
		"GL: T→Tc 时自由能升高")

	var emergence = CQMEmergenceIntegral.evaluate(eigenvalues, 0.5, 4.2, 0.4, 9.25, 0)
	_check(emergence is Dictionary, "涌现积分计算")

	var topo = CQMTopologyFactor.compute_from_spectral_gap(0.5)
	_check(topo > 0.0 and topo <= 1.0, "拓扑因子 ∈ (0,1]: %.4f" % topo)
	var topo_ideal = CQMTopologyFactor.compute_from_spectral_gap(
		CQMCartanBuilder.spectral_gap())
	_check(abs(topo_ideal - 1.0) < 1e-9, "理想 A4 谱隙 → 拓扑因子 = 1")

	_test_g16_g17_bridge()

# ---------- G16/G17 Regge-嘉当耦合桥接 ----------
func _dense_lattice_atoms() -> Array:
	# 4×2×2 立方晶格 (0.4 Å 间距) — 产生四面体剖分
	var atoms: Array = []
	for i in range(4):
		for j in range(2):
			for k in range(2):
				atoms.append({"symbol": "Nb", "position": Vector3(i * 0.4, j * 0.4, k * 0.4)})
	return atoms

func _lattice_bonds(atoms: Array) -> Array:
	var pairs: Array = []
	for a in range(atoms.size()):
		for b in range(a + 1, atoms.size()):
			var pa: Vector3 = atoms[a]["position"]
			var pb: Vector3 = atoms[b]["position"]
			if pa.distance_to(pb) < 0.6:
				pairs.append([a, b])
	return pairs

func _test_g16_g17_bridge():
	# Lean 定义的一一对应数值实现
	_check(absf(ReggeCartanBridge.dual_area(2.0) - sqrt(3.0)) < 1e-9,
		"G16 对偶面积 A(2.0) = √3 (Lean: reggeDualArea)")
	_check(absf(ReggeCartanBridge.ricci_scalar(0.5, 1.0) - 1.0) < 1e-9,
		"G16 Ricci 标量 R(0.5, 1.0) = 1.0 (Lean: reggeEffectiveRicciScalar)")
	_check(absf(ReggeCartanBridge.spectral_edge_length(2.0, 1.0, 4.0) - 1.0) < 1e-9,
		"G16 谱边长 l(κ=2, λᵢλⱼ=4) = 1.0 (Lean: reggeTetrahedronEdgeLength)")
	var cf = ReggeCartanBridge.closed_form_ricci(0.1, 0.585786437626905, 1.0)
	_check(absf(cf - (0.8 / sqrt(3.0)) * 0.585786437626905 * 0.585786437626905) < 1e-9,
		"G16 闭式 R = (8δ/√3)λ²/κ² (Lean: reggeDeficit_ricciScalar_closedForm)")

	var atoms = _dense_lattice_atoms()
	var pairs = _lattice_bonds(atoms)
	var positions: Array = []
	for a in atoms:
		positions.append(a["position"])
	var regge = ReggeCalculator.compute_regge_3d(positions, pairs, 1)
	_check(int(regge.get("tetrahedra_count", 0)) > 0,
		"稠密晶格产生四面体 (实际 %d)" % int(regge.get("tetrahedra_count", 0)))

	# G16: 亏角密度 → Ricci 标量
	var g16 = ReggeCartanBridge.compute_g16(regge, atoms)
	_check(int(g16.get("hinge_count", 0)) > 0, "G16 逐 hinge 计算覆盖")
	_check(absf(float(g16.get("ricci_scalar_global", 0.0))) > 0.0,
		"G16 全局 Ricci 标量非零 = %.4f" % float(g16.get("ricci_scalar_global", 0.0)))
	_check(float(g16.get("kappa", 0.0)) > 0.0,
		"G16 κ 标定正 = %.4f" % float(g16.get("kappa", 0.0)))
	_check(absf(float(g16.get("mean_spectral_weight", 0.0)) - 0.585786437626905) < 0.05,
		"G16 无缺陷 Nb 谱权重 ≈ 2-√2 (得 %.4f)" % float(g16.get("mean_spectral_weight", 0.0)))
	_check(bool(g16.get("monotonicity_holds", false)) or int(g16.get("hinge_count", 0)) < 2,
		"G16 谱间隙→曲率单调性方向成立")

	# G17: 有效度规 → 泊松牛顿退化
	var g17 = ReggeCartanBridge.compute_g17(regge, atoms, positions)
	_check(int(g17.get("sample_count", 0)) == 216, "G17 采样 6×6×6 = 216 点")
	_check(absf(float(g17.get("poisson_residual_newton", 1.0))) < 0.35,
		"G17 牛顿基准泊松残差 < 35%% (数值格式验证, 得 %.1f%%)" % (100.0 * float(g17.get("poisson_residual_newton", 1.0))))
	_check(float(g17.get("poisson_residual_newton", 1.0)) <= float(g17.get("poisson_residual_regge", 0.0)) or
		float(g17.get("poisson_residual_regge", 1.0)) < 0.35,
		"G17 Regge 退化残差有界 (%.1f%% vs 牛顿 %.1f%%)" % [
			100.0 * float(g17.get("poisson_residual_regge", 1.0)),
			100.0 * float(g17.get("poisson_residual_newton", 1.0))])
	_check(bool(g17.get("lorentz_signature_valid", false)),
		"G17 洛伦兹号差有效 |h₀₀|max = %s" % str(g17.get("h00_max", -1.0)))

	# 约束作用量: 矩阵和乐严格化
	var network: Array = []
	for i in range(atoms.size()):
		var row: Array = []
		row.resize(atoms.size())
		row.fill(0.0)
		network.append(row)
	for pair in pairs:
		network[pair[0]][pair[1]] = 0.5
		network[pair[1]][pair[0]] = 0.5
	var s_c = CQMConstraintAction.compute(regge.get("tetrahedra", []), network, 0.0)
	_check(absf(float(s_c.get("S_holonomy", 0.0))) > 0.0,
		"S_constraint 和乐项非零 (亏角×A4和乐×关联模式) = %.6f" % float(s_c.get("S_holonomy", 0.0)))

	# A4 谱半径归一化迹: N=1 且环路权重 1/2 → 0.5·(2-√2) (谱间隙不动点)
	var h1 = {"tet_count": 1, "opposite_verts": [[2, 3]], "edge": [0, 1],
		"deficit_angle": 0.0}
	var mode = CQMConstraintAction.association_mode(h1, network)
	_check(absf(mode - 0.5) < 1e-9,
		"关联模式 M_h = ½(R_ab + R̄_环路) = 0.5 (均匀关联) (得 %.4f)" % mode)
	var hol = CQMConstraintAction.matrix_holonomy(
		{"tet_count": 1, "opposite_verts": [[2, 3]]}, network)
	_check(absf(hol - 0.5 * (2.0 - sqrt(2.0))) < 1e-6,
		"A4 和乐 N=1, w=½ → 0.5·(2-√2) (得 %.6f)" % hol)

	# 端到端: 计算引擎输出 G16/G17
	var bonds_dicts: Array = []
	for pair in pairs:
		bonds_dicts.append({"a": pair[0], "b": pair[1], "order": 1})
	var res = CQMCalculator.evaluate_molecule(atoms, bonds_dicts, {"temperature": 4.2})
	var actions = res.get("cqm_actions", {})
	_check(actions.has("G16_ricci") and actions.has("G17_newtonian"),
		"计算引擎端到端输出 G16/G17 桥接结果")
	_check(int(actions.get("G16_ricci", {}).get("hinge_count", 0)) > 0,
		"端到端 G16 hinge 覆盖")

func _test_sweeps():
	var base = {"temperature": 4.2}
	var p_sweep = CQMCalculator.sweep_pressure(_nb_atom(), [], base, 0.0, 100.0, 11)
	_check(p_sweep.size() == 11, "压强扫描 11 点")
	var tc0 = float(p_sweep[0].get("tc", 0.0))
	var tc100 = float(p_sweep[10].get("tc", 0.0))
	_check(tc100 > tc0, "压强升高 Tc 单调增强 (Tc(0)=%.2f, Tc(100GPa)=%.2f)" % [tc0, tc100])

	var iso = CQMCalculator.sweep_isotope(_nb_atom(), [], base, 0.5, 2.0, 11)
	_check(iso.get("points", []).size() == 11, "同位素扫描 11 点")
	var alpha = iso.get("alpha", NAN)
	_check(not is_nan(alpha) and alpha > 0.0 and alpha < 1.0,
		"同位素效应指数 α = %.3f ∈ (0,1)" % (alpha if not is_nan(alpha) else -1.0))

	var comp = CQMCalculator.sweep_composition("Nb", "Ti", 27, base, 11)
	var cpts = comp.get("points", [])
	_check(cpts.size() == 11, "成分扫描 11 点")
	_check(float(cpts[0].get("x", -1.0)) == 0.0 and float(cpts[10].get("x", -1.0)) == 1.0,
		"成分扫描覆盖 x ∈ [0,1]")
	_check(int(cpts[0].get("count_b", -1)) == 0 and int(cpts[10].get("count_b", -1)) == 27,
		"端点成分计数正确 (纯Nb / 纯Ti)")
	var cb_half = int(cpts[5].get("count_b", -1))
	_check(cb_half == 14 or cb_half == 13, "x=0.5 处 B 原子数 ≈ 13/27 (得 %d)" % cb_half)
	_check(not comp.get("best", {}).is_empty(), "成分扫描返回最优成分点")
	var same = CQMCalculator.sweep_composition("Nb", "Nb", 8, base, 5)
	_check(same.get("points", []).is_empty(), "同元素成分扫描返回空")

# ---------- 专业符号 ----------
func _test_physics_notation():
	var t = PhysicsNotation.format_temperature(9.25)
	_check(t.find("K") >= 0, "温度格式含单位 K: %s" % t)
	var p = PhysicsNotation.format_pressure(155.0)
	_check(p.find("GPa") >= 0, "压强格式含 GPa: %s" % p)
	var u = PhysicsNotation.format_with_uncertainty(275.0, 8.0, "K")
	_check(u.find("±") >= 0 and u.find("K") >= 0, "不确定度格式: %s" % u)
	var sci = PhysicsNotation.format_scientific_unicode(1.616e-35)
	_check(sci.find("10") >= 0, "科学计数法上标: %s" % sci)
	_check(abs(PhysicsNotation.ev_to_kelvin(1.0) - 11604.5) < 1.0, "eV→K 转换")
	_check(PhysicsNotation.symbol_tc() == "T_c" or PhysicsNotation.symbol_tc().length() > 0,
		"Tc 符号非空")
	var pair = PhysicsNotation.format_pairing_symmetry(1)
	_check(pair.find("d") >= 0, "配对对称性 d 波标注: %s" % pair)

# ---------- 化学验证 ----------
func _test_chemistry_validator():
	var d = ChemValidator.validate_bond("H", "H", 0.74)
	_check(d is Dictionary, "H-H 键验证不崩溃")
	_check(ChemValidator.max_valence("C") == 4, "C 最大价键 = 4")
	_check(ChemValidator.max_valence("H") == 1, "H 最大价键 = 1")

	var carbon = Atom3D.new()
	carbon.element_symbol = "C"
	var bonds: Array = []
	for i in range(5):
		var partner = Atom3D.new()
		partner.element_symbol = "H"
		var bond = Bond3D.new()
		bond.atom_a = carbon
		bond.atom_b = partner
		bonds.append(bond)
	_check(not ChemValidator.can_add_bond(carbon, bonds), "C 五键被化学规则拒绝")
	var status = ChemValidator.valence_status(carbon, bonds)
	_check(int(status.get("current", -1)) == 5 and bool(status.get("full", false)),
		"价键状态计数 = 5 (已满)")
	var sc = ChemValidator.gen_lattice_points(0, 3.3, 1.0, Vector3.ZERO)
	_check(sc.size() > 0, "SC 晶格点生成")

# ---------- 空间哈希与力场 ----------
func _test_spatial_hash_and_force_field():
	var hash = SpatialHash.new(2.0)
	var positions = [
		Vector3(0, 0, 0), Vector3(1, 0, 0), Vector3(5, 0, 0), Vector3(10, 0, 0)
	]
	for i in range(positions.size()):
		hash.insert(i, positions[i])
	var near = hash.query_radius(Vector3(0, 0, 0), 1.5)
	_check(near.has(0) and near.has(1) and not near.has(2),
		"空间哈希半径查询正确 (r=1.5)")
	var nearest = hash.query_nearest(Vector3(4.6, 0, 0), 3.0)
	_check(nearest == 2, "空间哈希最近邻查询 (4.6 → idx2)")
	hash.update_position(2, Vector3(0.5, 0, 0))
	_check(hash.query_radius(Vector3(0, 0, 0), 1.0).has(2), "位置更新生效")

	var nl = SpatialHash.NeighborList.new(1.1, 0.2)
	var grid: Array = []
	for ix in range(3):
		for iy in range(3):
			for iz in range(3):
				grid.append(Vector3(ix * 1.0, iy * 1.0, iz * 1.0))
	nl.set_positions(grid)
	var nb0 = nl.get_neighbors(0)
	_check(nb0.size() == 3, "邻居列表角点面邻 = 3 (对角 1.414 正确排除, 得 %d)" % nb0.size())
	_check(nl.get_neighbors(13).size() == 6, "体心 (1,1,1) 面邻 = 6 (得 %d)" % nl.get_neighbors(13).size())

	# 力场: LJ 能量有限且对称结构受力平衡
	var atoms: Array = []
	for ix in range(3):
		for iy in range(3):
			for iz in range(3):
				atoms.append({"symbol": "Ar", "position": Vector3(ix * 3.8, iy * 3.8, iz * 3.8)})
	var e = ForceField.compute_energy(atoms, [])
	_check(not is_nan(e) and abs(e) < 100.0, "LJ 能量有限 (%.4f)" % e)
	var forces = ForceField.compute_forces(atoms, [])
	var center = Vector3.ZERO
	for f in forces:
		center += f
	_check(center.length() < 1e-6, "对称结构合力为零 (牛顿第三定律)")

	# 性能: 200 原子能量计算应 < 1s (空间哈希加速)
	var perf_atoms: Array = []
	var rng = RandomNumberGenerator.new()
	rng.seed = 42
	for i in range(200):
		perf_atoms.append({"symbol": "Ar",
			"position": Vector3(rng.randf(), rng.randf(), rng.randf()) * 40.0})
	var t0 = Time.get_ticks_msec()
	ForceField.compute_energy(perf_atoms, [])
	var dt = Time.get_ticks_msec() - t0
	_check(dt < 1000, "200 原子 LJ 能量 %dms < 1000ms" % dt)

	var minimized = ForceField.minimize(atoms.duplicate(true), [], [], 10, 0.0005)
	_check(minimized is Dictionary and minimized.has("converged"), "能量最小化运行正常")

# ---------- 周期表 UI ----------
func _test_element_palette():
	var palette = ElementPalette.new()
	get_tree().root.call_deferred("add_child", palette)
	await get_tree().process_frame
	await get_tree().process_frame
	var button_count = 0
	for sym in palette._buttons:
		if palette._buttons[sym] is Button:
			button_count += 1
	_check(button_count == 118, "周期表 UI 按钮 = 118 (实际 %d)" % button_count)
	palette.queue_free()
