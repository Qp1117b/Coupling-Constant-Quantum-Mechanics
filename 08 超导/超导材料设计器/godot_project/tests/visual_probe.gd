extends Node

## 可视化探针: 真实渲染窗口下实例化主场景, 生成材料/画笔形状, 截图验证 3D 显示
## 运行: Godot --path godot_project res://tests/visual_probe.tscn  (非 headless)

var _app: Node

func _ready():
	await get_tree().process_frame
	var scene = load("res://scenes/Main.tscn")
	_app = scene.instantiate()
	get_tree().root.add_child.call_deferred(_app)
	await get_tree().process_frame
	await get_tree().process_frame

	# 1. 生成第一个超导材料 (Hg) 到设计面板
	_app._sc_selector.selected = 1
	_app._generate_sc_material()
	for i in range(30):
		await get_tree().process_frame
	_shot("shot_sc_material.png")

	# 2. 大材料 YBCO 类 (取列表中间一个含 Ba/Cu/O 的)
	var scdb = SCDB.get_all()
	var idx = 0
	for i in range(scdb.size()):
		var syms: Array = []
		for a in scdb[i].atoms:
			syms.append(a.sym)
		if syms.has("Ba") and syms.has("Cu") and syms.has("O"):
			idx = i
			break
	_app._reset_selection_state()
	_app._workspace.clear()
	_app._sc_selector.selected = idx + 1
	_app._generate_sc_material()
	for i in range(30):
		await get_tree().process_frame
	_shot("shot_ybco.png")

	# 3. 底部画笔面板: 填充模式放球形晶格 (非边界 → MultiMesh 原子渲染)
	_app._reset_selection_state()
	_app._workspace.clear()
	var tmpl = _app._workspace.add_atom("Nb", 93, Vector3(0, 0, 0))
	_app._selected_atoms.append(tmpl)
	_app._toggle_brush_mode()
	_app._select_workmode_fill()
	_app._brush_shape = 0
	_app._brush_shape_size = 4.0
	_app._place_brush_shape(Vector3(0, 2, 0))
	for i in range(30):
		await get_tree().process_frame
	_shot("shot_brush.png")

	# 4. 边界模式: 蓝色边界轨迹线渲染 (修复 add_vertex 后应可见)
	_app._clear_brush_atoms()
	_app._select_workmode_boundary()
	_app._place_brush_shape(Vector3(0, 2, 0))
	for i in range(30):
		await get_tree().process_frame
	_shot("shot_boundary.png")

	print("[VISUAL-PROBE] 完成")
	get_tree().quit(0)

func _shot(fname: String):
	var img = get_viewport().get_texture().get_image()
	var path = "user://" + fname
	img.save_png(path)
	print("[VISUAL-PROBE] 已保存: %s (%s)" % [fname, ProjectSettings.globalize_path(path)])
