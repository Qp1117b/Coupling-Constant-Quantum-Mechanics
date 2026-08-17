extends Node

## 应用级冒烟测试: godot --headless --path godot_project res://tests/app_smoke_test.tscn
## 加载真实主场景, 逐项操作: 材料生成/预设/计算/扫描/窗口/导入导出/画笔/分子组, 捕获运行时错误

var passed := 0
var failed := 0
var failures: Array = []
var _app: Node

func _ready():
	await get_tree().process_frame
	_app = get_tree().root.get_node_or_null("Main")
	if _app == null:
		# 直接实例化主场景
		var scene = load("res://scenes/Main.tscn")
		if scene == null:
			_finish("主场景不存在")
			return
		_app = scene.instantiate()
		get_tree().root.add_child.call_deferred(_app)
		await get_tree().process_frame
		await get_tree().process_frame
	await _run_all()
	await get_tree().process_frame
	_finish()

func _finish(msg: String = ""):
	print("\n========== 应用冒烟测试结果 ==========")
	if msg != "":
		print("致命: " + msg)
	print("通过: %d  失败: %d" % [passed, failed])
	for f in failures:
		print("  - " + f)
	print("======================================")
	get_tree().quit(1 if failed > 0 else 0)

func _check(cond: bool, name: String):
	if cond:
		passed += 1
	else:
		failed += 1
		failures.append(name)
		print("[FAIL] " + name)

func _run_all():
	_test_material_generation()
	_test_presets()
	_test_calculation()
	await get_tree().process_frame
	_test_windows()
	_test_import_export()
	_test_lattice_templates()
	_test_layout_fit()
	_test_brush_stroke_calc()
	_test_stale_state_paths()
	_test_physics_interactions()

# ---------- 材料生成 ----------
func _test_material_generation():
	var scdb = SCDB.get_all()
	_check(scdb.size() >= 20, "SCDB 材料数 ≥ 20 (实际 %d)" % scdb.size())
	var bad: Array = []
	for i in range(scdb.size()):
		var m = scdb[i]
		if not m.has("atoms") or m.atoms.is_empty():
			bad.append(str(m.get("name", "?")))
			continue
		for a in m.atoms:
			if not a.has("sym") or not a.has("pos"):
				bad.append(str(m.get("name", "?")) + " 原子数据缺字段")
				break
			var ed = ElementDB.get_element(str(a.sym))
			if ed.is_empty():
				bad.append("%s 含未知元素 %s" % [m.get("name", "?"), a.sym])
				break
	_check(bad.is_empty(), "SCDB 全部材料原子数据有效 (异常: %s)" % str(bad))

	# 逐个生成全部材料 (捕获报错退出)
	var gen_fail: Array = []
	var total_atoms = 0
	for i in range(scdb.size()):
		_app._reset_selection_state()
		_app._workspace.clear()
		_app._sc_selector.selected = i + 1
		_app._generate_sc_material()
		var n = _app._workspace.atoms.size()
		total_atoms += n
		var expect = scdb[i].atoms.size()
		if n != expect:
			gen_fail.append("%s: 期望%d原子, 实得%d" % [scdb[i].name, expect, n])
	_check(gen_fail.is_empty(), "全部 %d 种材料生成成功 (异常: %s)" % [
		scdb.size(), str(gen_fail).substr(0, 400)])
	_check(total_atoms > 0, "材料原子总数 > 0")

	# 生成后原子在 3D 视口内可见
	_app._reset_selection_state()
	_app._workspace.clear()
	_app._sc_selector.selected = 1
	_app._generate_sc_material()
	var visible_count = 0
	for atom in _app._workspace.atoms:
		if atom is Node3D and is_instance_valid(atom) and atom.visible:
			visible_count += 1
	_check(visible_count == _app._workspace.atoms.size(),
		"生成原子全部可见于3D场景 (%d/%d)" % [visible_count, _app._workspace.atoms.size()])

# ---------- 预设 ----------
func _test_presets():
	for preset in ["LaH10", "MgB2", "FeSe", "H2O"]:
		_app._load_preset(preset)
		_check(_app._workspace.atoms.size() > 0, "预设 %s 加载后有原子" % preset)
	# 加载预设后选中状态应为空 (无已释放原子引用)
	_app._load_preset("LaH10")
	_app._workspace.atoms[0].set_selected(true)
	_app._selected_atoms.append(_app._workspace.atoms[0])
	_app._workspace.selected_atom = _app._workspace.atoms[0]
	_app._load_preset("MgB2")
	_check(_app._selected_atoms.is_empty(), "预设切换后选中列表已重置")
	_check(_app._selected_strokes.is_empty(), "预设切换后笔划选中已重置")
	_check(_app._atom_to_molecule.is_empty(), "预设切换后分子映射已重置")

# ---------- 计算 ----------
func _test_calculation():
	_app._load_preset("LaH10")
	_app._execute_calculation()
	_check(not _app._last_results.is_empty(), "LaH10 计算产生结果")
	var tc = float(_app._last_results.get("tc_estimate", -1.0))
	_check(tc > 0.0, "LaH10 计算 Tc > 0 (得 %.2f)" % tc)
	_app._load_preset("MgB2")
	_app._execute_calculation()
	_check(float(_app._last_results.get("tc_estimate", -1.0)) > 0.0, "MgB2 计算 Tc > 0")

	# 原子选中与属性面板
	var atom = _app._workspace.atoms[0]
	atom.set_selected(true)
	_app._workspace.selected_atom = atom
	_app._on_atom_selected(atom)
	_check(true, "原子选中面板更新无崩溃")

	# 撤销/重做
	_app._take_undo_snapshot()
	_app._workspace.remove_atom(_app._workspace.atoms[0])
	_app._do_undo()
	_check(true, "撤销操作无崩溃")
	_app._do_redo()
	_check(true, "重做操作无崩溃")

# ---------- 窗口 ----------
func _test_windows():
	_app._load_preset("LaH10")
	_app._execute_calculation()
	_app._show_chart_window()
	_check(true, "图表窗口打开无崩溃")
	if _app._chart_window and is_instance_valid(_app._chart_window):
		_app._chart_window.queue_free()

	_app._show_geometry_window()
	_check(true, "等效几何窗口无崩溃")

	_app._detect_symmetry()
	_check(true, "对称性检测无崩溃")

	_app._show_sweep_window()
	_check(true, "高通量扫描窗口无崩溃 (压强+同位素+成分)")
	await get_tree().process_frame

	# 标注切换
	_app._toggle_atom_labels()
	_app._toggle_bond_labels()
	_app._update_annotations()
	_check(true, "标注切换与更新无崩溃")

	# 测量模式
	_app._toggle_measure_mode()
	_app._update_measurement()
	_app._toggle_measure_mode()
	_check(true, "测量模式切换无崩溃")

# ---------- 导入导出 ----------
func _test_import_export():
	# XYZ 导入
	var xyz_path = "user://cqm_smoke_test.xyz"
	var f = FileAccess.open(xyz_path, FileAccess.WRITE)
	f.store_string("3\nCQM smoke test\nNb 0.0 0.0 0.0\nNb 1.6 0.0 0.0\nNb 0.0 1.6 0.0\n")
	f.close()
	_app._reset_selection_state()
	_app._workspace.clear()
	_app._import_structure(xyz_path)
	_check(_app._workspace.atoms.size() == 3,
		"XYZ 导入 3 原子 (实际 %d)" % _app._workspace.atoms.size())

	# 结构导出 (XYZ)
	var out_path = "user://cqm_smoke_export.xyz"
	var ok = StructureIO.export_to_format(_app._workspace.atoms, _app._workspace.bonds, "xyz", out_path)
	_check(ok, "结构导出 XYZ 成功")

	# 项目保存/加载往返
	_app._load_preset("MgB2")
	var n0 = _app._workspace.atoms.size()
	var proj_path = "user://cqm_smoke_test.cqm"
	_check(ProjectManager.save_project(proj_path, _app._workspace, _app._brush_strokes, [], {}),
		"项目保存成功")
	var data = ProjectManager.load_project(proj_path)
	_check(not data.is_empty(), "项目加载非空")
	_check(data.get("atoms", []).size() == n0,
		"项目往返原子数一致 (%d/%d)" % [data.get("atoms", []).size(), n0])

	# 结果 CSV 导出
	_app._execute_calculation()
	var csv_ok = ProjectManager.export_results_csv("user://cqm_smoke_test.csv", _app._last_results)
	_check(csv_ok, "计算结果 CSV 导出成功")

	# 项目保存含计算结果与元数据 (v1.1)
	var proj2 = "user://cqm_smoke_test_v11.cqm"
	_check(ProjectManager.save_project(proj2, _app._workspace, _app._brush_strokes, [],
			_app._default_physical_params(),
			{"metadata": {"material_name": "MgB2测试", "formula": "MgB2"},
			 "results": _app._last_results}),
		"项目保存含结果与元数据")
	var data2 = ProjectManager.load_project(proj2)
	_check(not data2.get("results", {}).is_empty(), "项目加载恢复计算结果")
	_check(str(data2.get("metadata", {}).get("material_name", "")) == "MgB2测试",
		"项目加载恢复材料元数据")

	# Markdown 学术报告导出
	_app._load_preset("MgB2")
	_app._execute_calculation()
	var md_ok = ProjectManager.export_report_md("user://cqm_smoke_report.md",
		_app._last_results, {"material_name": "MgB2", "formula": "MgB2",
			"benchmark": SCData.find_benchmark("MgB2")})
	_check(md_ok, "Markdown 学术报告导出成功")
	var rf = FileAccess.open("user://cqm_smoke_report.md", FileAccess.READ)
	var md_text = rf.get_as_text() if rf else ""
	if rf:
		rf.close()
	_check(md_text.find("Allen-Dynes") >= 0 and md_text.find("μ*") >= 0,
		"报告含 Allen-Dynes 公式链与 μ* 相关量")

	# SCDB 严谨化: 压强字段与理论标注
	var scdb2 = SCDB.get_all()
	_check(scdb2.size() >= 45, "SCDB 材料数 ≥ 45 (实际 %d)" % scdb2.size())
	var has_pressure := false
	var has_theoretical := false
	for m in scdb2:
		if float(m.get("pressure_GPa", 0.0)) > 0:
			has_pressure = true
		if bool(m.get("theoretical", false)):
			has_theoretical = true
	_check(has_pressure, "高压氢化物含结构化压强字段")
	_check(has_theoretical, "理论预测条目有标注")

# ---------- 晶格模板 / 超胞 / QE 导出 ----------
func _test_lattice_templates():
	for id in range(1, 7):
		_app._on_lattice_template_id(id)
		_check(_app._workspace.atoms.size() >= 6,
			"晶格模板 %d 生成原子 (%d)" % [id, _app._workspace.atoms.size()])
		_check(_app._workspace.bonds.size() > 0 or _app._workspace.atoms.size() < 2,
			"晶格模板 %d 自动成键" % id)
	# 超胞 2x1x1
	_app._on_lattice_template_id(3)
	var n_before = _app._workspace.atoms.size()
	_app._build_supercell(2, 1, 1)
	_check(_app._workspace.atoms.size() == n_before * 2,
		"超胞 2×1×1 原子数翻倍 (%d → %d)" % [n_before, _app._workspace.atoms.size()])
	# QE 输入导出到文件
	var qe_path = "user://cqm_smoke_test.in"
	var qf = FileAccess.open(qe_path, FileAccess.WRITE)
	if qf:
		qf.store_string(StructureIO.export_qe_input(_app._workspace.atoms, "smoke"))
		qf.close()
		var rf = FileAccess.open(qe_path, FileAccess.READ)
		var txt = rf.get_as_text() if rf else ""
		if rf:
			rf.close()
		_check(txt.find("ATOMIC_POSITIONS") >= 0, "QE 文件落盘并含坐标段")
	else:
		_check(false, "QE 文件写入失败")
	_app._reset_selection_state()
	_app._workspace.clear()

# ---------- 布局适配 (bug 回归: 窗口溢出屏幕/顶栏溢出) ----------
func _test_layout_fit():
	var usable: Rect2i = DisplayServer.screen_get_usable_rect()
	var win := DisplayServer.window_get_size()
	if win.x > 0 and win.y > 0:
		_check(win.x <= usable.size.x + 2 and win.y <= usable.size.y + 2,
			"窗口适配屏幕可用区 (%d×%d ≤ %d×%d)" % [win.x, win.y, usable.size.x, usable.size.y])
	_check(_app._top_bar_h >= 42 and _app._top_bar_h <= 160,
		"顶栏高度合理 (%d)" % _app._top_bar_h)
	_check(_app._vp_y == _app._top_bar_h + _app.UI_MARGIN * 2,
		"视口起点 = 顶栏高度 + 边距 (%d)" % _app._vp_y)
	_check(_app._vp_x == _app.LEFT_W + _app.UI_MARGIN * 2, "视口左边距对齐")
	_check(_app._vp_h + _app._vp_y + _app.UI_MARGIN == _app._screen_h - 45,
		"底栏与视口底边对齐留白")
	_check(_app._vp_h > 300, "视口高度充足 (%d)" % _app._vp_h)
	_check(_app._vp_w > 300, "视口宽度充足 (%d)" % _app._vp_w)
	_check(_app.LEFT_W >= 420 and _app.RIGHT_W >= 220, "侧栏宽度在合理范围")

# ---------- 画笔轨迹计算 ----------
func _test_brush_stroke_calc():
	_app._reset_selection_state()
	_app._workspace.clear()
	_app._clear_brush_atoms()

	# 元素标注单元测试: 两条不同元素笔划 (旧代码会将第二条笔划点错标为 H)
	var pts_a: Array = []
	var pts_b: Array = []
	for i in range(2):
		for j in range(2):
			for k in range(2):
				pts_a.append(Vector3(i * 1.6, j * 1.6, k * 1.6))
				pts_b.append(Vector3(3.0 + i * 1.6, j * 1.6, k * 1.6))
	_app._brush_strokes.append({
		"type": 0, "points": pts_a, "center": Vector3(0.8, 0.8, 0.8),
		"is_boundary": false, "element": "Nb",
		"physical_params": _app._default_physical_params(),
	})
	_app._brush_strokes.append({
		"type": 0, "points": pts_b, "center": Vector3(3.8, 0.8, 0.8),
		"is_boundary": false, "element": "Ti",
		"physical_params": _app._default_physical_params(),
	})
	var sd = _app._get_selected_stroke_data()
	var label_ok = sd["symbols"].size() == 16
	if label_ok:
		for i in range(8):
			if sd["symbols"][i] != "Nb":
				label_ok = false
		for i in range(8, 16):
			if sd["symbols"][i] != "Ti":
				label_ok = false
	_check(label_ok, "双元素笔划元素逐点正确标注")

	# 选中单条笔划时元素隔离
	_app._reset_selection_state()
	_app._selected_strokes.append(1)
	var sd2 = _app._get_selected_stroke_data()
	var ti_only = sd2["symbols"].size() == 8
	for s in sd2["symbols"]:
		if s != "Ti":
			ti_only = false
	_check(ti_only, "选中单笔划时元素隔离正确")

	# 全流程计算: 单条连通密集笔划 (满足密度条件: 连通/配位/四面体)
	_app._reset_selection_state()
	_app._clear_brush_atoms()
	var dense: Array = []
	for i in range(4):
		for j in range(2):
			for k in range(2):
				dense.append(Vector3(i * 0.4, j * 0.4, k * 0.4))
	_app._brush_strokes.append({
		"type": 0, "points": dense, "center": Vector3(0.6, 0.2, 0.2),
		"is_boundary": false, "element": "Nb",
		"physical_params": _app._default_physical_params(),
	})
	_app._refresh_brush_atom_render()
	_app._execute_calculation()
	_check(not _app._last_results.is_empty(), "画笔轨迹计算产生结果")
	_check(int(_app._last_results.get("atom_count", 0)) == 16,
		"画笔轨迹计算 16 原子 (实际 %d)" % int(_app._last_results.get("atom_count", 0)))
	_app._reset_selection_state()
	_app._clear_brush_atoms()

# ---------- 失效状态防护 ----------
func _test_stale_state_paths():
	_app._load_preset("MgB2")
	var atoms = _app._workspace.atoms.duplicate()
	for a in atoms:
		a.set_selected(true)
		_app._selected_atoms.append(a)
	_app._tag_as_molecule(atoms)
	_check(_app._molecule_groups.size() == 1, "分子标记成功")
	_app._select_molecule_group(0)
	_check(_app._selected_atoms.size() == 3, "分子组选择 3 原子")

	# 删除全部原子 → 分子组置空 → 访问不崩溃
	var all = _app._workspace.atoms.duplicate()
	for a in all:
		_app._workspace.remove_atom(a)
	_app._select_molecule_group(0)
	_check(true, "失效分子组选择无崩溃")
	_check(_app._workspace.selected_atom == null, "原子删除后 selected_atom 已清空")

	# 越界 gid 防护
	_app._select_molecule_group(99)
	_check(true, "越界分子组 gid 无崩溃")

	# 笔划索引越界防护
	_app._selected_strokes.append(50)
	_app._load_params_from_selected()
	_check(true, "越界笔划索引无崩溃")
	_app._reset_selection_state()

# ---------- 物理交互 ----------
func _test_physics_interactions():
	_app._load_preset("LaH10")
	_app._on_physics_temp_changed(300.0)
	_app._on_physics_press_changed(100.0)
	_app._on_physics_mag_changed(5.0)
	_app._on_physics_doping_changed(0.2)
	_app._on_physics_mu_star_changed(0.15)
	_app._on_pairing_changed(1)
	_check(true, "物理参数变更无崩溃")

	_app._relax_structure()
	_check(true, "结构弛豫 (力场+空间哈希) 无崩溃")
	_check(_app._workspace.atoms.size() == 11, "弛豫后原子数不变")

	_app._execute_calculation()
	_check(float(_app._last_results.get("tc_estimate", -1.0)) > 0.0, "参数调整后计算正常")
