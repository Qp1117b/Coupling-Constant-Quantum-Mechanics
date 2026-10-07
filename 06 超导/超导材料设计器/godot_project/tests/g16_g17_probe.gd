extends Node

## G16/G17 数值输出探针 (一次性运行, 打印具体数值供人工核查量级)

func _ready():
	var atoms: Array = []
	for i in range(4):
		for j in range(2):
			for k in range(2):
				atoms.append({"symbol": "Nb", "position": Vector3(i * 0.4, j * 0.4, k * 0.4)})
	var pairs: Array = []
	for a in range(atoms.size()):
		for b in range(a + 1, atoms.size()):
			if (atoms[a]["position"] as Vector3).distance_to(atoms[b]["position"]) < 0.6:
				pairs.append([a, b])
	var positions: Array = []
	for a in atoms:
		positions.append(a["position"])

	var regge = ReggeCalculator.compute_regge_3d(positions, pairs, 1)
	var g16 = ReggeCartanBridge.compute_g16(regge, atoms)
	var g17 = ReggeCartanBridge.compute_g17(regge, atoms, positions)

	print("=== G16 (亏角密度→Ricci 标量) ===")
	print("hinges = %d | tets = %d" % [g16.hinge_count, regge.tetrahedra_count])
	print("R_global (体积加权) = %.6f  [1/Å²]" % g16.ricci_scalar_global)
	print("R_mean (逐hinge)   = %.6f" % g16.ricci_scalar_mean)
	print("R_closed (谱闭式)  = %.6f" % g16.ricci_scalar_closed_form)
	print("闭式-数值交叉误差  = %.2f%%" % (100.0 * g16.cross_check_rel_error))
	print("δ_eff 密度 = %.6f | A_dual 均值 = %.6f Å²" % [g16.deficit_density, g16.dual_area_mean])
	print("κ = %.6f Å | λ̄ = %.6f | V_total = %.6f Å³" % [g16.kappa, g16.mean_spectral_weight, g16.total_volume])
	print("单调性成立 = %s" % g16.monotonicity_holds)

	print("=== G17 (有效度规→Poisson 牛顿退化) ===")
	print("拉普拉斯体积和: Regge = %s | 牛顿 = %s | 目标 4πGM = %s" % [
		_sci(g17.laplacian_sum_regge), _sci(g17.laplacian_sum_newton), _sci(g17.gauss_target)])
	print("泊松残差: Regge = %.1f%% | 牛顿基准 = %.1f%%" % [
		100.0 * g17.poisson_residual_regge, 100.0 * g17.poisson_residual_newton])
	print("β 标定 = %s | |h00|max = %s | 洛伦兹号差有效 = %s" % [
		_sci(g17.newtonian_scale_beta), _sci(g17.h00_max), str(g17.lorentz_signature_valid)])
	print("M_total = %s kg | 采样 = %d 点" % [_sci(g17.mass_total_kg), g17.sample_count])

	# 端到端确认引擎输出
	var bonds: Array = []
	for pair in pairs:
		bonds.append({"a": pair[0], "b": pair[1], "order": 1})
	var res = CQMCalculator.evaluate_molecule(atoms, bonds, {"temperature": 4.2})
	print("=== 端到端 Tc = %.2f K | 证据等级 G16 = %s ===" % [
		res.tc_estimate, res.evidence_levels.regge_cartan_G16])
	get_tree().quit(0)

func _sci(v: float) -> String:
	return String.num_scientific(v)
