extends RefCounted
class_name ProjectManager

# 项目保存/加载管理器
# 序列化/反序列化：原子、键、画笔笔划、自定义分子、物理参数、计算结果、材料元数据
# 版本: 1.1 — 新增 results (最后计算结果) 与 metadata (材料名/备注/基准对照)

const PROJECT_VERSION := "1.1"

static func save_project(path: String, workspace: Node, brush_strokes: Array,
						 custom_molecules: Array, physics_params: Dictionary,
						 extra: Dictionary = {}) -> bool:
	var data = {
		"version": PROJECT_VERSION,
		"timestamp": Time.get_unix_time_from_system(),
		"atoms": _serialize_atoms(workspace),
		"bonds": _serialize_bonds(workspace),
		"brush_strokes": _serialize_brush_strokes(brush_strokes),
		"custom_molecules": custom_molecules,
		"physics_params": _serialize_params(physics_params),
		"metadata": extra.get("metadata", {}),
		"results": _serialize_results(extra.get("results", {})),
	}
	var file = FileAccess.open(path, FileAccess.WRITE)
	if not file:
		return false
	file.store_string(JSON.stringify(data, "\t"))
	file.close()
	return true

static func load_project(path: String) -> Dictionary:
	var file = FileAccess.open(path, FileAccess.READ)
	if not file:
		return {}
	var text = file.get_as_text()
	file.close()
	var data = JSON.parse_string(text)
	if data == null or not data is Dictionary:
		return {}
	return _migrate(data)

## 版本迁移: 1.0 → 1.1 (补充缺失字段, 前向兼容)
static func _migrate(data: Dictionary) -> Dictionary:
	var v = str(data.get("version", "1.0"))
	if not data.has("metadata"):
		data["metadata"] = {}
	if not data.has("results"):
		data["results"] = {}
	data["version_loaded_from"] = v
	return data

## 计算结果序列化: 去除不可 JSON 化的嵌套 (Vector3/数组键)
static func _serialize_results(results: Dictionary) -> Dictionary:
	if results.is_empty():
		return {}
	var safe_keys := ["verdict", "tc_estimate", "confidence", "spectral_gap",
		"causal_cutoff_temp", "coupling", "lambda_literature", "lambda_coverage",
		"dos_fermi", "debye_temp", "debye_source", "omega_log_temp",
		"sqrt_omega2_temp", "ad_f1", "ad_f2", "mu_star", "mcmillan_valid",
		"tc_method", "gap_0", "gap_0_meV", "atom_count", "bond_count",
		"temperature", "pressure", "mag_field", "doping", "isotope_alpha",
		"n0v_product", "pairing_symmetry", "compute_time_ms"]
	var out := {}
	for k in safe_keys:
		if results.has(k):
			out[k] = results[k]
	if results.has("tc_mu_star_sensitivity"):
		var sens: Dictionary = results["tc_mu_star_sensitivity"]
		var sens_out := {}
		for mus in sens:
			sens_out[str(mus)] = sens[mus]
		out["tc_mu_star_sensitivity"] = sens_out
	if results.has("critical_fields"):
		var cf: Dictionary = results["critical_fields"]
		out["critical_fields"] = {"hc1": cf.get("hc1", 0.0), "hc2": cf.get("hc2", 0.0),
			"hc": cf.get("hc", 0.0), "kappa": cf.get("kappa", 0.0),
			"xi": cf.get("xi", 0.0), "lambda_L": cf.get("lambda_L", 0.0),
			"type": cf.get("type", "")}
	return out

static func _serialize_atoms(workspace: Node) -> Array:
	var result: Array = []
	if not workspace.has_method("get") or not workspace.get("atoms"):
		return result
	for atom in workspace.atoms:
		if not is_instance_valid(atom):
			continue
		result.append({
			"symbol": atom.element_symbol,
			"isotope": atom.isotope_mass,
			"position": [atom.global_position.x, atom.global_position.y, atom.global_position.z],
			"scale": [atom.scale.x, atom.scale.y, atom.scale.z]
		})
	return result

static func _serialize_bonds(workspace: Node) -> Array:
	var result: Array = []
	if not workspace.get("bonds"):
		return result
	for bond in workspace.bonds:
		if not is_instance_valid(bond):
			continue
		var a_idx = workspace.atoms.find(bond.atom_a)
		var b_idx = workspace.atoms.find(bond.atom_b)
		if a_idx < 0 or b_idx < 0:
			continue
		result.append({
			"a": a_idx,
			"b": b_idx,
			"order": bond.bond_order
		})
	return result

static func _serialize_brush_strokes(brush_strokes: Array) -> Array:
	var result: Array = []
	for stroke in brush_strokes:
		var pts: Array = []
		for p in stroke.get("points", []):
			if p is Vector3:
				pts.append([p.x, p.y, p.z])
		result.append({
			"shape": stroke.get("shape", 0),
			"is_boundary": stroke.get("is_boundary", false),
			"element": stroke.get("element", "H"),
			"points": pts,
			"physical_params": _serialize_params(stroke.get("physical_params", {}))
		})
	return result

static func _serialize_params(params: Dictionary) -> Dictionary:
	var result = params.duplicate(true)
	if result.has("efield") and result["efield"] is Vector3:
		var v = result["efield"]
		result["efield"] = [v.x, v.y, v.z]
	if result.has("pressure_dir") and result["pressure_dir"] is Vector3:
		var v = result["pressure_dir"]
		result["pressure_dir"] = [v.x, v.y, v.z]
	if result.has("mag_field_dir") and result["mag_field_dir"] is Vector3:
		var v = result["mag_field_dir"]
		result["mag_field_dir"] = [v.x, v.y, v.z]
	return result

static func deserialize_params(params: Dictionary) -> Dictionary:
	var result = params.duplicate(true)
	if result.has("efield") and result["efield"] is Array:
		var a = result["efield"]
		result["efield"] = Vector3(a[0], a[1], a[2])
	if result.has("pressure_dir") and result["pressure_dir"] is Array:
		var a = result["pressure_dir"]
		result["pressure_dir"] = Vector3(a[0], a[1], a[2])
	if result.has("mag_field_dir") and result["mag_field_dir"] is Array:
		var a = result["mag_field_dir"]
		result["mag_field_dir"] = Vector3(a[0], a[1], a[2])
	return result

static func apply_loaded_data(data: Dictionary, workspace: Node) -> Dictionary:
	workspace.clear()
	for atom_data in data.get("atoms", []):
		var pos = atom_data.get("position", [0, 0, 0])
		var atom = workspace.add_atom(
			atom_data.get("symbol", "H"),
			int(atom_data.get("isotope", 1)),
			Vector3(pos[0], pos[1], pos[2])
		)
		if atom and atom_data.has("scale"):
			var s = atom_data["scale"]
			atom.scale = Vector3(s[0], s[1], s[2])
	for bond_data in data.get("bonds", []):
		var a_idx = int(bond_data.get("a", 0))
		var b_idx = int(bond_data.get("b", 0))
		if a_idx < workspace.atoms.size() and b_idx < workspace.atoms.size():
			workspace.add_bond(
				workspace.atoms[a_idx],
				workspace.atoms[b_idx],
				int(bond_data.get("order", 1))
			)
	var brush_strokes: Array = []
	for stroke_data in data.get("brush_strokes", []):
		var pts: Array = []
		for p in stroke_data.get("points", []):
			pts.append(Vector3(p[0], p[1], p[2]))
		var stroke = {
			"shape": int(stroke_data.get("shape", 0)),
			"is_boundary": stroke_data.get("is_boundary", false),
			"element": stroke_data.get("element", "H"),
			"points": pts,
			"physical_params": deserialize_params(stroke_data.get("physical_params", {}))
		}
		brush_strokes.append(stroke)
	return {
		"brush_strokes": brush_strokes,
		"custom_molecules": data.get("custom_molecules", []),
		"physics_params": deserialize_params(data.get("physics_params", {}))
	}

static func export_results_csv(path: String, results: Dictionary) -> bool:
	var file = FileAccess.open(path, FileAccess.WRITE)
	if not file:
		return false
	file.store_line("Property,Value,Unit")
	file.store_line("Verdict,%s," % results.get("verdict", ""))
	file.store_line("Tc,%s,K" % str(results.get("tc_estimate", 0)))
	file.store_line("Confidence,%.4f," % results.get("confidence", 0))
	file.store_line("SpectralGap,%.6f," % results.get("spectral_gap", 0))
	file.store_line("Coupling,%.6f," % results.get("coupling", 0))
	file.store_line("DOS_Fermi,%.6f," % results.get("dos_fermi", 0))
	file.store_line("DebyeTemp,%.2f,K" % results.get("debye_temp", 0))
	file.store_line("MuStar,%.4f," % results.get("mu_star", 0))
	file.store_line("PairingSymmetry,%d," % results.get("pairing_symmetry", 0))
	file.store_line("AtomCount,%d," % results.get("atom_count", 0))
	file.store_line("BondCount,%d," % results.get("bond_count", 0))
	var cf = results.get("critical_fields", {})
	if not cf.is_empty():
		file.store_line("Hc1,%s,T" % str(cf.get("hc1", 0)))
		file.store_line("Hc2,%s,T" % str(cf.get("hc2", 0)))
		file.store_line("Hc,%s,T" % str(cf.get("hc", 0)))
		file.store_line("Kappa,%.4f," % cf.get("kappa", 0))
		file.store_line("Xi,%s,m" % str(cf.get("xi", 0)))
		file.store_line("LambdaL,%s,m" % str(cf.get("lambda_L", 0)))
	var ev = results.get("eigenvalues", [])
	for i in range(ev.size()):
		file.store_line("Eigenvalue_%d,%.6f," % [i + 1, float(ev[i])])
	file.close()
	return true

static func export_screenshot(path: String, viewport: Viewport) -> bool:
	var img = viewport.get_texture().get_image()
	return img.save_png(path) == OK

## Markdown 学术报告导出: 完整计算链、中间量、公式、基准对照、证据等级
static func export_report_md(path: String, results: Dictionary, info: Dictionary = {}) -> bool:
	var PN = PhysicsNotation
	var file = FileAccess.open(path, FileAccess.WRITE)
	if not file:
		return false
	var name = str(info.get("material_name", "未命名结构"))
	var formula = str(info.get("formula", "—"))
	var dt = Time.get_datetime_string_from_system().replace("T", " ")
	file.store_line("# CQM 超导材料设计器 — 计算报告")
	file.store_line("")
	file.store_line("- **材料**: %s (%s)" % [name, formula])
	file.store_line("- **生成时间**: %s" % dt)
	file.store_line("- **原子数/键数**: %d / %d" % [int(results.get("atom_count", 0)), int(results.get("bond_count", 0))])
	file.store_line("")
	file.store_line("## 1. 判定结论")
	file.store_line("")
	file.store_line("- 判定: **%s**" % str(results.get("verdict", "—")))
	file.store_line("- Tc 估计: **%s**" % PN.format_tc(results.get("tc_estimate", 0.0), results.get("confidence", 0.0)))
	file.store_line("- 置信度: %.1f%%" % (float(results.get("confidence", 0.0)) * 100.0))
	file.store_line("- 计算方法: %s (公式适用域: %s)" % [str(results.get("tc_method", "—")),
		"满足" if results.get("mcmillan_valid", false) else "不满足"])
	file.store_line("")
	file.store_line("## 2. 电声耦合链 (Allen–Dynes 1975)")
	file.store_line("")
	file.store_line("公式: %s" % PN.FORMULA_ALLEN_DYNES)
	file.store_line("")
	file.store_line("| 量 | 值 | 说明 |")
	file.store_line("|---|---|---|")
	file.store_line("| θ_D | %s | %s |" % [PN.format_temperature(results.get("debye_temp", 0.0)), str(results.get("debye_source", ""))])
	file.store_line("| ω_log | %s | 德拜模型 0.7165·θ_D |" % PN.format_temperature(results.get("omega_log_temp", 0.0)))
	file.store_line("| √⟨ω²⟩ | %s | 0.7746·θ_D |" % PN.format_temperature(results.get("sqrt_omega2_temp", 0.0)))
	file.store_line("| λ | %s | %s |" % [PN.format_coupling_constant(results.get("coupling", 0.0), results.get("mu_star", 0.0)).replace("\n", " "), PN.FORMULA_LAMBDA_HOPFIELD])
	file.store_line("| μ* | %.4f | Morel–Anderson 库仑赝势 |" % float(results.get("mu_star", 0.0)))
	file.store_line("| f₁ / f₂ | %.4f / %.4f | 强耦合修正因子 |" % [float(results.get("ad_f1", 1.0)), float(results.get("ad_f2", 1.0))])
	file.store_line("| N(0)V | %s | BCS 无量纲耦合 |" % PN.format_number(float(results.get("n0v_product", 0.0))))
	var alpha = results.get("isotope_alpha", NAN)
	if not is_nan(float(alpha)):
		file.store_line("| 同位素指数 α | %.3f | BCS: 0.5; 非声子机制可偏离/为负 |" % float(alpha))
	var sens: Dictionary = results.get("tc_mu_star_sensitivity", {})
	if not sens.is_empty():
		file.store_line("")
		file.store_line("### Tc 对 μ* 的敏感性")
		file.store_line("")
		file.store_line("| μ* | 0.10 | 0.13 | 0.16 |")
		file.store_line("|---|---|---|---|")
		file.store_line("| Tc (K) | %s | %s | %s |" % [
			PN.format_number(float(sens.get("0.10", 0.0))),
			PN.format_number(float(sens.get("0.13", 0.0))),
			PN.format_number(float(sens.get("0.16", 0.0)))])
	file.store_line("")
	file.store_line("## 3. 能隙与序参量")
	file.store_line("")
	file.store_line("- Δ₀ = %s" % PN.format_gap(results.get("gap_0", 0.0), results.get("tc_estimate", 0.0)).replace("\n", "  \n- "))
	file.store_line("- %s" % PN.FORMULA_GAP_RATIO)
	file.store_line("")
	file.store_line("## 4. 临界场与长度尺度 (唯象 GL)")
	file.store_line("")
	var cf: Dictionary = results.get("critical_fields", {})
	if not cf.is_empty() and float(cf.get("hc2", 0.0)) > 0:
		file.store_line("| 量 | 值 |")
		file.store_line("|---|---|")
		file.store_line("| Hc1 | %s |" % PN.format_hc(cf.get("hc1", 0.0), "Hc1"))
		file.store_line("| Hc2 | %s |" % PN.format_hc(cf.get("hc2", 0.0), "Hc2"))
		file.store_line("| Hc | %s |" % PN.format_hc(cf.get("hc", 0.0), "Hc"))
		file.store_line("| κ | %s" % PN.format_ginzburg_landau(cf.get("kappa", 0.0)))
		file.store_line("| ξ | %s |" % PN.format_coherence_length(cf.get("xi", 0.0)))
		file.store_line("| λ_L | %s |" % PN.format_penetration_depth(cf.get("lambda_L", 0.0)))
	file.store_line("")
	file.store_line("## 5. 实验基准对照")
	file.store_line("")
	var bench: Dictionary = info.get("benchmark", {})
	if bench.is_empty():
		file.store_line("(无匹配基准)")
	else:
		file.store_line("| 基准 | Tc 实验 | 压强 | 年份 | 来源 |")
		file.store_line("|---|---|---|---|---|")
		file.store_line("| %s | %s K | %s GPa | %d | %s |" % [
			str(bench.get("formula", "—")),
			str(bench.get("tc_K", "—")),
			str(bench.get("pressure_GPa", 0)),
			int(bench.get("year", 0)),
			str(bench.get("source", "—"))])
		var tc_exp = float(bench.get("tc_K", 0.0))
		var tc_calc = float(results.get("tc_estimate", 0.0))
		if tc_exp > 0:
			file.store_line("")
			file.store_line("计算/实验比: %.3f" % (tc_calc / tc_exp))
	file.store_line("")
	file.store_line("## 6. 证据等级")
	file.store_line("")
	file.store_line("每个输出量的证据分级: `lean_verified` (Lean 形式化数值) / `literature` (文献输入) / `semi_empirical` (半经验模型) / `phenomenological` (唯像实现)。")
	file.store_line("")
	file.store_line("---")
	file.store_line("")
	file.store_line("*本报告由 CQM 超导材料设计器自动生成。理论框架: CQM 超导理论 (谱-因果-涌现); 数值链对应 Lean 形式化定义。*")
	file.close()
	return true