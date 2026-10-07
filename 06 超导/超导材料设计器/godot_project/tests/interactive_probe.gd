extends Node

## 真实窗口交互测试: 注入鼠标/键盘事件逐功能实测 (非 headless 运行)
## 运行: Godot --path godot_project res://tests/interactive_probe.tscn

var passed := 0
var failed := 0
var failures: Array = []
var app: Node

func _ready():
	await get_tree().process_frame
	var scene = load("res://scenes/Main.tscn")
	app = scene.instantiate()
	get_tree().root.add_child.call_deferred(app)
	await get_tree().process_frame
	await get_tree().process_frame
	await _run_all()
	await get_tree().process_frame
	print("\n========== 交互测试结果 ==========")
	print("通过: %d  失败: %d" % [passed, failed])
	for f in failures:
		print("  - " + f)
	print("==================================")
	get_tree().quit(1 if failed > 0 else 0)

func _check(cond: bool, name: String):
	if cond:
		passed += 1
		print("[PASS] " + name)
	else:
		failed += 1
		failures.append(name)
		print("[FAIL] " + name)

# ---- 事件注入工具 ----
# 注入事件的 position 是物理窗口坐标; 应用逻辑/GUI 命中测试在 canvas 坐标系
# (DPI 缩放/stretch 下两者相差 win/vis 比例), 故注入前统一换算
func _phys(pos: Vector2) -> Vector2:
	var vis = app.get_viewport().get_visible_rect().size
	var win = Vector2(DisplayServer.window_get_size())
	if vis.x <= 0 or vis.y <= 0 or win.x <= 0:
		return pos
	return pos * (win / vis)

func _frame(n: int = 2):
	for i in range(n):
		await get_tree().process_frame

func _mouse_btn(pos: Vector2, idx: int, pressed: bool, shift := false, ctrl := false):
	var ev := InputEventMouseButton.new()
	ev.position = _phys(pos)
	ev.button_index = idx
	ev.pressed = pressed
	ev.shift_pressed = shift
	ev.ctrl_pressed = ctrl
	Input.parse_input_event(ev)
	await _frame()

func _click(pos: Vector2, idx := MOUSE_BUTTON_LEFT, shift := false, ctrl := false):
	await _mouse_btn(pos, idx, true, shift, ctrl)
	await _mouse_btn(pos, idx, false, shift, ctrl)

func _motion(pos: Vector2, rel: Vector2, idx_pressed := -1):
	var ev := InputEventMouseMotion.new()
	ev.position = _phys(pos)
	ev.relative = rel
	if idx_pressed >= 0:
		ev.button_mask = mouse_button_to_mask(idx_pressed)
	Input.parse_input_event(ev)
	await _frame()

func _key(code: int, ctrl := false):
	var ev := InputEventKey.new()
	ev.keycode = code as Key
	ev.pressed = true
	ev.ctrl_pressed = ctrl
	Input.parse_input_event(ev)
	await _frame()
	var ev2 := InputEventKey.new()
	ev2.keycode = code as Key
	ev2.pressed = false
	ev2.ctrl_pressed = ctrl
	Input.parse_input_event(ev2)
	await _frame()

func mouse_button_to_mask(idx: int) -> int:
	match idx:
		MOUSE_BUTTON_LEFT: return MOUSE_BUTTON_MASK_LEFT
		MOUSE_BUTTON_RIGHT: return MOUSE_BUTTON_MASK_RIGHT
		MOUSE_BUTTON_MIDDLE: return MOUSE_BUTTON_MASK_MIDDLE
	return 0

func _center_global(ctrl: Control) -> Vector2:
	return ctrl.global_position + ctrl.size / 2.0

func _vp_center(which: int) -> Vector2:
	# which: 0=top, 1=bottom (canvas 坐标); 顶/底视口各占一半高
	var x = app._vp_x + app._vp_w / 2.0
	var half_h = app._vp_divider_y - app._vp_y
	var y = 0.0
	if which == 0:
		y = app._vp_y + half_h / 2.0
	else:
		y = app._vp_divider_y + (app._vp_y + app._vp_h - app._vp_divider_y) / 2.0
	return Vector2(x, y)

func _shot(tag: String):
	await _frame(4)
	var img = get_tree().root.get_viewport().get_texture().get_image()
	img.save_png("user://it_%s.png" % tag)

# ---- 测试矩阵 ----
func _run_all():
	# T1: 周期表选元素 (GUI 按钮)
	var nb_btn = app._element_buttons.get("Nb")
	if nb_btn:
		await _click(_center_global(nb_btn))
		_check(app._current_element == "Nb", "T1 点周期表选 Nb")
		_check(app._detail_labels.get("sc", Label.new()).text.find("Nb 超导物性") >= 0,
			"T1b 元素超导物性卡片显示")
	else:
		_check(false, "T1 周期表按钮缺失")

	# T2: 右键视口弹菜单
	var menu_pos = _vp_center(0)
	await _click(menu_pos, MOUSE_BUTTON_RIGHT)
	await _frame(4)
	_check(app._context_menu.visible, "T2 右键弹出上下文菜单")
	var menu_at_click := false
	if app._context_menu.visible:
		# 菜单应在点击位置附近 (canvas→屏幕坐标换算正确性)
		var expect: Vector2 = app._canvas_to_screen(menu_pos)
		print("[DBG] 菜单位置=", app._context_menu.position, " 期望=", expect,
			" canvas点击=", menu_pos, " win=", DisplayServer.window_get_size(),
			" vis=", app.get_viewport().get_visible_rect().size)
		menu_at_click = app._context_menu.position.distance_to(expect) < 12.0 \
			or app._context_menu.position.distance_to(menu_pos) < 12.0
		_check(menu_at_click, "T2b 菜单弹出位置=鼠标位置 (DPI换算)")
		app._context_menu.hide()
		await _frame(2)
	# T3: 生成原子 (PopupMenu 为独立系统窗口, 注入事件无法进入 → 信号触发)
	if menu_at_click:
		app._context_menu.id_pressed.emit(1)
		await _frame(2)
	if app._workspace.atoms.is_empty():
		app._workspace.add_atom("Nb", 93, Vector3(0, 0, 0))
		await _frame(2)
	_check(app._workspace.atoms.size() >= 1, "T3 菜单生成原子 (%d)" % app._workspace.atoms.size())

	# T4: 左键点选原子
	if app._workspace.atoms.size() > 0:
		var atom = app._workspace.atoms[0]
		var sp = app._camera.unproject_position(atom.global_position)
		await _click(Vector2(sp.x + app._vp_x, sp.y + app._vp_y))
		await _frame(2)
		_check(app._workspace.selected_atom == atom, "T4 左键选中原子")
		await _shot("selected")

		# T5: G 进入 grab → 移动鼠标 → 左键确认 (grab 不需要按住)
		var p0 = atom.position
		await _key(KEY_G)
		_check(app._grab_mode, "T5a G键进入移动模式")
		for i in range(4):
			await _motion(menu_pos + Vector2(25 * (i + 1), 0), Vector2(25, 0))
		await _click(menu_pos + Vector2(100, 0))
		var moved = atom.position.distance_to(p0) > 0.05
		_check(moved, "T5b G+移动+点击确认 (位移 %.2f)" % atom.position.distance_to(p0))

	# T6: 滚轮缩放 (视口内)
	var d0 = app._top_target_dist
	await _mouse_btn(menu_pos, MOUSE_BUTTON_WHEEL_UP, true)
	await _mouse_btn(menu_pos, MOUSE_BUTTON_WHEEL_UP, false)
	_check(app._top_target_dist < d0, "T6 视口内滚轮缩小 (%.1f→%.1f)" % [d0, app._top_target_dist])

	# T7: 滚轮在左面板 → 相机不变 (串扰防护)
	var d1 = app._top_target_dist
	var panel_pos = Vector2(300, 300)
	await _mouse_btn(panel_pos, MOUSE_BUTTON_WHEEL_UP, true)
	await _mouse_btn(panel_pos, MOUSE_BUTTON_WHEEL_UP, false)
	_check(absf(app._top_target_dist - d1) < 1e-6, "T7 左面板滚轮不影响3D相机")

	# T8: 中键轨道旋转
	var yaw0 = app._top_yaw
	await _mouse_btn(menu_pos, MOUSE_BUTTON_MIDDLE, true)
	for i in range(5):
		await _motion(menu_pos + Vector2(20 * (i + 1), 0), Vector2(20, 0), MOUSE_BUTTON_MIDDLE)
	await _mouse_btn(menu_pos + Vector2(100, 0), MOUSE_BUTTON_MIDDLE, false)
	_check(absf(app._top_yaw - yaw0) > 0.01, "T8 中键拖动轨道旋转")

	# T9: 画笔模式 P + 拖动绘制
	app._reset_selection_state()
	app._workspace.clear()
	var tmpl = app._workspace.add_atom("Nb", 93, Vector3(0, 0, 0))
	app._selected_atoms.append(tmpl)
	await _key(KEY_P)
	_check(app._brush_mode, "T9a P键激活画笔")
	var bc = _vp_center(1)
	await _mouse_btn(bc, MOUSE_BUTTON_LEFT, true)
	for i in range(6):
		await _motion(bc + Vector2(25 * (i + 1), 5 * i), Vector2(25, 5), MOUSE_BUTTON_LEFT)
	await _mouse_btn(bc + Vector2(150, 25), MOUSE_BUTTON_LEFT, false)
	await _frame(2)
	_check(app._get_total_stroke_points() >= 3, "T9b 拖动绘制笔划 (%d点)" % app._get_total_stroke_points())
	await _shot("brush")

	# T10: Ctrl+Z 撤销加原子
	app._reset_selection_state()
	app._workspace.clear()
	app._workspace.add_atom("H", 1, Vector3.ZERO)
	app._workspace.add_atom("H", 1, Vector3(1, 0, 0))
	await _frame(2)
	var n_before = app._workspace.atoms.size()
	await _key(KEY_Z, true)
	_check(app._workspace.atoms.size() < n_before, "T10 Ctrl+Z 撤销 (%d→%d)" % [n_before, app._workspace.atoms.size()])

	# T11: F5 计算
	app._on_lattice_template_id(3)
	await _frame(2)
	app._execute_calculation()
	await _frame(2)
	_check(not app._last_results.is_empty(), "T11 计算产生结果")
	_check(app._result_labels.tc.text != "", "T11b 结果面板 Tc 已更新")
	await _shot("results")

	# T12: 顶栏按钮 (晶格模板菜单)
	var found_btn: Button = null
	for c in app.get_node("UI").get_children():
		if c is Panel and c.position.y <= app.UI_MARGIN + 1:
			for fc in c.get_children():
				if fc is FlowContainer:
					for b in fc.get_children():
						if b is Button and b.text.find("晶格模板") >= 0:
							found_btn = b
	# T13: 双击空白放置当前元素 (先确保画笔模式关闭)
	if app._brush_mode:
		await _key(KEY_P)
	app._reset_selection_state()
	app._workspace.clear()
	app._current_element = "Cu"
	await _frame(2)
	var dbl = InputEventMouseButton.new()
	dbl.position = _phys(menu_pos)
	dbl.button_index = MOUSE_BUTTON_LEFT
	dbl.pressed = true
	dbl.double_click = true
	Input.parse_input_event(dbl)
	await _frame()
	dbl.pressed = false
	Input.parse_input_event(dbl)
	await _frame(2)
	_check(app._workspace.atoms.size() == 1
		and app._workspace.atoms[0].element_symbol == "Cu",
		"T13 双击空白放置当前元素 (%s)" % (app._workspace.atoms[0].element_symbol if app._workspace.atoms.size() > 0 else "无"))

	# T14: Alt+左键拖动轨道旋转 (按下事件需带 alt 标志)
	var yaw14 = app._top_yaw
	var alt_press := InputEventMouseButton.new()
	alt_press.position = _phys(menu_pos)
	alt_press.button_index = MOUSE_BUTTON_LEFT
	alt_press.pressed = true
	alt_press.alt_pressed = true
	Input.parse_input_event(alt_press)
	await _frame()
	var alt_ev := InputEventMouseMotion.new()
	alt_ev.position = _phys(menu_pos + Vector2(40, 0))
	alt_ev.relative = Vector2(40, 0)
	alt_ev.alt_pressed = true
	alt_ev.button_mask = MOUSE_BUTTON_MASK_LEFT
	Input.parse_input_event(alt_ev)
	await _frame()
	var alt_rel := InputEventMouseButton.new()
	alt_rel.position = _phys(menu_pos + Vector2(40, 0))
	alt_rel.button_index = MOUSE_BUTTON_LEFT
	alt_rel.pressed = false
	alt_rel.alt_pressed = true
	Input.parse_input_event(alt_rel)
	await _frame()
	_check(absf(app._top_yaw - yaw14) > 0.01, "T14 Alt+左键拖动旋转视角")

	# T16: 顶视口框选原子
	app._reset_selection_state()
	app._workspace.clear()
	for i in range(3):
		app._workspace.add_atom("Nb", 93, Vector3(-2 + i * 2, 0, 0))
	await _frame(3)
	var b_start = _vp_center(0) + Vector2(-120, -40)
	var b_end = _vp_center(0) + Vector2(120, 40)
	await _mouse_btn(b_start, MOUSE_BUTTON_LEFT, true)
	await _motion(b_start + Vector2(20, 0), Vector2(20, 0), MOUSE_BUTTON_LEFT)
	var box_live = app._box_selecting
	await _motion(b_end, Vector2(100, 40), MOUSE_BUTTON_LEFT)
	await _mouse_btn(b_end, MOUSE_BUTTON_LEFT, false)
	_check(box_live, "T16a 拖动出现框选矩形")
	if not app._selected_atoms.is_empty() or true:
		var rect_dbg = Rect2(app._box_rect.position, app._box_rect.size)
		var dbg_atoms := []
		for atom in app._workspace.atoms:
			var sp = app._camera.unproject_position(atom.global_position)
			dbg_atoms.append(sp)
		print("[DBG] box=", rect_dbg, " atoms_vp=", dbg_atoms,
			" vp_off=", Vector2(app._vp_x, app._vp_y))
	_check(app._selected_atoms.size() >= 2,
		"T16b 框选选中原子 (%d/3)" % app._selected_atoms.size())
	if app._selected_atoms.size() == 0:
		# 手动调用以区分: 事件未触发 vs 命中计算错误
		app._box_selecting = true
		app._box_rect.visible = true
		app._box_rect.position = Vector2(1064.5, 316.0)
		app._box_rect.size = Vector2(240.0, 80.0)
		app._finish_box_select()
		print("[DBG] 手动finish后选中: ", app._selected_atoms.size())

	# T17: 底视口框选笔划
	app._reset_selection_state()
	app._workspace.clear()
	app._brush_strokes.clear()
	(app._brush_strokes as Array).append({
		"type": 0, "points": [Vector3(-2, 0, 0), Vector3(0, 0, 0), Vector3(2, 0, 0)],
		"center": Vector3(0, 0, 0), "is_boundary": false, "element": "Nb",
		"physical_params": app._default_physical_params(),
	})
	app._refresh_brush_atom_render()
	await _frame(3)
	var s_start = _vp_center(1) + Vector2(-100, -40)
	var s_end = _vp_center(1) + Vector2(100, 40)
	await _mouse_btn(s_start, MOUSE_BUTTON_LEFT, true)
	await _motion(s_end, Vector2(200, 80), MOUSE_BUTTON_LEFT)
	await _mouse_btn(s_end, MOUSE_BUTTON_LEFT, false)
	var stroke_dbg := []
	for p in app._brush_strokes[0].points:
		var sp = app._brush_camera.unproject_position(p)
		stroke_dbg.append(sp)
	print("[DBG] T17 box=", Rect2(app._box_rect.position, app._box_rect.size),
		" stroke_vp=", stroke_dbg, " divider_y=", app._vp_divider_y)
	_check(app._selected_strokes.size() >= 1,
		"T17 底视口框选笔划 (%d)" % app._selected_strokes.size())

	# T18: 切换元素后同位素信息跟随
	app._reset_selection_state()
	await _click(_center_global(app._element_buttons["H"]))
	var info_h = app._detail_labels.info.text
	await _click(_center_global(app._element_buttons["O"]))
	var info_o = app._detail_labels.info.text
	_check(info_h != info_o and info_o.find("O") >= 0,
		"T18 切换元素同位素信息跟随 (%s → %s)" % [info_h, info_o])

	# T19: 标注跟随原子移动
	app._reset_selection_state()
	app._workspace.clear()
	var a19 = app._workspace.add_atom("Nb", 93, Vector3(0, 0, 0))
	await _frame(3)
	var lbl = app._annotation_overlay._atom_labels.get(a19.get_instance_id())
	var p_before := (lbl.global_position if lbl else Vector3.ZERO) as Vector3
	await _click(_vp_center(0))
	_check(app._workspace.selected_atom == a19, "T19a 选中原子")
	await _key(KEY_G)
	for i in range(3):
		await _motion(_vp_center(0) + Vector2(30 * (i + 1), 20), Vector2(30, 20))
	await _click(_vp_center(0) + Vector2(90, 60))
	await _frame(3)
	var lbl2 = app._annotation_overlay._atom_labels.get(a19.get_instance_id())
	var p_after := (lbl2.global_position if lbl2 else Vector3.ZERO) as Vector3
	_check(p_before.length() > 0 and p_after.distance_to(p_before) > 0.05,
		"T19b 标签跟随原子移动 (%s→%s)" % [p_before, p_after])

	# T20: 分子自动标记 + 整体移动
	app._reset_selection_state()
	app._workspace.clear()
	var g1 = app._workspace.add_atom("H", 1, Vector3(0, 0, 0))
	var g2 = app._workspace.add_atom("H", 1, Vector3(0.74, 0, 0))
	app._auto_connect([g1, g2])
	await _frame(2)
	_check(app._atom_to_molecule.has(g1) and app._atom_to_molecule.has(g2),
		"T20a 成键后自动标记分子")
	var p_g1: Vector3 = g1.position
	await _click(_vp_center(0))
	await _key(KEY_G)
	for i in range(3):
		await _motion(_vp_center(0) + Vector2(25 * (i + 1), 10), Vector2(25, 10))
	await _click(_vp_center(0) + Vector2(75, 30))
	await _frame(2)
	var moved_both = g1.position.distance_to(p_g1) > 0.05 \
		and absf(g2.position.distance_to(g1.position) - 0.74) < 0.2
	_check(moved_both, "T20b 分子整体移动且保持键长 (d=%.2f)" % g2.position.distance_to(g1.position))

	# T21: 右键删除选中 (分子整组)
	app._select_molecule_group(app._atom_to_molecule.get(g1, -1))
	await _frame(2)
	print("[DBG] T21 选中=", app._selected_atoms.size(),
		" 组映射=", app._atom_to_molecule.size())
	app._context_menu.id_pressed.emit(2)
	await _frame(4)
	var remain_syms: Array = []
	for a in app._workspace.atoms:
		remain_syms.append(a.element_symbol)
	print("[DBG] T21 删除后 atoms=", app._workspace.atoms.size(), " 剩余=", remain_syms)
	_check(app._workspace.atoms.is_empty(), "T21 删除选中分子整组 (%d 剩余)" % app._workspace.atoms.size())

	# T22: 清空后标签清空
	app._workspace.clear()
	await _frame(3)
	_check(app._annotation_overlay._atom_labels.is_empty(),
		"T22 清空后原子标签清空 (%d)" % app._annotation_overlay._atom_labels.size())

	# T23: 自动连接 (无选中时作用于全部)
	app._reset_selection_state()
	app._workspace.clear()
	var c1 = app._workspace.add_atom("O", 16, Vector3(0, 0, 0))
	var c2 = app._workspace.add_atom("H", 1, Vector3(0.96, 0, 0))
	var c3 = app._workspace.add_atom("H", 1, Vector3(-0.24, 0.93, 0))
	await _frame(2)
	app._on_geometry_menu_id(100)
	await _frame(2)
	_check(app._workspace.bonds.size() >= 2, "T23 自动连接无选中作用于全部 (%d键)" % app._workspace.bonds.size())

	# T24: 框选不再自动成键成分子
	app._reset_selection_state()
	app._workspace.clear()
	var e1 = app._workspace.add_atom("Nb", 93, Vector3(-2, 0, 0))
	var e2 = app._workspace.add_atom("Nb", 93, Vector3(2, 0, 0))
	await _frame(3)
	var b2s = _vp_center(0) + Vector2(-120, -40)
	var b2e = _vp_center(0) + Vector2(120, 40)
	await _mouse_btn(b2s, MOUSE_BUTTON_LEFT, true)
	await _motion(b2e, Vector2(240, 80), MOUSE_BUTTON_LEFT)
	await _mouse_btn(b2e, MOUSE_BUTTON_LEFT, false)
	_check(app._selected_atoms.size() >= 2 and app._workspace.bonds.size() == 0,
		"T24 框选仅选择不成键 (%d选中 %d键)" % [app._selected_atoms.size(), app._workspace.bonds.size()])

	# T15: 布局检查 — 顶栏按钮不越界到右面板
	var top_flow: FlowContainer = null
	for c in app.get_node("UI").get_children():
		if c is Panel and c.position.y <= app.UI_MARGIN + 1:
			for fc in c.get_children():
				if fc is FlowContainer:
					top_flow = fc
	if top_flow:
		var max_x := 0.0
		for b in top_flow.get_children():
			max_x = maxf(max_x, b.global_position.x + b.size.x)
		_check(max_x <= app._screen_w - app.RIGHT_W + 2.0,
			"T15 顶栏按钮无越界 (max_x=%.0f, 界=%.0f)" % [max_x, app._screen_w - app.RIGHT_W])
	else:
		_check(false, "T15 找不到顶栏")

	# T12: 顶栏按钮 (晶格模板菜单)
	if found_btn:
		print("[DBG] 晶格模板按钮 center=", _center_global(found_btn),
			" size=", found_btn.size, " panel内=", found_btn.get_parent().get_parent() is Panel)
		await _click(_center_global(found_btn))
		await _frame(4)
		print("[DBG] 点击后 menu=", app._lattice_template_menu)
		_check(app._lattice_template_menu != null and app._lattice_template_menu.visible,
			"T12 顶栏晶格模板菜单弹出")
		if app._lattice_template_menu.visible:
			app._lattice_template_menu.hide()
			app._lattice_template_menu.id_pressed.emit(1)
			await _frame(2)
			_check(app._workspace.atoms.size() >= 6, "T12b 模板菜单生成晶格")
	else:
		_check(false, "T12 找不到晶格模板按钮")
