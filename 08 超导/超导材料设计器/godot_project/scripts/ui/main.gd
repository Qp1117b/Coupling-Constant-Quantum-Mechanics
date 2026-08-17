extends Node3D
class_name MainController

var _workspace: MoleculeWorkspace
var _camera: Camera3D
var _current_element: String = "H"
var _current_isotope: int = 1

var _top_yaw: float = 0.6
var _top_pitch: float = 0.4
var _top_cam_dist: float = 18.0
var _top_target_dist: float = 18.0
var _top_pan: Vector3 = Vector3.ZERO
var _bot_yaw: float = 0.6
var _bot_pitch: float = 0.4
var _bot_cam_dist: float = 18.0
var _bot_target_dist: float = 18.0
var _bot_pan: Vector3 = Vector3.ZERO
var _active_vp: int = 0
var _is_orbiting: bool = false
var _is_panning: bool = false
var _left_down_pos: Vector2 = Vector2.ZERO
var _left_dragged: bool = false
var _right_down_pos: Vector2 = Vector2.ZERO
var _right_dragged: bool = false

var _grab_mode: bool = false
var _grab_axis: int = 0
var _grab_orig_pos: Vector3 = Vector3.ZERO
var _grab_start_screen: Vector2 = Vector2.ZERO
var _grab_init_hit: Vector3 = Vector3.ZERO
var _grab_group: Array = []  # 整体移动组: [{atom, orig}]

var _gizmo: Node3D
var _gizmo_arrows: Array = []
var _drag_axis: int = 0
var _drag_start_screen: Vector2 = Vector2.ZERO
var _drag_orig_pos: Vector3 = Vector3.ZERO
var _drag_init_hit: Vector3 = Vector3.ZERO

var _context_menu: PopupMenu
var _mol_connect_menu: PopupMenu
var _l_connect_target: Atom3D
var _menu_mouse_pos: Vector2 = Vector2.ZERO
var _box_selecting: bool = false
var _box_start: Vector2 = Vector2.ZERO
var _box_rect: ColorRect
var _rotate_mode: bool = false
var _rotate_axis: int = 0
var _rotate_start_angle: float = 0.0
var _rotate_orig_rot: Vector3 = Vector3.ZERO
var _rotate_init: bool = false
var _scale_mode: bool = false
var _scale_axis: int = 0
var _scale_orig: float = 1.0
var _scale_start_dist: float = 0.0
var _scale_init: bool = false
var _selected_atoms: Array = []
var _molecule_groups: Array = []
var _atom_to_molecule: Dictionary = {}
var _secondary_selected_atoms: Array = []
var _secondary_connect_menu: PopupMenu

var _calc_pending: bool = false
var _calc_timer: float = 0.0
const CALC_DEBOUNCE: float = 0.3

var _brush_mode: bool = false
var _brush_template: Atom3D = null
var _brush_template_syms: Array = []
var _brush_scale: int = 1
var _brush_painting: bool = false
var _brush_last_3d: Vector3 = Vector3.ZERO
var _brush_strokes: Array = []
var _current_stroke: Dictionary = {}
var _selected_strokes: Array = []
var _brush_panel_visible: bool = false
const BRUSH_SPACING: float = 1.2
const BRUSH_BOND_DIST: float = 1.8
const BRUSH_SCALE_MAX: int = 10000000000

enum BrushShape { FREE, SPHERE, PLANE, CYLINDER, TORUS, CUBE }
var _brush_shape: int = BrushShape.FREE
var _brush_shape_size: float = 3.0
var _brush_shape_density: float = 1.2
var _brush_shape_fill: bool = false
var _brush_shape_names: Array = ["自由", "球体", "平面", "圆柱", "环面", "立方体"]
var _brush_lattice_type: int = 0
var _brush_lattice_selector: OptionButton
var _brush_lattice_info_lbl: Label

enum BrushWorkMode { BOUNDARY, FILL }
var _brush_work_mode: int = BrushWorkMode.BOUNDARY
var _boundary_shapes: Array = []
var _fill_element_sym: String = "H"
var _fill_element_iso: int = 1
var _fill_density: float = 1.5

var _brush_molecule_template: Array = []
var _fill_molecule_template: Array = []
var _brush_template_name: String = ""
var _fill_template_name: String = ""

var _brush_status_lbl: Label
var _brush_template_lbl: Label
var _brush_scale_lbl: Label
var _brush_count_lbl: Label
var _brush_shape_lbl: Label
var _brush_size_lbl: Label
var _brush_density_lbl: Label
var _brush_fill_lbl: Button
var _brush_workmode_lbl: Label
var _fill_element_lbl: Label
var _fill_density_lbl: Label
var _boundary_count_lbl: Label

var _sc_selector: OptionButton
var _sc_info_lbl: Label
var _sc_gen_btn: Button
var _custom_mol_list: ItemList
var _custom_molecules: Array = []

var _brush_tube_mmi: MultiMeshInstance3D
var _brush_tube_mm: MultiMesh
var _brush_radius: float = 0.18
var _brush_radius_lbl: Label
var _brush_atom_mmi: MultiMeshInstance3D
var _brush_atom_mm: MultiMesh
var _brush_trail_mesh: ImmediateMesh
var _brush_trail_mat: StandardMaterial3D
var _brush_trail_mi: MeshInstance3D

var _brush_camera: Camera3D
var _brush_workspace: Node3D
var _top_svc: SubViewportContainer
var _bottom_svc: SubViewportContainer
var _top_sv: SubViewport
var _bottom_sv: SubViewport
var _vp_divider_y: int = 0
var _world_env: WorldEnvironment
var _vp_x: int = 0
var _vp_w: int = 0
var _vp_y: int = 0
var _vp_h: int = 0

var _physics_arrow_mi: MeshInstance3D
var _physics_arrow_mesh: ImmediateMesh
var _physics_arrow_mat: StandardMaterial3D
var _arrow_drag_mode: int = 0
var _arrow_drag_init_dir: Vector3 = Vector3.ZERO
var _arrow_hover_mode: int = 0

var _physics_panel: VBoxContainer
var _physics_temp_spin: SpinBox
var _physics_temp_slider: HSlider
var _physics_press_spin: SpinBox
var _physics_press_dir_lbl: Label
var _physics_mag_spin: SpinBox
var _physics_mag_dir_lbl: Label
var _physics_fine_container: VBoxContainer
var _physics_fine_btn: Button
var _physics_strain_spins: Array = []
var _physics_efield_spins: Array = []
var _physics_doping_spin: SpinBox
var _physics_spin_orbit_spin: SpinBox
var _physics_mu_star_spin: SpinBox
var _physics_pairing_selector: OptionButton
var _selected_group_params: Dictionary = {}


var _status_label: Label
var _element_buttons: Dictionary = {}
var _isotope_container: FlowContainer
var _detail_labels: Dictionary = {}
var _result_labels: Dictionary = {}
var _atom_labels: Dictionary = {}
var _traj_labels: Dictionary = {}

var _undo_manager: UndoManager
var _measure_mode: bool = false
var _measure_atoms: Array = []
var _measure_label: Label
var _file_dialog: FileDialog
var _file_dialog_mode: int = 0
var _undo_btn: Button
var _redo_btn: Button
var _measure_btn: Button
var _geo_window: AcceptDialog
var _geo_viewport: SubViewport
var _geo_camera: Camera3D
var _geo_label: Label
var _last_results: Dictionary = {}
var _current_material_name: String = ""

var _annotation_overlay
var _chart_plotter
var _chart_window: Window
var _show_labels_btn: Button
var _show_bond_labels_btn: Button
var _import_btn: Button
var _symmetry_btn: Button
var _chart_btn: Button
var _show_atom_labels: bool = true
var _show_bond_labels: bool = false

var _formula_label: Label

var LEFT_W: int = 680
var RIGHT_W: int = 320
var _screen_w: int = 1920
var _screen_h: int = 1080
var _top_bar_h: int = 42
const UI_MARGIN := 6  # 面板间留白: 三个面板之间有间距, 不贴边

func _ready():
	# 窗口适配屏幕: 不超过可用区 (任务栏/DPI 缩放下 1920×1080 会溢出, 底部画笔视口被裁)
	var usable: Rect2i = DisplayServer.screen_get_usable_rect()
	var win := Vector2i(mini(1920, usable.size.x), mini(1080, usable.size.y))
	if win.x < 960:
		win.x = usable.size.x
	if win.y < 600:
		win.y = usable.size.y
	DisplayServer.window_set_size(win)
	DisplayServer.window_set_position(usable.position + (usable.size - win) / 2)
	_workspace = $MoleculeWorkspace
	_camera = $CameraRig/Camera3D
	var vp = get_viewport().get_visible_rect().size
	_screen_w = int(vp.x) if vp.x >= 800 else win.x
	_screen_h = int(vp.y) if vp.y >= 600 else win.y
	# 小屏比例化侧栏宽度 (面板内容随宽度自适应)
	LEFT_W = clampi(int(_screen_w * 0.354), 420, 680)
	RIGHT_W = clampi(int(_screen_w * 0.167), 220, 320)

	_setup_ui()
	_setup_viewports()
	_setup_environment()
	_setup_grid()
	_setup_brush_trail()
	_setup_gizmo()
	_setup_context_menu()
	_setup_box_select()

	Events.connect("molecule_changed", _on_molecule_changed)
	Events.connect("molecule_cleared", _on_molecule_changed)
	Events.connect("calculation_complete", _on_results)
	Events.connect("atom_selected", _on_atom_selected)
	Events.connect("atom_removed", _on_atom_removed)

	_undo_manager = UndoManager.new()
	_undo_manager.state_changed.connect(_on_undo_state_changed)
	_setup_file_dialog()
	_annotation_overlay = AnnotationOverlay.new()
	_workspace.add_child(_annotation_overlay)

	_update_camera()
	_select_element("H")
	_take_undo_snapshot()
	var validation = DataValidator.validate_all()
	if not bool(validation.get("passed", true)):
		for e in validation.get("errors", []):
			push_error("[CQM] 数据校验: " + str(e))
		print("[CQM] 数据校验失败: %d 错误" % validation.get("errors", []).size())
	else:
		var wn = validation.get("warnings", []).size()
		print("[CQM] 数据校验通过 (警告 %d 项)" % wn)
	print("[CQM] 超导材料设计器已启动")



func _setup_viewports():
	_vp_x = LEFT_W + UI_MARGIN * 2
	_vp_w = _screen_w - LEFT_W - RIGHT_W - UI_MARGIN * 4
	_vp_y = _top_bar_h + UI_MARGIN * 2
	_vp_h = _screen_h - _top_bar_h - 45 - UI_MARGIN * 4
	var vp_x = _vp_x
	var vp_w = _vp_w
	var vp_y = _vp_y
	var vp_h = _vp_h
	var half_h = vp_h / 2
	_vp_divider_y = vp_y + half_h
	_world_env = $Lighting/WorldEnv

	_top_svc = SubViewportContainer.new()
	_top_svc.position = Vector2(vp_x, vp_y)
	_top_svc.size = Vector2(vp_w, half_h)
	_top_svc.stretch = true
	$UI.add_child(_top_svc)
	$UI.move_child(_top_svc, 0)

	_top_sv = SubViewport.new()
	_top_sv.size = Vector2i(vp_w, half_h)
	_top_sv.world_3d = World3D.new()
	_top_svc.add_child(_top_sv)

	_bottom_svc = SubViewportContainer.new()
	_bottom_svc.position = Vector2(vp_x, _vp_divider_y)
	_bottom_svc.size = Vector2(vp_w, half_h)
	_bottom_svc.stretch = true
	$UI.add_child(_bottom_svc)
	$UI.move_child(_bottom_svc, 1)

	_bottom_sv = SubViewport.new()
	_bottom_sv.size = Vector2i(vp_w, half_h)
	_bottom_sv.world_3d = World3D.new()
	_bottom_svc.add_child(_bottom_sv)

	var cam_rig = $CameraRig
	var lighting = $Lighting
	remove_child(cam_rig)
	remove_child(_workspace)
	remove_child(lighting)
	_top_sv.add_child(cam_rig)
	_top_sv.add_child(_workspace)
	_top_sv.add_child(lighting)
	_camera.make_current()

	_brush_workspace = Node3D.new()
	_bottom_sv.add_child(_brush_workspace)

	_brush_camera = Camera3D.new()
	_brush_camera.position = Vector3(0.0, 10.0, 15.0)
	_brush_camera.fov = 60.0
	_bottom_sv.add_child(_brush_camera)
	_brush_camera.make_current()
	_brush_camera.look_at(Vector3.ZERO, Vector3.UP)

	var brush_light = DirectionalLight3D.new()
	var bl_basis = Basis(Vector3(0.866, 0.25, -0.433), Vector3(0.0, 0.866, 0.5), Vector3(0.5, -0.433, 0.75))
	brush_light.transform = Transform3D(bl_basis, Vector3(5.0, 15.0, 5.0))
	brush_light.light_energy = 1.2
	_bottom_sv.add_child(brush_light)

	var brush_env = WorldEnvironment.new()
	var env = Environment.new()
	# 与顶视口一致的渲染设置 (色调映射/辉光/环境光), 仅背景色调略偏绿以区分
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.16, 0.19, 0.22, 1)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.5, 0.52, 0.58, 1)
	env.ambient_light_energy = 1.0
	env.tonemap_mode = Environment.TONE_MAPPER_ACES
	env.tonemap_exposure = 1.05
	env.tonemap_white = 6.0
	env.glow_enabled = true
	env.glow_intensity = 0.4
	env.glow_bloom = 0.05
	brush_env.environment = env
	_bottom_sv.add_child(brush_env)

	var divider = ColorRect.new()
	divider.position = Vector2(vp_x, _vp_divider_y - 1)
	divider.size = Vector2(vp_w, 2)
	divider.color = Color(0.6, 0.7, 0.9, 0.8)
	$UI.add_child(divider)

	var top_lbl = Label.new()
	top_lbl.text = "分子/原子设计"
	top_lbl.position = Vector2(vp_x + 8, vp_y + 4)
	top_lbl.add_theme_font_size_override("font_size", 13)
	top_lbl.add_theme_color_override("font_color", Color(0.7, 0.8, 0.95, 0.7))
	$UI.add_child(top_lbl)

	var bottom_lbl = Label.new()
	bottom_lbl.text = "画笔材料"
	bottom_lbl.position = Vector2(vp_x + 8, _vp_divider_y + 4)
	bottom_lbl.add_theme_font_size_override("font_size", 13)
	bottom_lbl.add_theme_color_override("font_color", Color(0.3, 0.85, 0.4, 0.7))
	$UI.add_child(bottom_lbl)

func _is_in_top_viewport(screen_pos: Vector2) -> bool:
	return screen_pos.x >= _vp_x and screen_pos.x <= _vp_x + _vp_w and screen_pos.y >= _vp_y and screen_pos.y < _vp_divider_y

func _is_in_bottom_viewport(screen_pos: Vector2) -> bool:
	return screen_pos.x >= _vp_x and screen_pos.x <= _vp_x + _vp_w and screen_pos.y >= _vp_divider_y and screen_pos.y <= _vp_y + _vp_h

func _to_top_vp_local(screen_pos: Vector2) -> Vector2:
	return Vector2(screen_pos.x - _vp_x, screen_pos.y - _vp_y)

func _to_bottom_vp_local(screen_pos: Vector2) -> Vector2:
	return Vector2(screen_pos.x - _vp_x, screen_pos.y - _vp_divider_y)

func _setup_environment():
	var env = Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.18, 0.20, 0.26, 1)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.5, 0.52, 0.58, 1)
	env.ambient_light_energy = 1.0
	# 渲染效果: ACES 色调映射 (高光过渡柔和) + 辉光
	env.tonemap_mode = Environment.TONE_MAPPER_ACES
	env.tonemap_exposure = 1.05
	env.tonemap_white = 6.0
	env.glow_enabled = true
	env.glow_intensity = 0.4
	env.glow_bloom = 0.05
	env.ssao_enabled = true
	env.ssao_intensity = 1.0
	_world_env.environment = env

## Y 轴对齐指定方向的 Basis (圆柱默认沿 Y)
func _basis_y_along(dir: Vector3) -> Basis:
	var y = dir.normalized()
	var x = y.cross(Vector3.UP)
	if x.length() < 1e-4:
		x = Vector3(1, 0, 0)
	else:
		x = x.normalized()
	var z = x.cross(y)
	return Basis(x, y, z)

## 工作区 XYZ 坐标轴: 圆柱轴身 + 锥形箭头 + Label3D 标签 (建模软件惯例)
func _add_workspace_axes(parent: Node3D, axis_len: float = 8.0):
	var axes := [
		[Vector3(1, 0, 0), Color(0.92, 0.30, 0.30), "X"],
		[Vector3(0, 1, 0), Color(0.32, 0.90, 0.40), "Y"],
		[Vector3(0, 0, 1), Color(0.35, 0.55, 0.98), "Z"],
	]
	for axis in axes:
		var dir: Vector3 = axis[0]
		var col: Color = axis[1]
		var shaft_len = axis_len * 2.0
		var shaft = MeshInstance3D.new()
		var cyl = CylinderMesh.new()
		cyl.top_radius = 0.05
		cyl.bottom_radius = 0.05
		cyl.height = shaft_len
		cyl.radial_segments = 8
		shaft.mesh = cyl
		var mat = StandardMaterial3D.new()
		mat.albedo_color = col
		mat.emission_enabled = true
		mat.emission = col
		mat.emission_energy_multiplier = 0.8
		mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		shaft.material_override = mat
		shaft.transform = Transform3D(_basis_y_along(dir), Vector3.ZERO)
		parent.add_child(shaft)
		# 箭头
		var tip = MeshInstance3D.new()
		var cone = CylinderMesh.new()
		cone.top_radius = 0.0
		cone.bottom_radius = 0.16
		cone.height = 0.5
		cone.radial_segments = 10
		tip.mesh = cone
		tip.material_override = mat
		tip.transform = Transform3D(_basis_y_along(dir), dir * (axis_len + 0.25))
		parent.add_child(tip)
		# 标签
		var lbl = Label3D.new()
		lbl.text = axis[2]
		lbl.billboard = BaseMaterial3D.BILLBOARD_ENABLED
		lbl.font_size = 48
		lbl.modulate = col
		lbl.no_depth_test = true
		lbl.position = dir * (axis_len + 0.85)
		parent.add_child(lbl)

func _setup_grid():
	var grid_mat = StandardMaterial3D.new()
	grid_mat.albedo_color = Color(0.25, 0.28, 0.35, 0.6)
	grid_mat.metallic = 0.0
	grid_mat.roughness = 0.9
	grid_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA

	var plane = PlaneMesh.new()
	plane.size = Vector2(40, 40)
	var floor_mesh = MeshInstance3D.new()
	floor_mesh.mesh = plane
	floor_mesh.material_override = grid_mat
	floor_mesh.position.y = -0.01
	_workspace.add_child(floor_mesh)

	# 次网格线 (每 1 单位) + 主网格线 (每 5 单位, 更亮)
	var minor_mat = StandardMaterial3D.new()
	minor_mat.albedo_color = Color(0.4, 0.45, 0.55, 0.4)
	minor_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	minor_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	var major_mat = StandardMaterial3D.new()
	major_mat.albedo_color = Color(0.55, 0.62, 0.78, 0.65)
	major_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	major_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED

	for i in range(-20, 21):
		var is_major = i % 5 == 0
		var mat = major_mat if is_major else minor_mat
		var line_w = 0.045 if is_major else 0.02
		var mesh_x = BoxMesh.new()
		mesh_x.size = Vector3(line_w, 0.01, 40)
		var line_x = MeshInstance3D.new()
		line_x.mesh = mesh_x
		line_x.material_override = mat
		line_x.position = Vector3(i, 0, 0)
		_workspace.add_child(line_x)

		var mesh_z = BoxMesh.new()
		mesh_z.size = Vector3(40, 0.01, line_w)
		var line_z = MeshInstance3D.new()
		line_z.mesh = mesh_z
		line_z.material_override = mat
		line_z.position = Vector3(0, 0, i)
		_workspace.add_child(line_z)

	_add_workspace_axes(_workspace, 8.0)

func _setup_brush_trail():
	# 建模式网格: 主线(每5) + 次线(每1) 双色调
	var minor_mat = StandardMaterial3D.new()
	minor_mat.albedo_color = Color(0.15, 0.25, 0.18, 0.5)
	minor_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	minor_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	var major_mat = StandardMaterial3D.new()
	major_mat.albedo_color = Color(0.25, 0.42, 0.30, 0.75)
	major_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	major_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	for i in range(-15, 16):
		var is_major = i % 5 == 0
		var mat = major_mat if is_major else minor_mat
		var line_w = 0.045 if is_major else 0.02
		var mx = BoxMesh.new()
		mx.size = Vector3(line_w, 0.01, 30)
		var lx = MeshInstance3D.new()
		lx.mesh = mx
		lx.material_override = mat
		lx.position = Vector3(i, 0, 0)
		_brush_workspace.add_child(lx)
		var mz = BoxMesh.new()
		mz.size = Vector3(30, 0.01, line_w)
		var lz = MeshInstance3D.new()
		lz.mesh = mz
		lz.material_override = mat
		lz.position = Vector3(0, 0, i)
		_brush_workspace.add_child(lz)
	_add_workspace_axes(_brush_workspace, 7.0)
	# 笔划 = 3D 管体 (MultiMesh 圆柱段, 可调粗细), 替代 2D 线段
	_brush_tube_mm = MultiMesh.new()
	_brush_tube_mm.transform_format = MultiMesh.TRANSFORM_3D
	_brush_tube_mm.use_colors = true
	var cyl = CylinderMesh.new()
	cyl.top_radius = 0.5
	cyl.bottom_radius = 0.5
	cyl.height = 1.0
	cyl.radial_segments = 10
	_brush_tube_mm.mesh = cyl
	_brush_tube_mmi = MultiMeshInstance3D.new()
	_brush_tube_mmi.multimesh = _brush_tube_mm
	var tube_mat = StandardMaterial3D.new()
	tube_mat.albedo_color = Color.WHITE
	tube_mat.vertex_color_use_as_albedo = true
	tube_mat.metallic = 0.2
	tube_mat.roughness = 0.4
	_brush_tube_mmi.material_override = tube_mat
	_brush_workspace.add_child(_brush_tube_mmi)
	_brush_tube_mm.instance_count = 0
	_brush_trail_mesh = ImmediateMesh.new()
	_brush_trail_mat = StandardMaterial3D.new()
	_brush_trail_mat.albedo_color = Color(0.3, 0.85, 0.4)
	_brush_trail_mat.emission = Color(0.3, 0.85, 0.4)
	_brush_trail_mat.emission_energy_multiplier = 1.0
	_brush_trail_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_brush_trail_mi = MeshInstance3D.new()
	_brush_trail_mi.mesh = _brush_trail_mesh
	_brush_trail_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_brush_workspace.add_child(_brush_trail_mi)
	_setup_brush_atoms()
	_setup_physics_arrows()

## 画笔原子渲染: 底部视口以 MultiMesh 实例化全部笔画点 (元素配色)
func _setup_brush_atoms():
	_brush_atom_mm = MultiMesh.new()
	_brush_atom_mm.transform_format = MultiMesh.TRANSFORM_3D
	_brush_atom_mm.use_colors = true
	var sphere = SphereMesh.new()
	sphere.radius = 1.0
	sphere.height = 2.0
	sphere.radial_segments = 16
	sphere.rings = 12
	_brush_atom_mm.mesh = sphere
	_brush_atom_mmi = MultiMeshInstance3D.new()
	_brush_atom_mmi.multimesh = _brush_atom_mm
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color.WHITE
	mat.vertex_color_use_as_albedo = true
	mat.metallic = 0.1
	mat.roughness = 0.45
	_brush_atom_mmi.material_override = mat
	_brush_workspace.add_child(_brush_atom_mmi)
	_brush_atom_mm.instance_count = 0

func _brush_element_color(element_name) -> Color:
	var sym = str(element_name)
	var data = ElementDB.get_element(sym)
	if not data.is_empty():
		return Color.from_string(str(data.get("color", "#7FE87F")), Color(0.5, 0.9, 0.5))
	return Color(0.5, 0.9, 0.5)

func _refresh_brush_atom_render():
	if _brush_atom_mm == null:
		return
	var count = 0
	for s in _brush_strokes:
		if not s.is_boundary:
			count += s.points.size()
	if not _current_stroke.is_empty() and not _current_stroke.get("is_boundary", false):
		count += _current_stroke.points.size()
	_brush_atom_mm.instance_count = 0
	if count == 0:
		return
	_brush_atom_mm.instance_count = count
	var i = 0
	for s in _brush_strokes:
		if s.is_boundary:
			continue
		var sym = s.get("element", "H")
		var col = _brush_element_color(sym)
		var r = Atom3D.compute_atom_radius(sym)
		var sc = Vector3(r, r, r)
		for p in s.points:
			_brush_atom_mm.set_instance_transform(i, Transform3D(Basis().scaled(sc), p))
			_brush_atom_mm.set_instance_color(i, col)
			i += 1
	if not _current_stroke.is_empty() and not _current_stroke.get("is_boundary", false):
		var sym_c = _current_stroke.get("element", "H")
		var col_c = _brush_element_color(sym_c)
		var r_c = Atom3D.compute_atom_radius(sym_c)
		var sc_c = Vector3(r_c, r_c, r_c)
		for p in _current_stroke.points:
			_brush_atom_mm.set_instance_transform(i, Transform3D(Basis().scaled(sc_c), p))
			_brush_atom_mm.set_instance_color(i, col_c)
			i += 1

func _setup_physics_arrows():
	_physics_arrow_mi = MeshInstance3D.new()
	_physics_arrow_mesh = ImmediateMesh.new()
	_physics_arrow_mat = StandardMaterial3D.new()
	_physics_arrow_mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	_physics_arrow_mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	_physics_arrow_mat.vertex_color_use_as_albedo = true
	_physics_arrow_mi.mesh = _physics_arrow_mesh
	_physics_arrow_mi.material_override = _physics_arrow_mat
	_brush_workspace.add_child(_physics_arrow_mi)

func _default_physical_params() -> Dictionary:
	return {
		"temperature": 4.2,
		"pressure_mag": 0.0,
		"pressure_dir": Vector3(0.0, -1.0, 0.0),
		"mag_field_mag": 0.0,
		"mag_field_dir": Vector3(0.0, 0.0, 1.0),
		"strain": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		"efield": Vector3(0.0, 0.0, 0.0),
		"doping": 0.0,
		"spin_orbit": 0.0,
		"mu_star": 0.13,
		"pairing_symmetry": 0,
	}

func _load_params_from_selected():
	if _selected_strokes.is_empty():
		_selected_group_params = _default_physical_params()
		return
	var first_idx = _selected_strokes[0]
	if first_idx < 0 or first_idx >= _brush_strokes.size():
		_selected_group_params = _default_physical_params()
		return
	var first = _brush_strokes[first_idx]
	if not first.has("physical_params"):
		first["physical_params"] = _default_physical_params()
	_selected_group_params = first.physical_params.duplicate(true)

func _sync_params_to_selected():
	for idx in _selected_strokes:
		if idx < _brush_strokes.size():
			_brush_strokes[idx]["physical_params"] = _selected_group_params.duplicate(true)

func _get_selected_strokes_center() -> Vector3:
	if _selected_strokes.is_empty():
		return Vector3.ZERO
	var sum = Vector3.ZERO
	var count = 0
	for idx in _selected_strokes:
		if idx < _brush_strokes.size():
			var pts = _brush_strokes[idx].points
			for p in pts:
				sum += p
				count += 1
	return sum / count if count > 0 else Vector3.ZERO

func _draw_physics_arrows():
	_physics_arrow_mesh.clear_surfaces()
	if _selected_strokes.is_empty():
		return
	var center = _get_selected_strokes_center()
	var p = _selected_group_params
	var temp = float(p.get("temperature", 4.2))
	var press_mag = float(p.get("pressure_mag", 0.0))
	var press_dir = p.get("pressure_dir", Vector3(0, -1, 0))
	var mag_mag = float(p.get("mag_field_mag", 0.0))
	var mag_dir = p.get("mag_field_dir", Vector3(0, 0, 1))
	var temp_radius = 0.5 + sqrt(temp) * 0.15
	_physics_arrow_mesh.surface_begin(Mesh.PRIMITIVE_LINE_STRIP)
	var n_segments = 32
	for i in range(n_segments + 1):
		var angle = TAU * i / n_segments
		var pt = center + Vector3(cos(angle), 0, sin(angle)) * temp_radius
		var col = Color(1.0, 0.3, 0.2, 0.6)
		_physics_arrow_mesh.surface_set_color(col)
		_physics_arrow_mesh.surface_add_vertex(pt)
	_physics_arrow_mesh.surface_end()
	if press_mag > 0.01:
		_draw_arrow_3d(center, press_dir.normalized(), press_mag * 0.3, Color(0.2, 0.9, 0.3, 0.9))
	if mag_mag > 0.01:
		_draw_arrow_3d(center, mag_dir.normalized(), mag_mag * 0.3, Color(0.3, 0.5, 1.0, 0.9))

func _draw_arrow_3d(origin: Vector3, dir: Vector3, length: float, color: Color):
	var tip = origin + dir * length
	var up = Vector3.UP if abs(dir.y) < 0.99 else Vector3.FORWARD
	var perp = dir.cross(up).normalized() * length * 0.15
	_physics_arrow_mesh.surface_begin(Mesh.PRIMITIVE_LINE_STRIP)
	_physics_arrow_mesh.surface_set_color(color)
	_physics_arrow_mesh.surface_add_vertex(origin)
	_physics_arrow_mesh.surface_add_vertex(tip)
	_physics_arrow_mesh.surface_end()
	_physics_arrow_mesh.surface_begin(Mesh.PRIMITIVE_TRIANGLES)
	_physics_arrow_mesh.surface_set_color(color)
	var head_base = tip - dir * length * 0.15
	var p1 = head_base + perp
	var p2 = head_base - perp
	var p3 = head_base + dir.cross(perp).normalized() * length * 0.15
	var p4 = head_base - dir.cross(perp).normalized() * length * 0.15
	_physics_arrow_mesh.surface_add_vertex(tip)
	_physics_arrow_mesh.surface_add_vertex(p1)
	_physics_arrow_mesh.surface_add_vertex(p2)
	_physics_arrow_mesh.surface_add_vertex(tip)
	_physics_arrow_mesh.surface_add_vertex(p3)
	_physics_arrow_mesh.surface_add_vertex(p4)
	_physics_arrow_mesh.surface_end()

func _check_arrow_hit(screen_pos: Vector2) -> int:
	if _selected_strokes.is_empty():
		return 0
	if not _is_in_bottom_viewport(screen_pos):
		return 0
	var center = _get_selected_strokes_center()
	var local = _to_bottom_vp_local(screen_pos)
	var p = _selected_group_params
	var press_mag = float(p.get("pressure_mag", 0.0))
	var mag_mag = float(p.get("mag_field_mag", 0.0))
	if press_mag > 0.01:
		var press_dir = p.get("pressure_dir", Vector3(0, -1, 0))
		var tip = center + press_dir.normalized() * press_mag * 0.3
		var tip_screen = _brush_camera.unproject_position(tip)
		if local.distance_to(tip_screen) < 25:
			return 1
	if mag_mag > 0.01:
		var mag_dir = p.get("mag_field_dir", Vector3(0, 0, 1))
		var tip = center + mag_dir.normalized() * mag_mag * 0.3
		var tip_screen = _brush_camera.unproject_position(tip)
		if local.distance_to(tip_screen) < 25:
			return 2
	return 0

func _update_arrow_drag(screen_pos: Vector2):
	if _arrow_drag_mode == 0:
		return
	var local = _to_bottom_vp_local(screen_pos)
	var from = _brush_camera.project_ray_origin(local)
	var dir = _brush_camera.project_ray_normal(local)
	var center = _get_selected_strokes_center()
	var to_cam = center - from
	var proj = to_cam - dir * (to_cam.dot(dir))
	var new_dir = proj.normalized() if proj.length() > 0.01 else _arrow_drag_init_dir
	if _arrow_drag_mode == 1:
		_selected_group_params["pressure_dir"] = new_dir
	elif _arrow_drag_mode == 2:
		_selected_group_params["mag_field_dir"] = new_dir
	_sync_params_to_selected()
	_update_physics_panel_dirs()

func _adjust_arrow_magnitude(mode: int, direction: int):
	if mode == 1:
		var mag = float(_selected_group_params.get("pressure_mag", 0.0))
		mag = max(0.0, mag + direction * 1.0)
		_selected_group_params["pressure_mag"] = mag
		_physics_press_spin.set_block_signals(true)
		_physics_press_spin.value = mag
		_physics_press_spin.set_block_signals(false)
	elif mode == 2:
		var mag = float(_selected_group_params.get("mag_field_mag", 0.0))
		mag = max(0.0, mag + direction * 0.1)
		_selected_group_params["mag_field_mag"] = mag
		_physics_mag_spin.set_block_signals(true)
		_physics_mag_spin.value = mag
		_physics_mag_spin.set_block_signals(false)
	_sync_params_to_selected()

func _update_brush_trail():
	_brush_trail_mesh.clear_surfaces()
	var all_strokes: Array = _brush_strokes.duplicate()
	if not _current_stroke.is_empty():
		all_strokes.append(_current_stroke)
	for idx in range(all_strokes.size()):
		var stroke = all_strokes[idx]
		var pts = stroke.points
		if pts.size() < 2:
			continue
		var base_color = Color(0.3, 0.5, 1.0) if stroke.is_boundary else Color(0.3, 0.85, 0.4)
		var is_selected = idx in _selected_strokes
		if is_selected:
			base_color = Color(1.0, 0.8, 0.2)
		var density = _stroke_density(stroke)
		var emit_energy = clamp(0.5 + density * 0.3, 0.5, 3.0)
		_brush_trail_mat.albedo_color = base_color
		_brush_trail_mat.emission = base_color
		_brush_trail_mat.emission_energy_multiplier = emit_energy
		_brush_trail_mesh.surface_begin(Mesh.PRIMITIVE_LINE_STRIP, _brush_trail_mat)
		for p in pts:
			_brush_trail_mesh.surface_add_vertex(p)
		if stroke.type != BrushShape.FREE and pts.size() > 2:
			_brush_trail_mesh.surface_add_vertex(pts[0])
		_brush_trail_mesh.surface_end()
	_update_brush_tubes()

func _update_brush_tubes():
	if not _brush_tube_mm:
		return
	var all_strokes: Array = _brush_strokes.duplicate()
	if not _current_stroke.is_empty():
		all_strokes.append(_current_stroke)
	var transforms: Array = []
	var colors: Array = []
	for idx in range(all_strokes.size()):
		var stroke = all_strokes[idx]
		var pts = stroke.get("points", [])
		if pts.size() < 2:
			continue
		var base_color = Color(0.3, 0.5, 1.0) if stroke.get("is_boundary", false) else Color(0.3, 0.85, 0.4)
		if idx in _selected_strokes:
			base_color = Color(1.0, 0.8, 0.2)
		var radius = _brush_radius
		var closed = stroke.get("type", 0) != BrushShape.FREE and pts.size() > 2
		var n = pts.size()
		var end = n if closed else n - 1
		for i in range(end):
			var a = pts[i]
			var b = pts[(i + 1) % n]
			var diff = b - a
			var length = diff.length()
			if length < 0.001:
				continue
			var dir = diff / length
			var mid = (a + b) / 2.0
			var basis = _basis_y_along(dir)
			var scaled = basis.scaled(Vector3(radius * 2.0, length, radius * 2.0))
			transforms.append(Transform3D(scaled, mid))
			colors.append(base_color)
	_brush_tube_mm.instance_count = transforms.size()
	for i in range(transforms.size()):
		_brush_tube_mm.set_instance_transform(i, transforms[i])
		_brush_tube_mm.set_instance_color(i, colors[i])

func _stroke_density(stroke: Dictionary) -> float:
	var pts = stroke.points
	var n = pts.size()
	if n < 2:
		return 0.0
	var arc_len = 0.0
	for i in range(1, n):
		arc_len += pts[i].distance_to(pts[i - 1])
	if arc_len < 1e-6:
		return float(n)
	return float(n) / arc_len

func _find_stroke_at_screen_pos(screen_pos: Vector2) -> int:
	if not _is_in_bottom_viewport(screen_pos):
		return -1
	var local = _to_bottom_vp_local(screen_pos)
	var ray_origin = _brush_camera.project_ray_origin(local)
	var ray_dir = _brush_camera.project_ray_normal(local)
	var best_idx = -1
	var best_dist = 0.3
	for idx in range(_brush_strokes.size()):
		var pts = _brush_strokes[idx].points
		for i in range(1, pts.size()):
			var d = _ray_segment_min_dist(ray_origin, ray_dir, pts[i - 1], pts[i])
			if d < best_dist:
				best_dist = d
				best_idx = idx
	return best_idx

func _ray_segment_min_dist(ray_o: Vector3, ray_d: Vector3, p1: Vector3, p2: Vector3) -> float:
	var seg = p2 - p1
	var seg_len = seg.length()
	if seg_len < 1e-6:
		return ray_o.distance_to(p1)
	var seg_d = seg / seg_len
	var cross = ray_d.cross(seg_d)
	var cross_len = cross.length()
	if cross_len < 1e-6:
		return ray_o.distance_to(p1)
	var diff = p1 - ray_o
	var dist = abs(diff.dot(cross)) / cross_len
	var t = diff.cross(seg_d).dot(cross) / (cross_len * cross_len)
	var s = ray_d.cross(diff).dot(cross) / (cross_len * cross_len)
	if t < 0.0 or t > seg_len:
		var d1 = ray_o.distance_to(p1)
		var d2 = ray_o.distance_to(p2)
		return minf(d1, d2)
	return dist

func _select_stroke(idx: int, additive: bool):
	if not additive:
		_selected_strokes.clear()
		for atom in _selected_atoms:
			atom.set_selected(false)
		_selected_atoms.clear()
	if idx >= 0 and idx < _brush_strokes.size():
		if idx in _selected_strokes:
			_selected_strokes.erase(idx)
		else:
			_selected_strokes.append(idx)
		var n = _selected_strokes.size()
		if n > 0:
			_update_status("选中%d个笔划" % n)
		else:
			_update_status("取消选中")
	_load_params_from_selected()
	_update_physics_panel()

func _box_select_strokes(rect: Rect2):
	for idx in range(_brush_strokes.size()):
		var pts = _brush_strokes[idx].points
		for p in pts:
			var sp = _brush_camera.unproject_position(p)
			var global_sp = Vector2(sp.x + _vp_x, sp.y + _vp_divider_y)
			if rect.has_point(global_sp):
				if not (idx in _selected_strokes):
					_selected_strokes.append(idx)
				break
	_load_params_from_selected()
	_update_physics_panel()

func _get_selected_stroke_points() -> Array:
	var pts: Array = []
	if _selected_strokes.is_empty():
		return _get_all_stroke_points()
	for idx in _selected_strokes:
		if idx >= 0 and idx < _brush_strokes.size():
			var s = _brush_strokes[idx]
			if not s.is_boundary:
				for p in s.points:
					pts.append(p)
	return pts

func _get_selected_stroke_data() -> Dictionary:
	var pts: Array = []
	var syms: Array = []
	if _selected_strokes.is_empty():
		for s in _brush_strokes:
			if not s.is_boundary:
				var sym = str(s.get("element", "H"))
				for p in s.points:
					pts.append(p)
					syms.append(sym)
	else:
		for idx in _selected_strokes:
			if idx >= 0 and idx < _brush_strokes.size():
				var s = _brush_strokes[idx]
				if not s.is_boundary:
					var sym = str(s.get("element", "H"))
					for p in s.points:
						pts.append(p)
						syms.append(sym)
	return {"points": pts, "symbols": syms}

func _setup_ui():
	var ui = $UI

	var left_panel = Panel.new()
	left_panel.position = Vector2(UI_MARGIN, UI_MARGIN)
	left_panel.size = Vector2(LEFT_W, _screen_h - UI_MARGIN * 2)
	left_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	var ls = StyleBoxFlat.new()
	ls.bg_color = Color(0.21, 0.24, 0.31, 1)
	ls.border_width_right = 3
	ls.border_color = Color(0.45, 0.6, 0.85, 1)
	left_panel.add_theme_stylebox_override("panel", ls)
	ui.add_child(left_panel)
	_build_left_panel(left_panel)

	var right_panel = Panel.new()
	right_panel.position = Vector2(_screen_w - RIGHT_W - UI_MARGIN, UI_MARGIN)
	right_panel.size = Vector2(RIGHT_W, _screen_h - UI_MARGIN * 2)
	var rs = StyleBoxFlat.new()
	rs.bg_color = Color(0.14, 0.16, 0.22, 1)
	rs.border_width_left = 3
	rs.border_color = Color(0.35, 0.5, 0.8, 1)
	right_panel.add_theme_stylebox_override("panel", rs)
	ui.add_child(right_panel)
	_build_right_panel(right_panel)

	var bottom_bar = Panel.new()
	bottom_bar.position = Vector2(LEFT_W + UI_MARGIN * 2, _screen_h - 45 - UI_MARGIN)
	bottom_bar.size = Vector2(_screen_w - LEFT_W - RIGHT_W - UI_MARGIN * 4, 45)
	bottom_bar.mouse_filter = Control.MOUSE_FILTER_STOP
	var bs = StyleBoxFlat.new()
	bs.bg_color = Color(0.1, 0.12, 0.18, 1)
	bs.border_width_top = 2
	bs.border_color = Color(0.3, 0.4, 0.6, 1)
	bottom_bar.add_theme_stylebox_override("panel", bs)
	ui.add_child(bottom_bar)

	_status_label = Label.new()
	_status_label.position = Vector2(10, 12)
	_status_label.size = Vector2(_screen_w - LEFT_W - RIGHT_W - UI_MARGIN * 4 - 20, 25)
	_status_label.add_theme_font_size_override("font_size", 13)
	_status_label.add_theme_color_override("font_color", Color(0.75, 0.82, 0.95))
	_status_label.text = "就绪"
	bottom_bar.add_child(_status_label)

	_measure_label = Label.new()
	_measure_label.position = Vector2(LEFT_W + 10, 50)
	_measure_label.add_theme_font_size_override("font_size", 14)
	_measure_label.add_theme_color_override("font_color", Color(0.9, 0.85, 0.3))
	_measure_label.text = ""
	ui.add_child(_measure_label)

	var top_bar = Panel.new()
	top_bar.position = Vector2(LEFT_W + UI_MARGIN * 2, UI_MARGIN)
	top_bar.size = Vector2(_screen_w - LEFT_W - RIGHT_W - UI_MARGIN * 4, 42)
	top_bar.mouse_filter = Control.MOUSE_FILTER_STOP
	var ts = StyleBoxFlat.new()
	ts.bg_color = Color(0.16, 0.18, 0.25, 1)
	ts.border_width_bottom = 2
	ts.border_color = Color(0.3, 0.4, 0.6, 1)
	top_bar.add_theme_stylebox_override("panel", ts)
	ui.add_child(top_bar)
	_build_top_bar(top_bar)
	_top_bar_h = int(top_bar.size.y)
	_measure_label.position = Vector2(LEFT_W + UI_MARGIN * 2 + 10, _top_bar_h + UI_MARGIN * 2 + 8)

func _build_left_panel(panel: Panel):
	var scroll = ScrollContainer.new()
	scroll.position = Vector2(4, 4)
	scroll.size = Vector2(LEFT_W - 8, _screen_h - UI_MARGIN * 2 - 8)
	scroll.mouse_filter = Control.MOUSE_FILTER_STOP
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	var ss = StyleBoxFlat.new()
	ss.bg_color = Color(0.21, 0.24, 0.31, 0)
	scroll.add_theme_stylebox_override("panel", ss)
	panel.add_child(scroll)

	var container = VBoxContainer.new()
	container.size = Vector2(LEFT_W - 24, 0)
	container.position = Vector2(8, 8)
	container.add_theme_constant_override("separation", 5)
	scroll.add_child(container)

	var title1 = _make_title("元素周期表", 20)
	container.add_child(title1)

	var grid = GridContainer.new()
	grid.columns = 18
	grid.add_theme_constant_override("h_separation", 3)
	grid.add_theme_constant_override("v_separation", 3)
	container.add_child(grid)
	_build_periodic_table(grid)

	var legend = _build_category_legend()
	container.add_child(legend)

	var title2 = _make_title("同位素选择", 15)
	container.add_child(title2)

	_isotope_container = FlowContainer.new()
	_isotope_container.add_theme_constant_override("h_separation", 4)
	_isotope_container.add_theme_constant_override("v_separation", 3)
	container.add_child(_isotope_container)

	for key in ["info", "neutrons", "defect", "abundance", "sc"]:
		var lbl = Label.new()
		lbl.add_theme_font_size_override("font_size", 12)
		lbl.add_theme_color_override("font_color", Color(0.75, 0.8, 0.9))
		lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		container.add_child(lbl)
		_detail_labels[key] = lbl

	_build_brush_panel_section(container)

	_build_sc_selector_section(container)

	_build_custom_mol_section(container)

	var sep_help = ColorRect.new()
	sep_help.custom_minimum_size = Vector2(LEFT_W - 40, 1)
	sep_help.color = Color(0.4, 0.5, 0.7, 0.4)
	container.add_child(sep_help)

	var title3 = _make_title("操作说明", 16)
	container.add_child(title3)

	var help = Label.new()
	help.text = "左键: 选中/框选  双击空白: 放置当前元素
点击分子=整组选中并整体移动 (G后移动,点击确认)
S+点击分子内原子=二级选中单个原子
Ctrl+左键: 多选  Alt+左键拖动: 旋转视角
右键拖动: 平移  右键点击: 菜单(删除/连接)
中键: 旋转  Shift+中键: 平移  滚轮: 缩放
G=移动 R=旋转 S=缩放  X/Y/Z=约束轴
L+点击=连接  A=全选  B=框选
P=画笔模式  Del=删除  F5=计算
成键后自动标记为分子 (结合连接见右键菜单)"
	help.add_theme_font_size_override("font_size", 12)
	help.add_theme_color_override("font_color", Color(0.8, 0.85, 0.95))
	help.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	help.custom_minimum_size = Vector2(LEFT_W - 30, 0)
	container.add_child(help)

func _make_title(text: String, size: int) -> Label:
	var lbl = Label.new()
	lbl.text = text
	lbl.add_theme_font_size_override("font_size", size)
	lbl.add_theme_color_override("font_color", Color(0.9, 0.93, 1.0))
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	return lbl

func _build_periodic_table(grid: GridContainer):
	# 单元格宽度自适应面板宽度 (18 列铺满, 避免溢出/横向滚动)
	# 可用宽度 = container宽度(LEFT_W-24) ; 18列间有17个h_sep=3的间距
	var cell_w = int((LEFT_W - 24 - 17 * 3) / 18.0)
	var cell_h = int(cell_w * 1.05)
	var layout = [
		["H","","","","","","","","","","","","","","","","","He"],
		["Li","Be","","","","","","","","","","","B","C","N","O","F","Ne"],
		["Na","Mg","","","","","","","","","","","Al","Si","P","S","Cl","Ar"],
		["K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr"],
		["Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe"],
		["Cs","Ba","","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn"],
		["Fr","Ra","","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"],
		["","","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",""],
		["","","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr",""],
	]

	for row in layout:
		for sym in row:
			if sym == "":
				var spacer = Control.new()
				spacer.custom_minimum_size = Vector2(cell_w, cell_h)
				grid.add_child(spacer)
			else:
				var btn = Button.new()
				btn.text = ""
				btn.custom_minimum_size = Vector2(cell_w, cell_h)
				btn.add_theme_constant_override("margin_left", 0)
				btn.add_theme_constant_override("margin_right", 0)
				btn.add_theme_constant_override("margin_top", 0)
				btn.add_theme_constant_override("margin_bottom", 0)

				if ElementDB.has_element(sym):
					var data = ElementDB.get_element(sym)
					var z = data.get("atomic_number", 0)
					btn.tooltip_text = "%s (Z=%d)" % [data.get("name_en",""), z]
					var cat_color = _get_category_color(sym)

					var z_lbl = Label.new()
					z_lbl.text = str(z)
					z_lbl.position = Vector2(0, 1)
					z_lbl.size = Vector2(cell_w, 12)
					z_lbl.add_theme_font_size_override("font_size", 9)
					z_lbl.add_theme_color_override("font_color", Color(1, 1, 1, 0.85))
					z_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
					btn.add_child(z_lbl)

					var sym_lbl = Label.new()
					sym_lbl.text = sym
					sym_lbl.position = Vector2(0, 12)
					sym_lbl.size = Vector2(cell_w, cell_h - 12)
					sym_lbl.add_theme_font_size_override("font_size", 14)
					sym_lbl.add_theme_color_override("font_color", Color.WHITE)
					sym_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
					sym_lbl.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
					btn.add_child(sym_lbl)

					var bg = StyleBoxFlat.new()
					bg.bg_color = cat_color
					bg.border_width_left = 2
					bg.border_width_right = 2
					bg.border_width_top = 2
					bg.border_width_bottom = 2
					bg.border_color = Color(0.1, 0.1, 0.15, 0.9)
					bg.corner_radius_top_left = 5
					bg.corner_radius_top_right = 5
					bg.corner_radius_bottom_left = 5
					bg.corner_radius_bottom_right = 5
					btn.add_theme_stylebox_override("normal", bg)

					var bg_h = StyleBoxFlat.new()
					bg_h.bg_color = cat_color.lerp(Color.WHITE, 0.35)
					bg_h.border_width_left = 2
					bg_h.border_width_right = 2
					bg_h.border_width_top = 2
					bg_h.border_width_bottom = 2
					bg_h.border_color = Color(1, 1, 1, 1)
					bg_h.corner_radius_top_left = 5
					bg_h.corner_radius_top_right = 5
					bg_h.corner_radius_bottom_left = 5
					bg_h.corner_radius_bottom_right = 5
					btn.add_theme_stylebox_override("hover", bg_h)

					var bg_p = StyleBoxFlat.new()
					bg_p.bg_color = cat_color.lerp(Color.WHITE, 0.5)
					bg_p.border_width_left = 3
					bg_p.border_width_right = 3
					bg_p.border_width_top = 3
					bg_p.border_width_bottom = 3
					bg_p.border_color = Color(1, 1, 1, 1)
					bg_p.corner_radius_top_left = 5
					bg_p.corner_radius_top_right = 5
					bg_p.corner_radius_bottom_left = 5
					bg_p.corner_radius_bottom_right = 5
					btn.add_theme_stylebox_override("pressed", bg_p)
					btn.pressed.connect(func(): _select_element(sym))
				else:
					btn.disabled = true
					btn.modulate = Color(0.35, 0.35, 0.4)

				_element_buttons[sym] = btn
				grid.add_child(btn)

func _get_category_color(sym: String) -> Color:
	var alkali = ["Li","Na","K","Rb","Cs","Fr"]
	var alkaline = ["Be","Mg","Ca","Sr","Ba","Ra"]
	var transition = ["Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn"]
	var post_trans = ["Al","Ga","In","Sn","Po","Nh","Fl","Mc","Lv"]
	var metalloid = ["B","Si","Ge","As","Sb","Te"]
	var nonmetal = ["H","C","N","O","P","S","Se"]
	var halogen = ["F","Cl","Br","I","At","Ts"]
	var noble = ["He","Ne","Ar","Kr","Xe","Rn","Og"]
	var lanthanide = ["La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"]
	var actinide = ["Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"]
	if sym in alkali: return Color(0.92, 0.28, 0.28)
	if sym in alkaline: return Color(0.92, 0.58, 0.22)
	if sym in transition: return Color(0.28, 0.52, 0.92)
	if sym in post_trans: return Color(0.32, 0.78, 0.38)
	if sym in metalloid: return Color(0.22, 0.72, 0.62)
	if sym in nonmetal: return Color(0.48, 0.82, 0.28)
	if sym in halogen: return Color(0.88, 0.78, 0.22)
	if sym in noble: return Color(0.62, 0.38, 0.88)
	if sym in lanthanide: return Color(0.88, 0.38, 0.62)
	if sym in actinide: return Color(0.72, 0.48, 0.28)
	return Color(0.5, 0.5, 0.55)

func _build_category_legend() -> FlowContainer:
	# FlowContainer 自动换行: 10 类图例在面板宽度内折行显示
	var legend = FlowContainer.new()
	legend.add_theme_constant_override("h_separation", 6)
	legend.add_theme_constant_override("v_separation", 3)
	var cats = [
		["碱金属", Color(0.92, 0.28, 0.28)],
		["碱土", Color(0.92, 0.58, 0.22)],
		["过渡", Color(0.28, 0.52, 0.92)],
		["后过渡", Color(0.32, 0.78, 0.38)],
		["类金属", Color(0.22, 0.72, 0.62)],
		["非金属", Color(0.48, 0.82, 0.28)],
		["卤素", Color(0.88, 0.78, 0.22)],
		["惰性", Color(0.62, 0.38, 0.88)],
		["镧系", Color(0.88, 0.38, 0.62)],
		["锕系", Color(0.72, 0.48, 0.28)],
	]
	for cat in cats:
		var item = HBoxContainer.new()
		item.add_theme_constant_override("separation", 3)
		var swatch = ColorRect.new()
		swatch.color = cat[1]
		swatch.custom_minimum_size = Vector2(16, 16)
		swatch.size = Vector2(16, 16)
		item.add_child(swatch)
		var lbl = Label.new()
		lbl.text = cat[0]
		lbl.add_theme_font_size_override("font_size", 12)
		lbl.add_theme_color_override("font_color", Color(0.85, 0.9, 1.0))
		item.add_child(lbl)
		legend.add_child(item)
	return legend

func _build_brush_panel_section(container: VBoxContainer):
	var sep = ColorRect.new()
	sep.custom_minimum_size = Vector2(LEFT_W - 40, 1)
	sep.color = Color(0.4, 0.5, 0.7, 0.4)
	container.add_child(sep)

	var title = _make_title("画笔设置", 16)
	container.add_child(title)

	_brush_status_lbl = Label.new()
	_brush_status_lbl.text = "画笔: 未激活 (按P切换)"
	_brush_status_lbl.add_theme_font_size_override("font_size", 12)
	_brush_status_lbl.add_theme_color_override("font_color", Color(0.7, 0.75, 0.85))
	container.add_child(_brush_status_lbl)

	_brush_template_lbl = Label.new()
	_brush_template_lbl.text = "模板: 未选择"
	_brush_template_lbl.add_theme_font_size_override("font_size", 12)
	_brush_template_lbl.add_theme_color_override("font_color", Color(0.85, 0.88, 0.95))
	container.add_child(_brush_template_lbl)

	var shape_title = Label.new()
	shape_title.text = "画笔形状:"
	shape_title.add_theme_font_size_override("font_size", 12)
	shape_title.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
	container.add_child(shape_title)

	var shape_row = HBoxContainer.new()
	shape_row.add_theme_constant_override("separation", 4)
	for i in range(BrushShape.size()):
		var btn = Button.new()
		btn.text = _brush_shape_names[i]
		btn.custom_minimum_size = Vector2(52, 26)
		btn.add_theme_font_size_override("font_size", 11)
		btn.connect("pressed", Callable(self, "_select_brush_shape").bind(i))
		shape_row.add_child(btn)
	container.add_child(shape_row)

	_brush_shape_lbl = Label.new()
	_brush_shape_lbl.text = "当前: 自由"
	_brush_shape_lbl.add_theme_font_size_override("font_size", 12)
	_brush_shape_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 0.4))
	container.add_child(_brush_shape_lbl)


	var fill_btn = Button.new()
	fill_btn.text = "填充: 仅表面"
	fill_btn.custom_minimum_size = Vector2(130, 28)
	fill_btn.add_theme_font_size_override("font_size", 12)
	fill_btn.pressed.connect(_toggle_brush_fill)
	container.add_child(fill_btn)
	_brush_fill_lbl = fill_btn

	var lattice_title = Label.new()
	lattice_title.text = "晶格分布:"
	lattice_title.add_theme_font_size_override("font_size", 12)
	lattice_title.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
	container.add_child(lattice_title)

	_brush_lattice_selector = OptionButton.new()
	for name in ChemValidator.LATTICE_NAMES:
		_brush_lattice_selector.add_item(name)
	_brush_lattice_selector.custom_minimum_size = Vector2(130, 28)
	_brush_lattice_selector.add_theme_font_size_override("font_size", 12)
	_brush_lattice_selector.item_selected.connect(_on_lattice_type_changed)
	container.add_child(_brush_lattice_selector)

	_brush_lattice_info_lbl = Label.new()
	_brush_lattice_info_lbl.text = "间距: — | 点数: —"
	_brush_lattice_info_lbl.add_theme_font_size_override("font_size", 11)
	_brush_lattice_info_lbl.add_theme_color_override("font_color", Color(0.6, 0.75, 0.6))
	container.add_child(_brush_lattice_info_lbl)

	var wm_sep = ColorRect.new()
	wm_sep.custom_minimum_size = Vector2(LEFT_W - 40, 1)
	wm_sep.color = Color(0.4, 0.5, 0.7, 0.3)
	container.add_child(wm_sep)

	var wm_title = Label.new()
	wm_title.text = "工作模式:"
	wm_title.add_theme_font_size_override("font_size", 12)
	wm_title.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
	container.add_child(wm_title)

	var wm_row = HBoxContainer.new()
	wm_row.add_theme_constant_override("separation", 6)
	var boundary_btn = Button.new()
	boundary_btn.text = "边界绘制"
	boundary_btn.custom_minimum_size = Vector2(95, 28)
	boundary_btn.add_theme_font_size_override("font_size", 12)
	boundary_btn.pressed.connect(_select_workmode_boundary)
	wm_row.add_child(boundary_btn)
	var fill_btn2 = Button.new()
	fill_btn2.text = "画桶填充"
	fill_btn2.custom_minimum_size = Vector2(95, 28)
	fill_btn2.add_theme_font_size_override("font_size", 12)
	fill_btn2.pressed.connect(_select_workmode_fill)
	wm_row.add_child(fill_btn2)
	container.add_child(wm_row)

	_brush_workmode_lbl = Label.new()
	_brush_workmode_lbl.text = "当前: 边界绘制"
	_brush_workmode_lbl.add_theme_font_size_override("font_size", 12)
	_brush_workmode_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 0.4))
	container.add_child(_brush_workmode_lbl)

	_boundary_count_lbl = Label.new()
	_boundary_count_lbl.text = "边界数: 0"
	_boundary_count_lbl.add_theme_font_size_override("font_size", 12)
	_boundary_count_lbl.add_theme_color_override("font_color", Color(0.75, 0.8, 0.9))
	container.add_child(_boundary_count_lbl)

	var fill_title = Label.new()
	fill_title.text = "填充元素 (画桶模式):"
	fill_title.add_theme_font_size_override("font_size", 12)
	fill_title.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
	container.add_child(fill_title)

	var fill_row = HBoxContainer.new()
	fill_row.add_theme_constant_override("separation", 4)
	var fill_syms = ["H", "B", "C", "N", "O", "La", "Mg", "Fe", "Se", "S"]
	for sym in fill_syms:
		var btn = Button.new()
		btn.text = sym
		btn.custom_minimum_size = Vector2(38, 26)
		btn.add_theme_font_size_override("font_size", 11)
		btn.connect("pressed", Callable(self, "_select_fill_element").bind(sym))
		fill_row.add_child(btn)
	container.add_child(fill_row)

	_fill_element_lbl = Label.new()
	_fill_element_lbl.text = "填充: H"
	_fill_element_lbl.add_theme_font_size_override("font_size", 12)
	_fill_element_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 0.4))
	container.add_child(_fill_element_lbl)

	var scale_title = Label.new()
	scale_title.text = "尺度 (1~10^10):"
	scale_title.add_theme_font_size_override("font_size", 12)
	scale_title.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
	container.add_child(scale_title)

	var scale_row = HBoxContainer.new()
	scale_row.add_theme_constant_override("separation", 6)

	var div_btn = Button.new()
	div_btn.text = "÷10"
	div_btn.custom_minimum_size = Vector2(70, 30)
	div_btn.add_theme_font_size_override("font_size", 13)
	div_btn.pressed.connect(_brush_scale_div)
	scale_row.add_child(div_btn)

	_brush_scale_lbl = Label.new()
	_brush_scale_lbl.text = "1x"
	_brush_scale_lbl.add_theme_font_size_override("font_size", 14)
	_brush_scale_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 0.4))
	_brush_scale_lbl.custom_minimum_size = Vector2(100, 30)
	_brush_scale_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	scale_row.add_child(_brush_scale_lbl)

	var mul_btn = Button.new()
	mul_btn.text = "×10"
	mul_btn.custom_minimum_size = Vector2(70, 30)
	mul_btn.add_theme_font_size_override("font_size", 13)
	mul_btn.pressed.connect(_brush_scale_mul)
	scale_row.add_child(mul_btn)

	container.add_child(scale_row)

	_brush_count_lbl = Label.new()
	_brush_count_lbl.text = "画笔点: 0 | 边界: 0"
	_brush_count_lbl.add_theme_font_size_override("font_size", 12)
	_brush_count_lbl.add_theme_color_override("font_color", Color(0.75, 0.8, 0.9))
	container.add_child(_brush_count_lbl)

	var btn_row = HBoxContainer.new()
	btn_row.add_theme_constant_override("separation", 5)

	var clr_bnd_btn = Button.new()
	clr_bnd_btn.text = "清空边界"
	clr_bnd_btn.custom_minimum_size = Vector2(85, 28)
	clr_bnd_btn.add_theme_font_size_override("font_size", 11)
	clr_bnd_btn.pressed.connect(_clear_boundaries)
	btn_row.add_child(clr_bnd_btn)

	var clear_btn = Button.new()
	clear_btn.text = "清空画笔"
	clear_btn.custom_minimum_size = Vector2(85, 28)
	clear_btn.add_theme_font_size_override("font_size", 11)
	clear_btn.pressed.connect(_clear_brush_atoms)
	btn_row.add_child(clear_btn)

	var regge_btn = Button.new()
	regge_btn.text = "计算Regge"
	regge_btn.custom_minimum_size = Vector2(90, 28)
	regge_btn.add_theme_font_size_override("font_size", 11)
	regge_btn.pressed.connect(_compute_regge)
	btn_row.add_child(regge_btn)

	container.add_child(btn_row)

	var relax_btn = Button.new()
	relax_btn.text = "弛豫结构 (力场最小化)"
	relax_btn.custom_minimum_size = Vector2(LEFT_W - 40, 30)
	relax_btn.add_theme_font_size_override("font_size", 12)
	relax_btn.pressed.connect(_relax_structure)
	container.add_child(relax_btn)

	var hint = Label.new()
	hint.text = "边界模式: 画形状定义区域(蓝)\n画桶模式: 点击边界内填充元素(绿)\n自由+边界: 拖动画蓝色边界线"
	hint.add_theme_font_size_override("font_size", 12)
	hint.add_theme_color_override("font_color", Color(0.7, 0.75, 0.85))
	container.add_child(hint)

func _build_sc_selector_section(container: VBoxContainer):
	var sep = ColorRect.new()
	sep.custom_minimum_size = Vector2(LEFT_W - 40, 1)
	sep.color = Color(0.5, 0.7, 0.9, 0.5)
	container.add_child(sep)

	var title = _make_title("超导分子选择器", 16)
	container.add_child(title)

	_sc_selector = OptionButton.new()
	_sc_selector.add_theme_font_size_override("font_size", 12)
	_sc_selector.custom_minimum_size = Vector2(LEFT_W - 40, 30)
	_sc_selector.add_item("-- 选择超导材料 --", 0)
	var sc_list = SCDB.get_all()
	for i in range(sc_list.size()):
		var m = sc_list[i]
		_sc_selector.add_item("%s (Tc=%.1fK)" % [m.name, m.tc], i + 1)
	_sc_selector.item_selected.connect(_on_sc_selected)
	container.add_child(_sc_selector)

	_sc_info_lbl = Label.new()
	_sc_info_lbl.text = ""
	_sc_info_lbl.add_theme_font_size_override("font_size", 11)
	_sc_info_lbl.add_theme_color_override("font_color", Color(0.7, 0.8, 0.9))
	_sc_info_lbl.custom_minimum_size = Vector2(LEFT_W - 40, 50)
	_sc_info_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	container.add_child(_sc_info_lbl)

	_sc_gen_btn = Button.new()
	_sc_gen_btn.text = "生成到设计面板"
	_sc_gen_btn.custom_minimum_size = Vector2(LEFT_W - 40, 32)
	_sc_gen_btn.add_theme_font_size_override("font_size", 13)
	_sc_gen_btn.disabled = true
	_sc_gen_btn.pressed.connect(_generate_sc_material)
	container.add_child(_sc_gen_btn)

func _build_custom_mol_section(container: VBoxContainer):
	var sep = ColorRect.new()
	sep.custom_minimum_size = Vector2(LEFT_W - 40, 1)
	sep.color = Color(0.4, 0.8, 0.5, 0.5)
	container.add_child(sep)

	var title = _make_title("自定义分子列表", 16)
	container.add_child(title)

	_custom_mol_list = ItemList.new()
	_custom_mol_list.custom_minimum_size = Vector2(LEFT_W - 40, 100)
	_custom_mol_list.add_theme_font_size_override("font_size", 12)
	_custom_mol_list.allow_reselect = true
	container.add_child(_custom_mol_list)

	var btn_row = HBoxContainer.new()
	btn_row.add_theme_constant_override("separation", 6)
	var gen_btn = Button.new()
	gen_btn.text = "生成"
	gen_btn.custom_minimum_size = Vector2(80, 28)
	gen_btn.add_theme_font_size_override("font_size", 12)
	gen_btn.pressed.connect(_generate_custom_mol)
	btn_row.add_child(gen_btn)
	var del_btn = Button.new()
	del_btn.text = "删除"
	del_btn.custom_minimum_size = Vector2(80, 28)
	del_btn.add_theme_font_size_override("font_size", 12)
	del_btn.pressed.connect(_delete_custom_mol)
	btn_row.add_child(del_btn)
	container.add_child(btn_row)

	var hint = Label.new()
	hint.text = "设计好分子后右键→加入自定义分子列表"
	hint.add_theme_font_size_override("font_size", 11)
	hint.add_theme_color_override("font_color", Color(0.6, 0.75, 0.65))
	container.add_child(hint)

func _on_sc_selected(idx: int):
	if idx == 0:
		_sc_info_lbl.text = ""
		_sc_gen_btn.disabled = true
		return
	var m = SCDB.get_all()[idx - 1]
	var p_str = ""
	if float(m.get("pressure_GPa", 0.0)) > 0:
		p_str = " @%.0f GPa" % float(m.get("pressure_GPa", 0.0))
	if bool(m.get("theoretical", false)):
		p_str += " [理论预测]"
	_sc_info_lbl.text = "%s\nTc = %.1f K (%d年)%s\n%s" % [m.formula, m.tc, m.year, p_str, m.desc]
	_sc_gen_btn.disabled = false

func _generate_sc_material():
	var idx = _sc_selector.selected
	if idx <= 0:
		return
	var m = SCDB.get_all()[idx - 1]
	var atoms = m.atoms
	var center = Vector3.ZERO
	for a in atoms:
		center += a.pos
	center /= max(atoms.size(), 1)
	var scale = 0.6
	var placed: Array = []
	for a in atoms:
		var pos = (a.pos - center) * scale
		pos = pos.snapped(Vector3(0.1, 0.1, 0.1))
		var atom = _workspace.add_atom(a.sym, ElementDB.most_abundant_isotope(a.sym), pos)
		placed.append(atom)
	if placed.size() >= 2:
		_auto_connect(placed)
		_auto_tag_molecules(placed)
	_current_material_name = m.name
	_update_status("生成: %s (%s, Tc=%.1fK) → %d原子" % [m.name, m.formula, m.tc, placed.size()])

func _add_to_custom_molecules():
	if _selected_atoms.is_empty():
		_update_status("请先选中分子(框选或Ctrl多选)")
		return
	var formula = _compute_formula(_selected_atoms)
	var atoms_data: Array = []
	for atom in _selected_atoms:
		atoms_data.append({
			"sym": atom.element_symbol,
			"pos": atom.position,
		})
	var mol = {
		"name": formula,
		"formula": formula,
		"atoms": atoms_data,
	}
	_custom_molecules.append(mol)
	_custom_mol_list.add_item("%s (%d原子)" % [formula, atoms_data.size()])
	_update_status("已加入自定义分子: %s (%d原子)" % [formula, atoms_data.size()])

func _generate_custom_mol():
	var sel = _custom_mol_list.get_selected_items()
	if sel.is_empty():
		_update_status("请先在列表中选择一个分子")
		return
	var idx = sel[0]
	if idx < 0 or idx >= _custom_molecules.size():
		return
	var mol = _custom_molecules[idx]
	var placed: Array = []
	for a in mol.atoms:
		var atom = _workspace.add_atom(a.sym, ElementDB.most_abundant_isotope(a.sym), a.pos)
		placed.append(atom)
	if placed.size() >= 2:
		_auto_connect(placed)
		_auto_tag_molecules(placed)
	_update_status("生成自定义分子: %s → %d原子" % [mol.formula, placed.size()])

func _delete_custom_mol():
	var sel = _custom_mol_list.get_selected_items()
	if sel.is_empty():
		_update_status("请先选择要删除的分子")
		return
	var idx = sel[0]
	_custom_molecules.remove_at(idx)
	_custom_mol_list.remove_item(idx)
	_update_status("已删除自定义分子")

func _brush_scale_mul():
	_brush_scale = min(_brush_scale * 10, BRUSH_SCALE_MAX)
	_brush_scale_lbl.text = "%dx" % _brush_scale
	_update_status("画笔尺度: %dx" % _brush_scale)

func _brush_scale_div():
	_brush_scale = max(_brush_scale / 10, 1)
	_brush_scale_lbl.text = "%dx" % _brush_scale
	_update_status("画笔尺度: %dx" % _brush_scale)

func _select_brush_shape(shape: int):
	_brush_shape = shape
	_brush_shape_lbl.text = "当前: %s" % _brush_shape_names[shape]
	var hint = "自由: 左键拖动绘制"
	match shape:
		BrushShape.SPHERE:
			hint = "球体: 左键点击放置"
		BrushShape.PLANE:
			hint = "平面: 左键点击放置"
		BrushShape.CYLINDER:
			hint = "圆柱: 左键点击放置"
		BrushShape.TORUS:
			hint = "环面: 左键点击放置"
		BrushShape.CUBE:
			hint = "立方体: 左键点击放置"
	_update_status("画笔形状: %s — %s" % [_brush_shape_names[shape], hint])

func _brush_size_inc():
	_brush_shape_size = min(_brush_shape_size + 0.5, 20.0)
	_brush_size_lbl.text = "%.1f" % _brush_shape_size

func _brush_size_dec():
	_brush_shape_size = max(_brush_shape_size - 0.5, 0.5)
	_brush_size_lbl.text = "%.1f" % _brush_shape_size

func _brush_density_inc():
	_brush_shape_density = min(_brush_shape_density + 0.2, 5.0)
	_brush_density_lbl.text = "%.2f" % _brush_shape_density

func _brush_density_dec():
	_brush_shape_density = max(_brush_shape_density - 0.2, 0.3)
	_brush_density_lbl.text = "%.2f" % _brush_shape_density

func _toggle_brush_fill():
	_brush_shape_fill = not _brush_shape_fill
	_brush_fill_lbl.text = "填充: 体积" if _brush_shape_fill else "填充: 仅表面"
	_update_status("填充模式: %s" % ("体积" if _brush_shape_fill else "仅表面"))

func _on_lattice_type_changed(idx: int):
	_brush_lattice_type = idx
	var name = ChemValidator.LATTICE_NAMES[idx]
	_update_status("晶格分布: %s" % name)

func _get_brush_element_symbol() -> String:
	if _brush_template and is_instance_valid(_brush_template):
		return _brush_template.element_symbol
	return _brush_template_name if not _brush_template_name.is_empty() else "H"

func _compute_lattice_spacing() -> float:
	var sym = _get_brush_element_symbol()
	return ChemValidator.get_lattice_spacing(sym)

func _compute_bond_dist() -> float:
	return _compute_lattice_spacing() * 1.3

func _select_workmode_boundary():
	_brush_work_mode = BrushWorkMode.BOUNDARY
	_brush_workmode_lbl.text = "当前: 边界绘制"
	_update_status("工作模式: 边界绘制 — 画形状定义区域")

func _select_workmode_fill():
	_brush_work_mode = BrushWorkMode.FILL
	_brush_workmode_lbl.text = "当前: 画桶填充"
	_update_status("工作模式: 画桶填充 — 点击边界内填充元素")

func _select_fill_element(sym: String):
	_fill_element_sym = sym
	var data = ElementDB.get_element(sym)
	_fill_element_iso = int(data.get("mass_number", 1))
	_fill_molecule_template.clear()
	_fill_template_name = ""
	_fill_element_lbl.text = "填充: %s (A=%d)" % [sym, _fill_element_iso]
	_update_status("填充元素: %s" % sym)

func _fill_density_inc():
	_fill_density = min(_fill_density + 0.2, 5.0)
	_fill_density_lbl.text = "%.2f" % _fill_density

func _fill_density_dec():
	_fill_density = max(_fill_density - 0.2, 0.3)
	_fill_density_lbl.text = "%.2f" % _fill_density

func _clear_boundaries():
	var keep: Array = []
	for s in _brush_strokes:
		if not s.is_boundary:
			keep.append(s)
	_brush_strokes = keep
	_boundary_shapes.clear()
	_boundary_count_lbl.text = "边界数: 0"
	_brush_count_lbl.text = "画笔点: %d" % _get_total_stroke_points()
	_compute_trajectory_geometry()
	_update_status("已清空所有边界")

func _extract_molecule_template(atoms: Array) -> Array:
	if atoms.is_empty():
		return []
	var center = Vector3.ZERO
	for atom in atoms:
		center += atom.global_position
	center /= atoms.size()
	var template: Array = []
	for atom in atoms:
		template.append({
			"symbol": atom.element_symbol,
			"isotope": atom.isotope_mass,
			"offset": atom.global_position - center,
		})
	return template

func _set_brush_molecule_template():
	if _selected_atoms.is_empty():
		_update_status("请先选中原子或分子")
		return
	_brush_molecule_template = _extract_molecule_template(_selected_atoms)
	var syms: Array = []
	for entry in _brush_molecule_template:
		syms.append(entry.symbol)
	_brush_template_name = ""
	for s in syms:
		_brush_template_name += s
	_brush_template_lbl.text = "分子模板: %s (%d原子)" % [_brush_template_name, _brush_molecule_template.size()]
	_brush_mode = true
	_brush_status_lbl.text = "画笔: 已激活 (分子模板)"
	_brush_status_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 0.4))
	_update_status("画笔分子模板: %s (%d原子)" % [_brush_template_name, _brush_molecule_template.size()])

func _set_fill_molecule_template():
	if _selected_atoms.is_empty():
		_update_status("请先选中原子或分子")
		return
	_fill_molecule_template = _extract_molecule_template(_selected_atoms)
	var syms: Array = []
	for entry in _fill_molecule_template:
		syms.append(entry.symbol)
	_fill_template_name = ""
	for s in syms:
		_fill_template_name += s
	_fill_element_lbl.text = "填充分子: %s (%d原子)" % [_fill_template_name, _fill_molecule_template.size()]
	_update_status("画桶分子模板: %s (%d原子)" % [_fill_template_name, _fill_molecule_template.size()])

func _place_molecule_at(template: Array, center: Vector3, as_boundary: bool) -> Array:
	var placed: Array = []
	for entry in template:
		var pos = center + entry.offset
		placed.append(pos)
	return placed

func _toggle_brush_mode():
	if _brush_mode and _selected_atoms.is_empty():
		_brush_mode = false
		_brush_painting = false
		_brush_status_lbl.text = "画笔: 未激活 (按P切换)"
		_brush_status_lbl.add_theme_color_override("font_color", Color(0.7, 0.75, 0.85))
		_update_status("画笔模式关闭")
		return

	if _selected_atoms.is_empty():
		_update_status("请先选择一个原子作为画笔模板")
		return

	_brush_template = _selected_atoms[0]
	_brush_template_syms = []
	_brush_molecule_template.clear()
	_brush_template_name = ""
	for atom in _selected_atoms:
		_brush_template_syms.append(atom.element_symbol)

	_brush_mode = true
	_brush_status_lbl.text = "画笔: 已激活 (左键拖动绘制)"
	_brush_status_lbl.add_theme_color_override("font_color", Color(0.3, 0.9, 0.4))

	if _brush_template_syms.size() == 1:
		_brush_template_lbl.text = "模板: %s" % _brush_template_syms[0]
	else:
		_brush_template_lbl.text = "模板: %s" % str(_brush_template_syms)

	_update_status("画笔源切换: %s" % str(_brush_template_syms))

func _start_brush_paint(screen_pos: Vector2):
	if not _brush_mode:
		return
	if not _brush_template and _brush_molecule_template.is_empty():
		return
	var pos3d = _project_mouse_to_brush_plane(screen_pos)
	if pos3d == null:
		return
	if _brush_work_mode == BrushWorkMode.FILL:
		_fill_boundary(pos3d)
		return
	if _brush_shape == BrushShape.FREE:
		_brush_painting = true
		_brush_last_3d = pos3d
		_current_stroke = {
			"type": BrushShape.FREE,
			"points": [pos3d],
			"center": pos3d,
			"size": 0.0,
			"is_boundary": _brush_work_mode == BrushWorkMode.BOUNDARY,
			"element": _brush_template.element_symbol if _brush_template else _brush_template_name,
			"physical_params": _default_physical_params(),
		}
	else:
		_place_brush_shape(pos3d)

func _update_brush_paint(screen_pos: Vector2):
	if not _brush_painting or not _brush_mode:
		return
	var pos3d = _project_mouse_to_brush_plane(screen_pos)
	if pos3d == null:
		return
	var dist = pos3d.distance_to(_brush_last_3d)
	var lattice_spacing = _compute_lattice_spacing()
	if lattice_spacing < 0.1:
		lattice_spacing = BRUSH_SPACING
	if dist >= lattice_spacing:
		var dir = (pos3d - _brush_last_3d).normalized()
		var steps = int(dist / lattice_spacing)
		for i in range(1, steps + 1):
			var place_pos = _brush_last_3d + dir * lattice_spacing * i
			_current_stroke.points.append(place_pos)
		_brush_last_3d = pos3d
		_brush_count_lbl.text = "画笔点: %d" % _get_total_stroke_points()
		_refresh_brush_atom_render()

func _stop_brush_paint():
	if _brush_painting and not _current_stroke.is_empty():
		_brush_strokes.append(_current_stroke)
		_current_stroke = {}
	_brush_painting = false
	_refresh_brush_atom_render()

func _get_total_stroke_points() -> int:
	var total = 0
	for s in _brush_strokes:
		total += s.points.size()
	if not _current_stroke.is_empty():
		total += _current_stroke.points.size()
	return total

func _place_brush_shape(center: Vector3):
	var pts = _gen_lattice_in_shape(center)
	var stroke = {
		"type": _brush_shape,
		"points": pts,
		"center": center,
		"size": _brush_shape_size,
		"is_boundary": _brush_work_mode == BrushWorkMode.BOUNDARY,
		"element": _brush_template.element_symbol if _brush_template else _brush_template_name,
		"physical_params": _default_physical_params(),
	}
	_brush_strokes.append(stroke)
	if _brush_work_mode == BrushWorkMode.BOUNDARY:
		_boundary_shapes.append({
			"type": _brush_shape,
			"center": center,
			"size": _brush_shape_size,
			"stroke_idx": _brush_strokes.size() - 1,
		})
		_boundary_count_lbl.text = "边界数: %d" % _boundary_shapes.size()
	_brush_count_lbl.text = "画笔点: %d" % _get_total_stroke_points()
	var spacing = _compute_lattice_spacing()
	_brush_lattice_info_lbl.text = "间距: %.2f | 点数: %d" % [spacing, pts.size()]
	_refresh_brush_atom_render()
	_compute_trajectory_geometry()
	_update_status("放置%s: %d点" % [_brush_shape_names[_brush_shape], pts.size()])

func _gen_lattice_in_shape(center: Vector3) -> Array:
	var spacing = _compute_lattice_spacing()
	if spacing < 0.1:
		spacing = 0.5
	var size = _brush_shape_size
	var raw_pts = ChemValidator.gen_lattice_points(_brush_lattice_type, size, spacing, center)
	var pts: Array = []
	var surface_tol = spacing * 0.5
	for p in raw_pts:
		var local = p - center
		var inside = false
		var on_surface = false
		match _brush_shape:
			BrushShape.SPHERE:
				var d = local.length()
				inside = d <= size
				on_surface = abs(d - size) < surface_tol
			BrushShape.PLANE:
				var cam_basis = _brush_camera.global_transform.basis
				var u_dist = abs(local.dot(cam_basis.x))
				var v_dist = abs(local.dot(cam_basis.y))
				var r = sqrt(u_dist * u_dist + v_dist * v_dist)
				inside = r <= size
				on_surface = abs(r - size) < surface_tol
			BrushShape.CYLINDER:
				var r = sqrt(local.x * local.x + local.z * local.z)
				var h = size * 1.5
				inside = r <= size and abs(local.y) <= h / 2.0
				on_surface = (abs(r - size) < surface_tol and abs(local.y) <= h / 2.0) or (r <= size and abs(abs(local.y) - h / 2.0) < surface_tol)
			BrushShape.TORUS:
				var R = size
				var r_minor = size * 0.3
				var xz = Vector2(local.x, local.z)
				var tube_d = abs(xz.length() - R)
				var d = sqrt(tube_d * tube_d + local.y * local.y)
				inside = d <= r_minor
				on_surface = abs(d - r_minor) < surface_tol
			BrushShape.CUBE:
				inside = abs(local.x) <= size and abs(local.y) <= size and abs(local.z) <= size
				on_surface = (abs(abs(local.x) - size) < surface_tol and abs(local.y) <= size and abs(local.z) <= size) or (abs(local.x) <= size and abs(abs(local.y) - size) < surface_tol and abs(local.z) <= size) or (abs(local.x) <= size and abs(local.y) <= size and abs(abs(local.z) - size) < surface_tol)
			_:
				inside = local.length() <= size
				on_surface = abs(local.length() - size) < surface_tol
		if inside and (_brush_shape_fill or on_surface):
			pts.append(p)
	if pts.size() < ChemValidator.TARGET_MIN_POINTS:
		pts = raw_pts
	return pts

func _gen_sphere_points(center: Vector3) -> Array:
	var r = _brush_shape_size
	var spacing = _brush_shape_density
	var pts: Array = []
	if _brush_shape_fill:
		var n_r = max(int(r / spacing), 1)
		for ir in range(1, n_r + 1):
			var rr = r * float(ir) / n_r
			var n_phi = max(int(2.0 * PI * rr / spacing), 3)
			for i in range(n_phi):
				var phi = PI * float(i) / n_phi
				var n_theta = max(int(2.0 * PI * sin(phi) * rr / spacing + 1), 3)
				for j in range(n_theta):
					var theta = 2.0 * PI * float(j) / n_theta
					pts.append(center + Vector3(
						rr * sin(phi) * cos(theta),
						rr * cos(phi),
						rr * sin(phi) * sin(theta)
					))
	else:
		var n_phi = max(int(PI * r / spacing), 3)
		for i in range(1, n_phi):
			var phi = PI * float(i) / n_phi
			var n_theta = max(int(2.0 * PI * sin(phi) * r / spacing + 1), 3)
			for j in range(n_theta):
				var theta = 2.0 * PI * float(j) / n_theta
				pts.append(center + Vector3(
					r * sin(phi) * cos(theta),
					r * cos(phi),
					r * sin(phi) * sin(theta)
				))
	return pts

func _gen_plane_points(center: Vector3) -> Array:
	var r = _brush_shape_size
	var spacing = _brush_shape_density
	var pts: Array = []
	var cam_basis = _brush_camera.global_transform.basis
	var u = cam_basis.x
	var v = cam_basis.y
	var n_side = max(int(r / spacing), 1)
	for i in range(-n_side, n_side + 1):
		for j in range(-n_side, n_side + 1):
			var pu = u * (i * spacing)
			var pv = v * (j * spacing)
			if pu.length() + pv.length() <= r:
				pts.append(center + pu + pv)
	return pts

func _gen_cylinder_points(center: Vector3) -> Array:
	var r = _brush_shape_size
	var h = _brush_shape_size * 1.5
	var spacing = _brush_shape_density
	var pts: Array = []
	var n_h = max(int(h / spacing), 1)
	var n_theta = max(int(2.0 * PI * r / spacing), 3)
	for i in range(n_h + 1):
		var y = -h / 2.0 + h * float(i) / n_h
		for j in range(n_theta):
			var theta = 2.0 * PI * float(j) / n_theta
			pts.append(center + Vector3(r * cos(theta), y, r * sin(theta)))
	if _brush_shape_fill:
		var n_r = max(int(r / spacing), 1)
		for i in range(1, n_h):
			var y = -h / 2.0 + h * float(i) / n_h
			for ir in range(1, n_r):
				var rr = r * float(ir) / n_r
				var n_t2 = max(int(2.0 * PI * rr / spacing), 3)
				for j in range(n_t2):
					var theta = 2.0 * PI * float(j) / n_t2
					pts.append(center + Vector3(rr * cos(theta), y, rr * sin(theta)))
	return pts

func _gen_torus_points(center: Vector3) -> Array:
	var R = _brush_shape_size
	var r = _brush_shape_size * 0.3
	var spacing = _brush_shape_density
	var pts: Array = []
	var n_u = max(int(2.0 * PI * R / spacing), 3)
	var n_v = max(int(2.0 * PI * r / spacing), 3)
	for i in range(n_u):
		var u = 2.0 * PI * float(i) / n_u
		for j in range(n_v):
			var v_ang = 2.0 * PI * float(j) / n_v
			pts.append(center + Vector3(
				(R + r * cos(v_ang)) * cos(u),
				r * sin(v_ang),
				(R + r * cos(v_ang)) * sin(u)
			))
	return pts

func _gen_cube_points(center: Vector3) -> Array:
	var s = _brush_shape_size
	var spacing = _brush_shape_density
	var pts: Array = []
	var n_side = max(int(s / spacing), 1)
	if _brush_shape_fill:
		for i in range(-n_side, n_side + 1):
			for j in range(-n_side, n_side + 1):
				for k in range(-n_side, n_side + 1):
					pts.append(center + Vector3(i * spacing, j * spacing, k * spacing))
	else:
		for i in range(-n_side, n_side + 1):
			for j in range(-n_side, n_side + 1):
				var x = i * spacing
				var y = j * spacing
				pts.append(center + Vector3(x, y, -s))
				pts.append(center + Vector3(x, y, s))
				pts.append(center + Vector3(x, -s, y))
				pts.append(center + Vector3(x, s, y))
				pts.append(center + Vector3(-s, x, y))
				pts.append(center + Vector3(s, x, y))
	return pts

func _project_mouse_to_brush_plane(screen_pos: Vector2) -> Variant:
	if not _is_in_bottom_viewport(screen_pos):
		return null
	var local = _to_bottom_vp_local(screen_pos)
	var from = _brush_camera.project_ray_origin(local)
	var dir = _brush_camera.project_ray_normal(local)
	var cam_dir = _brush_camera.global_transform.basis.z
	var t = (_bot_pan - from).dot(cam_dir) / dir.dot(cam_dir)
	if t < 0:
		return null
	return from + dir * t

func _fill_boundary(click_pos: Vector3):
	var target_shape: Dictionary = {}
	for shape in _boundary_shapes:
		if _is_point_in_boundary(click_pos, shape):
			target_shape = shape
			break
	if target_shape.is_empty():
		_update_status("点击点不在任何边界内")
		return

	var pts = _gen_fill_points(target_shape)
	var fill_pts: Array = []
	for p in pts:
		fill_pts.append(p)
	var stroke = {
		"type": target_shape.type,
		"points": fill_pts,
		"center": target_shape.center,
		"size": target_shape.size,
		"is_boundary": false,
		"element": _fill_element_sym if _fill_molecule_template.is_empty() else _fill_template_name,
		"physical_params": _default_physical_params(),
	}
	_brush_strokes.append(stroke)
	_brush_count_lbl.text = "画笔点: %d" % _get_total_stroke_points()
	_refresh_brush_atom_render()
	_compute_trajectory_geometry()
	var elem_name = _fill_template_name if not _fill_molecule_template.is_empty() else _fill_element_sym
	_update_status("填充%s: %d个%s点" % [_brush_shape_names[target_shape.type], fill_pts.size(), elem_name])

func _is_point_in_boundary(pt: Vector3, shape: Dictionary) -> bool:
	var center = shape.center
	var size = shape.size
	match shape.type:
		BrushShape.SPHERE:
			return pt.distance_to(center) < size
		BrushShape.CUBE:
			return abs(pt.x - center.x) < size and abs(pt.y - center.y) < size and abs(pt.z - center.z) < size
		BrushShape.CYLINDER:
			var h = size * 1.5
			var dy = abs(pt.y - center.y)
			var dr = sqrt((pt.x - center.x) ** 2 + (pt.z - center.z) ** 2)
			return dy < h / 2.0 and dr < size
		BrushShape.TORUS:
			var R = size
			var r = size * 0.3
			var dx = pt.x - center.x
			var dy = pt.y - center.y
			var dz = pt.z - center.z
			var dist_to_ring = sqrt((sqrt(dx * dx + dz * dz) - R) ** 2 + dy * dy)
			return dist_to_ring < r
		BrushShape.PLANE:
			var cam_basis = _brush_camera.global_transform.basis
			var local = pt - center
			var u_dist = abs(local.dot(cam_basis.x))
			var v_dist = abs(local.dot(cam_basis.y))
			return u_dist < size and v_dist < size
		_:
			return false

func _gen_fill_points(shape: Dictionary) -> Array:
	var center = shape.center
	var size = shape.size
	var spacing = _fill_density
	var pts: Array = []
	match shape.type:
		BrushShape.SPHERE:
			var n_r = max(int(size / spacing), 1)
			for ir in range(1, n_r + 1):
				var rr = size * float(ir) / n_r
				var n_phi = max(int(PI * rr / spacing), 2)
				for i in range(1, n_phi):
					var phi = PI * float(i) / n_phi
					var n_theta = max(int(2.0 * PI * sin(phi) * rr / spacing + 1), 3)
					for j in range(n_theta):
						var theta = 2.0 * PI * float(j) / n_theta
						pts.append(center + Vector3(
							rr * sin(phi) * cos(theta),
							rr * cos(phi),
							rr * sin(phi) * sin(theta)
						))
		BrushShape.CUBE:
			var n_side = max(int(size / spacing), 1)
			for i in range(-n_side + 1, n_side):
				for j in range(-n_side + 1, n_side):
					for k in range(-n_side + 1, n_side):
						pts.append(center + Vector3(i * spacing, j * spacing, k * spacing))
		BrushShape.CYLINDER:
			var h = size * 1.5
			var n_h = max(int(h / spacing), 1)
			var n_r = max(int(size / spacing), 1)
			for i in range(1, n_h):
				var y = -h / 2.0 + h * float(i) / n_h
				for ir in range(1, n_r):
					var rr = size * float(ir) / n_r
					var n_t = max(int(2.0 * PI * rr / spacing), 3)
					for j in range(n_t):
						var theta = 2.0 * PI * float(j) / n_t
						pts.append(center + Vector3(rr * cos(theta), y, rr * sin(theta)))
		BrushShape.TORUS:
			var R = size
			var r = size * 0.3
			var n_u = max(int(2.0 * PI * R / spacing), 3)
			var n_v = max(int(2.0 * PI * r / spacing), 3)
			var n_r = max(int(r / spacing * 0.5), 1)
			for i in range(n_u):
				var u = 2.0 * PI * float(i) / n_u
				for ir in range(1, n_r + 1):
					var rr = r * float(ir) / n_r
					for j in range(n_v):
						var v_ang = 2.0 * PI * float(j) / n_v
						pts.append(center + Vector3(
							(R + rr * cos(v_ang)) * cos(u),
							rr * sin(v_ang),
							(R + rr * cos(v_ang)) * sin(u)
						))
		BrushShape.PLANE:
			var cam_basis = _brush_camera.global_transform.basis
			var u = cam_basis.x
			var v = cam_basis.y
			var n_side = max(int(size / spacing), 1)
			for i in range(-n_side + 1, n_side):
				for j in range(-n_side + 1, n_side):
					pts.append(center + u * (i * spacing) + v * (j * spacing))
	return pts

func _auto_bond_brush_atom(atom: Atom3D):
	var data = ElementDB.get_element(atom.element_symbol)
	var r_a = float(data.get("covalent_radius_pm", 50)) / 100.0
	for other in _workspace.atoms:
		if other == atom:
			continue
		var dist = atom.global_position.distance_to(other.global_position)
		var data_b = ElementDB.get_element(other.element_symbol)
		var r_b = float(data_b.get("covalent_radius_pm", 50)) / 100.0
		var bond_range = (r_a + r_b) * 1.3
		if dist < bond_range and dist > 0.1:
			_workspace.add_bond(atom, other, 1)

func _clear_brush_atoms():
	_brush_strokes.clear()
	_current_stroke = {}
	_selected_strokes.clear()
	_boundary_shapes.clear()
	_brush_count_lbl.text = "画笔点: 0"
	_boundary_count_lbl.text = "边界数: 0"
	_refresh_brush_atom_render()
	_load_params_from_selected()
	_update_physics_panel()
	_compute_trajectory_geometry()
	_update_status("已清空画笔轨迹和边界")

func _get_all_stroke_points() -> Array:
	var pts: Array = []
	for s in _brush_strokes:
		if not s.is_boundary:
			for p in s.points:
				pts.append(p)
	return pts

func _gen_bonds_from_points(pts: Array, threshold: float) -> Array:
	var bonds: Array = []
	for i in range(pts.size()):
		for j in range(i + 1, pts.size()):
			if pts[i].distance_to(pts[j]) < threshold:
				bonds.append([i, j])
	return bonds

func _compute_regge():
	var pts = _get_selected_stroke_points()
	if pts.size() < 4:
		_update_status("画笔点不足(<4)，无法计算Regge")
		return
	var bond_pairs = _gen_bonds_from_points(pts, _compute_bond_dist())
	var result = ReggeCalculator.compute_regge_3d(pts, bond_pairs, _brush_scale)
	Events.emit_signal("calculation_complete", _build_regge_results(result))
	_update_status("Regge: S=%.6f | 四面体:%d | 边:%d" % [result.regge_action, result.tetrahedra_count, result.edge_count])

func _build_regge_results(regge: Dictionary) -> Dictionary:
	return {
		"verdict": "brush_material",
		"tc_estimate": 0.0,
		"confidence": 0.0,
		"spectral_gap": 0.0,
		"coupling": 0.0,
		"causal_cutoff_temp": 0.0,
		"eigenvalues": [],
		"order_parameters": [],
		"atom_count": _get_total_stroke_points(),
		"bond_count": 0,
		"regge": regge,
	}

func _build_right_panel(panel: Panel):
	panel.mouse_filter = Control.MOUSE_FILTER_STOP
	# 滚动容器: 内容超出屏幕高度时可滚动查看全部结果
	var scroll = ScrollContainer.new()
	scroll.position = Vector2(6, 6)
	scroll.size = Vector2(RIGHT_W - 12, _screen_h - UI_MARGIN * 2 - 12)
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	panel.add_child(scroll)
	var container = VBoxContainer.new()
	container.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	container.add_theme_constant_override("separation", 6)
	scroll.add_child(container)

	var title1 = _make_title("原子/分子属性", 16)
	container.add_child(title1)

	_formula_label = Label.new()
	_formula_label.text = "化学式: —"
	_formula_label.add_theme_font_size_override("font_size", 14)
	_formula_label.add_theme_color_override("font_color", Color(0.9, 0.85, 0.5))
	_formula_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	container.add_child(_formula_label)

	var sep1 = ColorRect.new()
	sep1.custom_minimum_size = Vector2(RIGHT_W - 20, 1)
	sep1.color = Color(0.4, 0.5, 0.7, 0.5)
	container.add_child(sep1)

	var atom_props = GridContainer.new()
	atom_props.columns = 2
	atom_props.add_theme_constant_override("h_separation", 8)
	atom_props.add_theme_constant_override("v_separation", 4)
	container.add_child(atom_props)

	var atom_prop_list = [
		["symbol", "元素"], ["z", "原子序数"],
		["mass", "质量数"], ["neutrons", "中子数"],
		["defect", "中子亏格"], ["cartan", "Cartan本征值"],
		["bond_count", "键数"], ["bond_info", "键长/角"],
		["regge", "离散Regge"], ["spec_gap", "谱间隙"],
		["brush", "画笔材料"], ["scale", "尺度"],
		["config", "构型"], ["mol_dim", "矩阵维数"],
	]
	for item in atom_prop_list:
		var key = item[0]
		var name_lbl = Label.new()
		name_lbl.text = item[1] + ":"
		name_lbl.add_theme_font_size_override("font_size", 12)
		name_lbl.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
		atom_props.add_child(name_lbl)
		var val_lbl = Label.new()
		val_lbl.add_theme_font_size_override("font_size", 12)
		val_lbl.add_theme_color_override("font_color", Color(0.85, 0.88, 0.95))
		atom_props.add_child(val_lbl)
		_atom_labels[key] = val_lbl

	_atom_labels.symbol.text = "—"

	var sep_a = ColorRect.new()
	sep_a.custom_minimum_size = Vector2(RIGHT_W - 20, 2)
	sep_a.color = Color(0.5, 0.6, 0.8, 0.6)
	container.add_child(sep_a)

	var title2 = _make_title("超导属性", 16)
	container.add_child(title2)

	var sep2 = ColorRect.new()
	sep2.custom_minimum_size = Vector2(RIGHT_W - 20, 1)
	sep2.color = Color(0.4, 0.5, 0.7, 0.5)
	container.add_child(sep2)

	var props = GridContainer.new()
	props.columns = 2
	props.add_theme_constant_override("h_separation", 8)
	props.add_theme_constant_override("v_separation", 4)
	container.add_child(props)

	var prop_list = [
		["verdict", "判定"], ["tc", "Tc (K)"],
		["confidence", "置信度"], ["gap", "谱间隙"],
		["coupling", "耦合常数"], ["causal_t", "因果截断T"],
		["order_params", "序参量"], ["atoms_bonds", "原子/键"],
	]
	for item in prop_list:
		var key = item[0]
		var name_lbl = Label.new()
		name_lbl.text = item[1] + ":"
		name_lbl.add_theme_font_size_override("font_size", 12)
		name_lbl.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
		props.add_child(name_lbl)
		var val_lbl = Label.new()
		val_lbl.add_theme_font_size_override("font_size", 12)
		val_lbl.add_theme_color_override("font_color", Color(0.85, 0.88, 0.95))
		props.add_child(val_lbl)
		_result_labels[key] = val_lbl

	_result_labels.verdict.text = "未计算"
	_result_labels.verdict.add_theme_font_size_override("font_size", 13)

	var sep3 = ColorRect.new()
	sep3.custom_minimum_size = Vector2(RIGHT_W - 20, 1)
	sep3.color = Color(0.4, 0.5, 0.7, 0.5)
	container.add_child(sep3)

	var ev_title = _make_title("Regge / A₄ 详情", 14)
	container.add_child(ev_title)
	var ev_lbl = Label.new()
	ev_lbl.add_theme_font_size_override("font_size", 11)
	ev_lbl.add_theme_color_override("font_color", Color(0.75, 0.8, 0.9))
	ev_lbl.add_theme_constant_override("lines_spacing", 2)
	ev_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	ev_lbl.custom_minimum_size = Vector2(RIGHT_W - 24, 0)
	container.add_child(ev_lbl)
	_result_labels["eigenvals"] = ev_lbl

	var sep4 = ColorRect.new()
	sep4.custom_minimum_size = Vector2(RIGHT_W - 20, 1)
	sep4.color = Color(0.4, 0.5, 0.7, 0.5)
	container.add_child(sep4)

	var traj_title = _make_title("轨迹几何特征", 14)
	container.add_child(traj_title)

	var traj_props = GridContainer.new()
	traj_props.columns = 2
	traj_props.add_theme_constant_override("h_separation", 8)
	traj_props.add_theme_constant_override("v_separation", 4)
	container.add_child(traj_props)

	var traj_prop_list = [
		["topology", "拓扑类型"], ["arc_len", "总弧长"],
		["end_dist", "端点距离"], ["compact", "紧致度"],
		["avg_curv", "平均曲率"], ["max_curv", "最大曲率"],
		["avg_tors", "平均挠率"], ["bbox", "包围盒"],
		["branches", "分支点"], ["tortuosity", "曲折度"],
	]
	for item in traj_prop_list:
		var key = item[0]
		var name_lbl = Label.new()
		name_lbl.text = item[1] + ":"
		name_lbl.add_theme_font_size_override("font_size", 12)
		name_lbl.add_theme_color_override("font_color", Color(0.65, 0.7, 0.8))
		traj_props.add_child(name_lbl)
		var val_lbl = Label.new()
		val_lbl.add_theme_font_size_override("font_size", 12)
		val_lbl.add_theme_color_override("font_color", Color(0.85, 0.88, 0.95))
		traj_props.add_child(val_lbl)
		_traj_labels[key] = val_lbl

	_traj_labels.topology.text = "—"

	var traj_detail_lbl = Label.new()
	traj_detail_lbl.add_theme_font_size_override("font_size", 12)
	traj_detail_lbl.add_theme_color_override("font_color", Color(0.75, 0.8, 0.9))
	traj_detail_lbl.add_theme_constant_override("lines_spacing", 2)
	container.add_child(traj_detail_lbl)
	_traj_labels["detail"] = traj_detail_lbl
	_build_physics_panel_section(container)

func _build_physics_panel_section(container: VBoxContainer):
	var sep5 = ColorRect.new()
	sep5.custom_minimum_size = Vector2(RIGHT_W - 20, 2)
	sep5.color = Color(0.5, 0.6, 0.8, 0.6)
	container.add_child(sep5)

	var title = _make_title("物理环境参数", 15)
	container.add_child(title)
	_physics_panel = VBoxContainer.new()
	_physics_panel.add_theme_constant_override("separation", 4)
	container.add_child(_physics_panel)
	var temp_lbl = Label.new()
	temp_lbl.text = "温度 (K)"
	temp_lbl.add_theme_font_size_override("font_size", 12)
	temp_lbl.add_theme_color_override("font_color", Color(0.8, 0.5, 0.4))
	_physics_panel.add_child(temp_lbl)
	var temp_hbox = HBoxContainer.new()
	temp_hbox.add_theme_constant_override("separation", 4)
	_physics_panel.add_child(temp_hbox)
	_physics_temp_spin = SpinBox.new()
	_physics_temp_spin.min_value = 0.0
	_physics_temp_spin.max_value = 2000.0
	_physics_temp_spin.step = 0.1
	_physics_temp_spin.value = 4.2
	_physics_temp_spin.custom_minimum_size = Vector2(80, 24)
	_physics_temp_spin.value_changed.connect(_on_physics_temp_changed)
	temp_hbox.add_child(_physics_temp_spin)
	_physics_temp_slider = HSlider.new()
	_physics_temp_slider.min_value = 0.0
	_physics_temp_slider.max_value = 300.0
	_physics_temp_slider.step = 0.1
	_physics_temp_slider.value = 4.2
	_physics_temp_slider.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	_physics_temp_slider.value_changed.connect(_on_physics_temp_slider_changed)
	temp_hbox.add_child(_physics_temp_slider)
	var preset_hbox = HBoxContainer.new()
	preset_hbox.add_theme_constant_override("separation", 4)
	_physics_panel.add_child(preset_hbox)
	for preset in [["4.2K", 4.2], ["77K", 77.0], ["300K", 300.0]]:
		var btn = Button.new()
		btn.text = preset[0]
		btn.custom_minimum_size = Vector2(50, 24)
		btn.add_theme_font_size_override("font_size", 11)
		var temp_val = preset[1]
		btn.pressed.connect(func(): _set_physics_temp(temp_val))
		preset_hbox.add_child(btn)
	var press_lbl = Label.new()
	press_lbl.text = "压强 (GPa)"
	press_lbl.add_theme_font_size_override("font_size", 12)
	press_lbl.add_theme_color_override("font_color", Color(0.4, 0.8, 0.4))
	_physics_panel.add_child(press_lbl)
	var press_hbox = HBoxContainer.new()
	press_hbox.add_theme_constant_override("separation", 4)
	_physics_panel.add_child(press_hbox)
	_physics_press_spin = SpinBox.new()
	_physics_press_spin.min_value = 0.0
	_physics_press_spin.max_value = 500.0
	_physics_press_spin.step = 0.1
	_physics_press_spin.value = 0.0
	_physics_press_spin.custom_minimum_size = Vector2(80, 24)
	_physics_press_spin.value_changed.connect(_on_physics_press_changed)
	press_hbox.add_child(_physics_press_spin)
	_physics_press_dir_lbl = Label.new()
	_physics_press_dir_lbl.text = "方向: ↓ (0,-1,0)"
	_physics_press_dir_lbl.add_theme_font_size_override("font_size", 11)
	_physics_press_dir_lbl.add_theme_color_override("font_color", Color(0.6, 0.75, 0.6))
	_physics_press_dir_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	press_hbox.add_child(_physics_press_dir_lbl)
	var mag_lbl = Label.new()
	mag_lbl.text = "磁场 (T)"
	mag_lbl.add_theme_font_size_override("font_size", 12)
	mag_lbl.add_theme_color_override("font_color", Color(0.4, 0.5, 0.9))
	_physics_panel.add_child(mag_lbl)
	var mag_hbox = HBoxContainer.new()
	mag_hbox.add_theme_constant_override("separation", 4)
	_physics_panel.add_child(mag_hbox)
	_physics_mag_spin = SpinBox.new()
	_physics_mag_spin.min_value = 0.0
	_physics_mag_spin.max_value = 50.0
	_physics_mag_spin.step = 0.01
	_physics_mag_spin.value = 0.0
	_physics_mag_spin.custom_minimum_size = Vector2(80, 24)
	_physics_mag_spin.value_changed.connect(_on_physics_mag_changed)
	mag_hbox.add_child(_physics_mag_spin)
	_physics_mag_dir_lbl = Label.new()
	_physics_mag_dir_lbl.text = "方向: → (0,0,1)"
	_physics_mag_dir_lbl.add_theme_font_size_override("font_size", 11)
	_physics_mag_dir_lbl.add_theme_color_override("font_color", Color(0.5, 0.6, 0.85))
	_physics_mag_dir_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	mag_hbox.add_child(_physics_mag_dir_lbl)
	_physics_fine_btn = Button.new()
	_physics_fine_btn.text = "▶ 精细设置"
	_physics_fine_btn.add_theme_font_size_override("font_size", 12)
	_physics_fine_btn.pressed.connect(_toggle_physics_fine)
	_physics_panel.add_child(_physics_fine_btn)
	_physics_fine_container = VBoxContainer.new()
	_physics_fine_container.add_theme_constant_override("separation", 3)
	_physics_fine_container.visible = false
	_physics_panel.add_child(_physics_fine_container)
	var strain_lbl = Label.new()
	strain_lbl.text = "应变张量 (xx,yy,zz,xy,xz,yz)"
	strain_lbl.add_theme_font_size_override("font_size", 11)
	strain_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.8))
	_physics_fine_container.add_child(strain_lbl)
	var strain_grid = GridContainer.new()
	strain_grid.columns = 3
	strain_grid.add_theme_constant_override("h_separation", 3)
	strain_grid.add_theme_constant_override("v_separation", 2)
	_physics_fine_container.add_child(strain_grid)
	for i in range(6):
		var spin = SpinBox.new()
		spin.min_value = -1.0
		spin.max_value = 1.0
		spin.step = 0.001
		spin.value = 0.0
		spin.custom_minimum_size = Vector2(70, 22)
		var idx = i
		spin.value_changed.connect(func(v): _on_physics_strain_changed(idx, v))
		strain_grid.add_child(spin)
		_physics_strain_spins.append(spin)
	var efield_lbl = Label.new()
	efield_lbl.text = "电场 (V/m)"
	efield_lbl.add_theme_font_size_override("font_size", 11)
	efield_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.8))
	_physics_fine_container.add_child(efield_lbl)
	var efield_hbox = HBoxContainer.new()
	efield_hbox.add_theme_constant_override("separation", 3)
	_physics_fine_container.add_child(efield_hbox)
	for i in range(3):
		var spin = SpinBox.new()
		spin.min_value = -1000.0
		spin.max_value = 1000.0
		spin.step = 0.1
		spin.value = 0.0
		spin.custom_minimum_size = Vector2(70, 22)
		var idx = i
		spin.value_changed.connect(func(v): _on_physics_efield_changed(idx, v))
		efield_hbox.add_child(spin)
		_physics_efield_spins.append(spin)
	var doping_lbl = Label.new()
	doping_lbl.text = "掺杂浓度"
	doping_lbl.add_theme_font_size_override("font_size", 11)
	doping_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.8))
	_physics_fine_container.add_child(doping_lbl)
	_physics_doping_spin = SpinBox.new()
	_physics_doping_spin.min_value = -1.0
	_physics_doping_spin.max_value = 1.0
	_physics_doping_spin.step = 0.001
	_physics_doping_spin.value = 0.0
	_physics_doping_spin.custom_minimum_size = Vector2(100, 22)
	_physics_doping_spin.value_changed.connect(_on_physics_doping_changed)
	_physics_fine_container.add_child(_physics_doping_spin)
	var so_lbl = Label.new()
	so_lbl.text = "自旋轨道耦合"
	so_lbl.add_theme_font_size_override("font_size", 11)
	so_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.8))
	_physics_fine_container.add_child(so_lbl)
	_physics_spin_orbit_spin = SpinBox.new()
	_physics_spin_orbit_spin.min_value = 0.0
	_physics_spin_orbit_spin.max_value = 1.0
	_physics_spin_orbit_spin.step = 0.001
	_physics_spin_orbit_spin.value = 0.0
	_physics_spin_orbit_spin.custom_minimum_size = Vector2(100, 22)
	_physics_spin_orbit_spin.value_changed.connect(_on_physics_spin_orbit_changed)
	_physics_fine_container.add_child(_physics_spin_orbit_spin)
	var mu_lbl = Label.new()
	mu_lbl.text = "库仑赝势 μ*"
	mu_lbl.add_theme_font_size_override("font_size", 11)
	mu_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.8))
	_physics_fine_container.add_child(mu_lbl)
	_physics_mu_star_spin = SpinBox.new()
	_physics_mu_star_spin.min_value = 0.0
	_physics_mu_star_spin.max_value = 0.5
	_physics_mu_star_spin.step = 0.01
	_physics_mu_star_spin.value = 0.13
	_physics_mu_star_spin.custom_minimum_size = Vector2(100, 22)
	_physics_mu_star_spin.value_changed.connect(_on_physics_mu_star_changed)
	_physics_fine_container.add_child(_physics_mu_star_spin)
	var pair_lbl = Label.new()
	pair_lbl.text = "配对对称性"
	pair_lbl.add_theme_font_size_override("font_size", 12)
	pair_lbl.add_theme_color_override("font_color", Color(0.7, 0.8, 0.9))
	_physics_panel.add_child(pair_lbl)
	_physics_pairing_selector = OptionButton.new()
	for name in CQMCalculator.PAIRING_NAMES:
		_physics_pairing_selector.add_item(name)
	_physics_pairing_selector.custom_minimum_size = Vector2(130, 28)
	_physics_pairing_selector.add_theme_font_size_override("font_size", 12)
	_physics_pairing_selector.item_selected.connect(_on_pairing_changed)
	_physics_panel.add_child(_physics_pairing_selector)
	_physics_panel.visible = false

func _toggle_physics_fine():
	_physics_fine_container.visible = not _physics_fine_container.visible
	_physics_fine_btn.text = "▼ 精细设置" if _physics_fine_container.visible else "▶ 精细设置"

func _set_physics_temp(val: float):
	_physics_temp_spin.value = val
	_physics_temp_slider.value = val

func _on_physics_temp_changed(val: float):
	_selected_group_params["temperature"] = val
	if abs(_physics_temp_slider.value - val) > 0.01:
		_physics_temp_slider.value = val
	_sync_params_to_selected()

func _on_physics_temp_slider_changed(val: float):
	_physics_temp_spin.value = val

func _on_physics_press_changed(val: float):
	_selected_group_params["pressure_mag"] = val
	_sync_params_to_selected()

func _on_physics_mag_changed(val: float):
	_selected_group_params["mag_field_mag"] = val
	_sync_params_to_selected()

func _on_physics_strain_changed(idx: int, val: float):
	var strain = _selected_group_params.get("strain", [0.0,0.0,0.0,0.0,0.0,0.0])
	strain[idx] = val
	_selected_group_params["strain"] = strain
	_sync_params_to_selected()

func _on_physics_efield_changed(idx: int, val: float):
	var ef = _selected_group_params.get("efield", Vector3.ZERO)
	match idx:
		0: ef.x = val
		1: ef.y = val
		2: ef.z = val
	_selected_group_params["efield"] = ef
	_sync_params_to_selected()

func _on_physics_doping_changed(val: float):
	_selected_group_params["doping"] = val
	_sync_params_to_selected()

func _on_physics_spin_orbit_changed(val: float):
	_selected_group_params["spin_orbit"] = val
	_sync_params_to_selected()

func _on_physics_mu_star_changed(val: float):
	_selected_group_params["mu_star"] = val
	_sync_params_to_selected()

func _on_pairing_changed(idx: int):
	_selected_group_params["pairing_symmetry"] = idx
	_sync_params_to_selected()

func _relax_structure():
	if _selected_atoms.is_empty():
		_update_status("请先选中原子再弛豫")
		return
	var bond_pairs: Array = []
	for i in range(_selected_atoms.size()):
		for j in range(i + 1, _selected_atoms.size()):
			var dist = _selected_atoms[i].position.distance_to(_selected_atoms[j].position)
			var sym_a = _selected_atoms[i].element_symbol
			var sym_b = _selected_atoms[j].element_symbol
			var r_a = float(ElementDB.get_element(sym_a).get("covalent_radius_pm", 50)) / 100.0
			var r_b = float(ElementDB.get_element(sym_b).get("covalent_radius_pm", 50)) / 100.0
			if dist <= (r_a + r_b) * 1.3:
				bond_pairs.append([i, j])
	var bonds = ForceField.build_bonds_with_ideal(_selected_atoms, bond_pairs)
	var angles = ForceField.build_angles_from_bonds(_selected_atoms, bonds)
	var result = ForceField.minimize(_selected_atoms, bonds, angles)
	_update_annotations()  # 弛豫后标签跟随新位置
	_update_status("弛豫: %s | %d步 | E=%.6f | F=%.6f" % [
		"收敛" if result.converged else "未收敛",
		result.iterations, result.final_energy, result.max_force
	])

func _update_physics_panel():
	var has_selection = not _selected_strokes.is_empty()
	_physics_panel.visible = has_selection
	if not has_selection:
		return
	var p = _selected_group_params
	_physics_temp_spin.set_block_signals(true)
	_physics_temp_spin.value = float(p.get("temperature", 4.2))
	_physics_temp_spin.set_block_signals(false)
	_physics_temp_slider.set_block_signals(true)
	_physics_temp_slider.value = clamp(float(p.get("temperature", 4.2)), 0.0, 300.0)
	_physics_temp_slider.set_block_signals(false)
	_physics_press_spin.set_block_signals(true)
	_physics_press_spin.value = float(p.get("pressure_mag", 0.0))
	_physics_press_spin.set_block_signals(false)
	_physics_mag_spin.set_block_signals(true)
	_physics_mag_spin.value = float(p.get("mag_field_mag", 0.0))
	_physics_mag_spin.set_block_signals(false)
	var strain = p.get("strain", [0.0,0.0,0.0,0.0,0.0,0.0])
	for i in range(min(6, _physics_strain_spins.size())):
		_physics_strain_spins[i].set_block_signals(true)
		_physics_strain_spins[i].value = float(strain[i])
		_physics_strain_spins[i].set_block_signals(false)
	var ef = p.get("efield", Vector3.ZERO)
	var ef_vals = [ef.x, ef.y, ef.z]
	for i in range(min(3, _physics_efield_spins.size())):
		_physics_efield_spins[i].set_block_signals(true)
		_physics_efield_spins[i].value = float(ef_vals[i])
		_physics_efield_spins[i].set_block_signals(false)
	_physics_doping_spin.set_block_signals(true)
	_physics_doping_spin.value = float(p.get("doping", 0.0))
	_physics_doping_spin.set_block_signals(false)
	_physics_spin_orbit_spin.set_block_signals(true)
	_physics_spin_orbit_spin.value = float(p.get("spin_orbit", 0.0))
	_physics_spin_orbit_spin.set_block_signals(false)
	_physics_mu_star_spin.set_block_signals(true)
	_physics_mu_star_spin.value = float(p.get("mu_star", 0.13))
	_physics_mu_star_spin.set_block_signals(false)
	var pairing_idx = int(p.get("pairing_symmetry", CQMCalculator.PairingSymmetry.S_WAVE))
	pairing_idx = clamp(pairing_idx, 0, CQMCalculator.PAIRING_NAMES.size() - 1)
	_physics_pairing_selector.set_block_signals(true)
	_physics_pairing_selector.selected = pairing_idx
	_physics_pairing_selector.set_block_signals(false)
	_update_physics_panel_dirs()

func _update_physics_panel_dirs():
	var pd = _selected_group_params.get("pressure_dir", Vector3(0,-1,0))
	_physics_press_dir_lbl.text = "方向: (%.2f,%.2f,%.2f)" % [pd.x, pd.y, pd.z]
	var md = _selected_group_params.get("mag_field_dir", Vector3(0,0,1))
	_physics_mag_dir_lbl.text = "方向: (%.2f,%.2f,%.2f)" % [md.x, md.y, md.z]

func _build_top_bar(panel: Panel):
	# FlowContainer 自动换行: 按钮总数超过视口宽度时折行, 不再溢出到右侧面板
	var hbox = FlowContainer.new()
	hbox.position = Vector2(10, 5)
	hbox.add_theme_constant_override("h_separation", 6)
	hbox.add_theme_constant_override("v_separation", 4)
	panel.add_child(hbox)


	var calc_btn = Button.new()
	calc_btn.text = "计算 (F5)"
	calc_btn.custom_minimum_size = Vector2(90, 30)
	calc_btn.add_theme_font_size_override("font_size", 12)
	calc_btn.pressed.connect(_execute_calculation)
	hbox.add_child(calc_btn)

	var clear_btn = Button.new()
	clear_btn.text = "清空"
	clear_btn.custom_minimum_size = Vector2(60, 30)
	clear_btn.add_theme_font_size_override("font_size", 12)
	clear_btn.pressed.connect(func(): _reset_selection_state(); _workspace.clear(); _take_undo_snapshot())
	hbox.add_child(clear_btn)

	var sep1 = _make_toolbar_sep()
	hbox.add_child(sep1)

	_undo_btn = Button.new()
	_undo_btn.text = "撤销 (Ctrl+Z)"
	_undo_btn.custom_minimum_size = Vector2(100, 30)
	_undo_btn.add_theme_font_size_override("font_size", 12)
	_undo_btn.disabled = true
	_undo_btn.pressed.connect(_do_undo)
	hbox.add_child(_undo_btn)

	_redo_btn = Button.new()
	_redo_btn.text = "重做 (Ctrl+Y)"
	_redo_btn.custom_minimum_size = Vector2(100, 30)
	_redo_btn.add_theme_font_size_override("font_size", 12)
	_redo_btn.disabled = true
	_redo_btn.pressed.connect(_do_redo)
	hbox.add_child(_redo_btn)

	var sep2 = _make_toolbar_sep()
	hbox.add_child(sep2)

	_measure_btn = Button.new()
	_measure_btn.text = "测量 (M)"
	_measure_btn.custom_minimum_size = Vector2(90, 30)
	_measure_btn.add_theme_font_size_override("font_size", 12)
	_measure_btn.pressed.connect(_toggle_measure_mode)
	hbox.add_child(_measure_btn)

	var sep3 = _make_toolbar_sep()
	hbox.add_child(sep3)

	var save_btn = Button.new()
	save_btn.text = "保存 (Ctrl+S)"
	save_btn.custom_minimum_size = Vector2(100, 30)
	save_btn.add_theme_font_size_override("font_size", 12)
	save_btn.pressed.connect(_save_project_dialog)
	hbox.add_child(save_btn)

	var load_btn = Button.new()
	load_btn.text = "加载 (Ctrl+O)"
	load_btn.custom_minimum_size = Vector2(100, 30)
	load_btn.add_theme_font_size_override("font_size", 12)
	load_btn.pressed.connect(_load_project_dialog)
	hbox.add_child(load_btn)

	var export_btn = Button.new()
	export_btn.text = "导出"
	export_btn.custom_minimum_size = Vector2(70, 30)
	export_btn.add_theme_font_size_override("font_size", 12)
	export_btn.pressed.connect(_export_dialog)
	hbox.add_child(export_btn)

	var sep4 = _make_toolbar_sep()
	hbox.add_child(sep4)

	var geo_btn = Button.new()
	geo_btn.text = "等效几何"
	geo_btn.custom_minimum_size = Vector2(90, 30)
	geo_btn.add_theme_font_size_override("font_size", 12)
	geo_btn.pressed.connect(_show_geometry_window)
	hbox.add_child(geo_btn)

	var sep5 = _make_toolbar_sep()
	hbox.add_child(sep5)

	_import_btn = Button.new()
	_import_btn.text = "导入"
	_import_btn.custom_minimum_size = Vector2(70, 30)
	_import_btn.add_theme_font_size_override("font_size", 12)
	_import_btn.pressed.connect(_import_structure_dialog)
	hbox.add_child(_import_btn)

	_symmetry_btn = Button.new()
	_symmetry_btn.text = "对称性"
	_symmetry_btn.custom_minimum_size = Vector2(80, 30)
	_symmetry_btn.add_theme_font_size_override("font_size", 12)
	_symmetry_btn.pressed.connect(_detect_symmetry)
	hbox.add_child(_symmetry_btn)

	_chart_btn = Button.new()
	_chart_btn.text = "图表"
	_chart_btn.custom_minimum_size = Vector2(70, 30)
	_chart_btn.add_theme_font_size_override("font_size", 12)
	_chart_btn.pressed.connect(_show_chart_window)
	hbox.add_child(_chart_btn)

	var sweep_btn = Button.new()
	sweep_btn.text = "扫描"
	sweep_btn.custom_minimum_size = Vector2(70, 30)
	sweep_btn.add_theme_font_size_override("font_size", 12)
	sweep_btn.pressed.connect(_show_sweep_window)
	hbox.add_child(sweep_btn)

	var sep6 = _make_toolbar_sep()
	hbox.add_child(sep6)

	var template_btn = Button.new()
	template_btn.text = "晶格模板"
	template_btn.custom_minimum_size = Vector2(90, 30)
	template_btn.add_theme_font_size_override("font_size", 12)
	template_btn.pressed.connect(_show_lattice_template_menu)
	hbox.add_child(template_btn)

	var supercell_btn = Button.new()
	supercell_btn.text = "超胞"
	supercell_btn.custom_minimum_size = Vector2(70, 30)
	supercell_btn.add_theme_font_size_override("font_size", 12)
	supercell_btn.pressed.connect(_show_supercell_dialog)
	hbox.add_child(supercell_btn)

	_show_labels_btn = Button.new()
	_show_labels_btn.text = "原子标签"
	_show_labels_btn.custom_minimum_size = Vector2(90, 30)
	_show_labels_btn.add_theme_font_size_override("font_size", 12)
	_show_labels_btn.toggle_mode = true
	_show_labels_btn.button_pressed = _show_atom_labels
	_show_labels_btn.pressed.connect(_toggle_atom_labels)
	hbox.add_child(_show_labels_btn)

	_show_bond_labels_btn = Button.new()
	_show_bond_labels_btn.text = "键长标注"
	_show_bond_labels_btn.custom_minimum_size = Vector2(90, 30)
	_show_bond_labels_btn.add_theme_font_size_override("font_size", 12)
	_show_bond_labels_btn.toggle_mode = true
	_show_bond_labels_btn.button_pressed = _show_bond_labels
	_show_bond_labels_btn.pressed.connect(_toggle_bond_labels)
	hbox.add_child(_show_bond_labels_btn)

	# 预估换行行数设置顶栏高度 (FlowContainer 的 minimum size 不反映换行)
	var avail = maxf(panel.size.x - 20.0, 100.0)
	var row_x := 0.0
	var rows := 1
	for btn in hbox.get_children():
		var bw = btn.get_combined_minimum_size().x + 6.0
		if row_x > 0.0 and row_x + bw > avail:
			rows += 1
			row_x = 0.0
		row_x += bw
	var bar_h = clampi(rows * 34 + 10, 42, 160)
	panel.size = Vector2(panel.size.x, bar_h)
	hbox.size = Vector2(panel.size.x - 20, bar_h - 10)

func _make_toolbar_sep() -> VSeparator:
	var sep = VSeparator.new()
	sep.add_theme_constant_override("separation", 4)
	return sep

# === 晶格模板库 (GaussView 片段库范式) ===

var _lattice_template_menu: PopupMenu

func _show_lattice_template_menu():
	if _lattice_template_menu == null:
		_lattice_template_menu = PopupMenu.new()
		_lattice_template_menu.add_item("BCC 体心立方 (当前元素)", 1)
		_lattice_template_menu.add_item("FCC 面心立方 (当前元素)", 2)
		_lattice_template_menu.add_item("钙钛矿 ABO₃ (SrTiO₃)", 3)
		_lattice_template_menu.add_item("CuO₂ 平面 (铜氧面)", 4)
		_lattice_template_menu.add_item("金刚石结构 (当前元素)", 5)
		_lattice_template_menu.add_item("石墨烯片 (当前元素)", 6)
		_lattice_template_menu.id_pressed.connect(_on_lattice_template_id)
		$UI.add_child(_lattice_template_menu)
	_lattice_template_menu.popup_centered()

func _on_lattice_template_id(id: int):
	_reset_selection_state()
	_workspace.clear()
	var sym = _current_element
	var iso = ElementDB.most_abundant_isotope(sym)
	var placed: Array = []
	match id:
		1:  # BCC: a 由共价半径估计 (当前元素)
			var a = 4.0 * float(ElementDB.get_element(sym).get("covalent_radius_pm", 100)) / 100.0
			if a < 2.0:
				a = 3.3
			for p in [Vector3(0,0,0), Vector3(a,a,a), Vector3(a,0,0), Vector3(0,a,0), Vector3(0,0,a), Vector3(a,a,0), Vector3(0,a,a), Vector3(a,0,a)]:
				placed.append(_workspace.add_atom(sym, iso, p))
			_current_material_name = "BCC-" + sym
		2:  # FCC
			var a2 = 4.5 * float(ElementDB.get_element(sym).get("covalent_radius_pm", 100)) / 100.0
			if a2 < 2.5:
				a2 = 4.95
			var h = a2 / 2.0
			for p in [Vector3(0,0,0), Vector3(a2,0,0), Vector3(0,a2,0), Vector3(0,0,a2),
					Vector3(a2,a2,0), Vector3(a2,0,a2), Vector3(0,a2,a2), Vector3(a2,a2,a2),
					Vector3(h,h,0), Vector3(h,0,h), Vector3(0,h,h), Vector3(h,h,a2),
					Vector3(h,a2,h), Vector3(a2,h,h)]:
				placed.append(_workspace.add_atom(sym, iso, p))
			_current_material_name = "FCC-" + sym
		3:  # 钙钛矿 SrTiO3 型 ABO3
			var ap = 3.905
			var pairs = [
				["Sr", Vector3(0,0,0)], ["Sr", Vector3(ap,ap,ap)],
				["Ti", Vector3(ap/2, ap/2, ap/2)],
				["O", Vector3(ap/2, ap/2, 0)], ["O", Vector3(ap/2, 0, ap/2)], ["O", Vector3(0, ap/2, ap/2)],
			]
			for entry in pairs:
				placed.append(_workspace.add_atom(entry[0], ElementDB.most_abundant_isotope(entry[0]), entry[1]))
			_current_material_name = "钙钛矿 SrTiO3"
		4:  # CuO2 平面 (2x2)
			var ac = 3.8
			for i in range(2):
				for j in range(2):
					placed.append(_workspace.add_atom("Cu", 63, Vector3(i * ac, j * ac, 0)))
					placed.append(_workspace.add_atom("O", 16, Vector3((i + 0.5) * ac, j * ac, 0)))
					placed.append(_workspace.add_atom("O", 16, Vector3(i * ac, (j + 0.5) * ac, 0)))
			_current_material_name = "CuO2平面"
		5:  # 金刚石
			var ad = 3.567 if sym == "C" else 5.43
			var q = ad / 4.0
			var fcc_pts = [Vector3(0,0,0), Vector3(ad,0,0), Vector3(0,ad,0), Vector3(0,0,ad),
				Vector3(ad,ad,0), Vector3(ad,0,ad), Vector3(0,ad,ad), Vector3(ad,ad,ad),
				Vector3(ad/2,ad/2,0), Vector3(ad/2,0,ad/2), Vector3(0,ad/2,ad/2),
				Vector3(ad/2,ad/2,ad), Vector3(ad/2,ad,ad/2), Vector3(ad,ad/2,ad/2)]
			for p in fcc_pts:
				placed.append(_workspace.add_atom(sym, iso, p))
			for p in fcc_pts:
				placed.append(_workspace.add_atom(sym, iso, p + Vector3(q, q, q)))
			_current_material_name = "金刚石-" + sym
		6:  # 石墨烯 3x3
			var acc = 1.42
			for i in range(3):
				for j in range(3):
					var o = Vector3(i * 3 * acc * 0.866, j * 3 * acc, 0)
					placed.append(_workspace.add_atom(sym, iso, o))
					placed.append(_workspace.add_atom(sym, iso, o + Vector3(acc * 0.866, acc * 0.5, 0)))
					placed.append(_workspace.add_atom(sym, iso, o + Vector3(acc * 0.866 * 3, acc * 0.5, 0)))
					placed.append(_workspace.add_atom(sym, iso, o + Vector3(acc * 0.866 * 2, acc * 1.5, 0)))
					placed.append(_workspace.add_atom(sym, iso, o + Vector3(acc * 0.866 * 3, acc * 2.5, 0)))
					placed.append(_workspace.add_atom(sym, iso, o + Vector3(acc * 0.866 * 4, acc * 2, 0)))
			_current_material_name = "石墨烯-" + sym
	if placed.size() >= 2:
		_auto_connect_lattice(placed)
		_auto_tag_molecules(placed)
	_take_undo_snapshot()
	_update_status("晶格模板: %s → %d 原子 (配位%d)" % [
		_current_material_name, placed.size(),
		_workspace.bonds.size() * 2 / max(placed.size(), 1)])

## 晶格最近邻成键: 以体系最小原子间距 d_min 的 1.25 倍为阈值
## (金属/共价晶格的配位由几何决定: FCC 12配位, BCC 8, 金刚石 4)
func _auto_connect_lattice(atoms: Array, max_bonds_per_atom: int = 12):
	if atoms.size() < 2:
		return 0
	var min_d := INF
	for i in range(atoms.size()):
		for j in range(i + 1, atoms.size()):
			var d = atoms[i].position.distance_to(atoms[j].position)
			if d > 1e-6 and d < min_d:
				min_d = d
	if is_inf(min_d):
		return 0
	var cutoff = min_d * 1.25
	var count_per_atom: Dictionary = {}
	var connected := 0
	for i in range(atoms.size()):
		for j in range(i + 1, atoms.size()):
			if int(count_per_atom.get(i, 0)) >= max_bonds_per_atom:
				break
			if int(count_per_atom.get(j, 0)) >= max_bonds_per_atom:
				continue
			var d = atoms[i].position.distance_to(atoms[j].position)
			if d <= cutoff:
				_workspace.add_bond(atoms[i], atoms[j], 1)
				count_per_atom[i] = int(count_per_atom.get(i, 0)) + 1
				count_per_atom[j] = int(count_per_atom.get(j, 0)) + 1
				connected += 1
	return connected

# === 超胞构建 (正交近似: 以结构包围盒为晶胞) ===

var _supercell_window: Window

func _show_supercell_dialog():
	if _workspace.atoms.is_empty():
		_update_status("超胞需要先有原子结构")
		return
	if _supercell_window and is_instance_valid(_supercell_window):
		_supercell_window.queue_free()
	_supercell_window = Window.new()
	_supercell_window.title = "超胞构建 (正交近似)"
	_supercell_window.size = Vector2i(320, 200)
	var vb = VBoxContainer.new()
	vb.offset_left = 12
	vb.offset_top = 12
	vb.offset_right = -12
	vb.offset_bottom = -12
	_supercell_window.add_child(vb)
	var lbl = Label.new()
	lbl.text = "以结构包围盒为正交晶胞复制。原原子数: %d" % _workspace.atoms.size()
	vb.add_child(lbl)
	var row = HBoxContainer.new()
	row.add_theme_constant_override("separation", 8)
	vb.add_child(row)
	var spins: Array = []
	for axis in ["nx", "ny", "nz"]:
		var l = Label.new()
		l.text = axis
		row.add_child(l)
		var s = SpinBox.new()
		s.min_value = 1
		s.max_value = 5
		s.value = 2
		row.add_child(s)
		spins.append(s)
	var preview = Label.new()
	vb.add_child(preview)
	var apply_btn = Button.new()
	apply_btn.text = "生成超胞"
	vb.add_child(apply_btn)
	var spin_handler = func():
		preview.text = "目标: %d 原子 (%d×%d×%d)" % [
			_workspace.atoms.size() * int(spins[0].value) * int(spins[1].value) * int(spins[2].value),
			int(spins[0].value), int(spins[1].value), int(spins[2].value)]
	for s in spins:
		s.value_changed.connect(func(_v): spin_handler.call())
	spin_handler.call()
	apply_btn.pressed.connect(func():
		_build_supercell(int(spins[0].value), int(spins[1].value), int(spins[2].value))
		_supercell_window.queue_free())
	$UI.add_child(_supercell_window)
	_supercell_window.popup_centered()

func _build_supercell(nx: int, ny: int, nz: int):
	if _workspace.atoms.is_empty() or nx * ny * nz <= 1:
		return
	var src = _workspace.atoms.duplicate()
	var mn := Vector3(INF, INF, INF)
	var mx := Vector3(-INF, -INF, -INF)
	for atom in src:
		mn = mn.min(atom.position)
		mx = mx.max(atom.position)
	var span = mx - mn
	var cell = Vector3(maxf(span.x, 2.0), maxf(span.y, 2.0), maxf(span.z, 2.0))
	_reset_selection_state()
	_workspace.clear()
	var placed: Array = []
	for ix in range(nx):
		for iy in range(ny):
			for iz in range(nz):
				var offset = Vector3(ix * cell.x, iy * cell.y, iz * cell.z) - mn
				for atom in src:
					placed.append(_workspace.add_atom(atom.element_symbol, atom.isotope_mass,
						atom.position + offset))
	if placed.size() >= 2:
		_auto_connect_lattice(placed)
		_auto_tag_molecules(placed)
	_current_material_name += " 超胞%dx%dx%d" % [nx, ny, nz]
	_take_undo_snapshot()
	_update_status("超胞 %d×%d×%d: %d → %d 原子 (正交近似)" % [nx, ny, nz, src.size(), placed.size()])

func _select_element(symbol: String):
	_current_element = symbol

	for sym in _element_buttons.keys():
		var btn = _element_buttons[sym] as Button
		if sym == symbol:
			btn.modulate = Color(1.0, 1.0, 1.0)
		elif not btn.disabled:
			btn.modulate = Color(0.55, 0.6, 0.72)

	var isotopes = ElementDB.get_stable_isotopes(symbol)
	if not isotopes.is_empty():
		_current_isotope = int(isotopes[0].mass_number)
	else:
		_current_isotope = ElementDB.most_abundant_isotope(symbol)

	_refresh_isotopes()
	# 切换元素后立即更新详情 (同位素信息跟随, 而非等用户点同位素按钮)
	var iso_list = ElementDB.get_isotopes(_current_element)
	var cur: Dictionary = {}
	for iso in iso_list:
		if int(iso.mass_number) == _current_isotope:
			cur = iso
			break
	if cur.is_empty() and not iso_list.is_empty():
		cur = iso_list[0]
		_current_isotope = int(cur.mass_number)
	if not cur.is_empty():
		_update_isotope_details(cur)
	_update_element_sc_info()
	_update_status("已选: %s (A=%d) | 右键菜单放置" % [_current_element, _current_isotope])

func _refresh_isotopes():
	for child in _isotope_container.get_children():
		child.queue_free()

	var isotopes = ElementDB.get_isotopes(_current_element)
	isotopes.sort_custom(func(a, b): return int(a.mass_number) < int(b.mass_number))

	for iso in isotopes:
		var btn = Button.new()
		btn.text = str(iso.mass_number)
		btn.custom_minimum_size = Vector2(40, 32)
		btn.add_theme_font_size_override("font_size", 11)
		if bool(iso.get("is_stable", false)):
			btn.modulate = Color(0.7, 1.0, 0.7)
		else:
			btn.modulate = Color(1.0, 0.7, 0.7)
		var captured_iso = iso
		btn.pressed.connect(func(): _select_isotope(captured_iso))
		_isotope_container.add_child(btn)

func _select_isotope(iso: Dictionary):
	_current_isotope = int(iso.mass_number)
	_update_isotope_details(iso)

## 同位素详情标签 (中子数/缺陷/丰度) — 选元素与选同位素共用
func _update_isotope_details(iso: Dictionary):
	var n = int(iso.get("neutrons", 0))
	var defect = CQMCartanBuilder.neutron_defect(n, _current_element)

	_detail_labels.info.text = "选中: %d%s" % [_current_isotope, _current_element]
	_detail_labels.neutrons.text = "中子数: %d" % n
	_detail_labels.defect.text = "中子缺陷 ε: %.6f" % defect
	_detail_labels.abundance.text = "丰度: %.3f%%" % (float(iso.get("abundance", 0)) * 100)
	_update_element_sc_info()

## 元素超导物性卡片 (文档 02 §5.3): θD/λ/Tc/高压记录/来源
func _update_element_sc_info():
	if not _detail_labels.has("sc"):
		return
	var sym = _current_element
	if not SCData.has_entry(sym):
		_detail_labels.sc.text = "%s: 无超导物性数据" % sym
		return
	var theta_d = SCData.get_debye_temperature(sym)
	var lam = SCData.get_lambda_epc(sym)
	var tc = SCData.get_experimental_tc(sym)
	var text = "%s 超导物性:" % sym
	if not is_nan(theta_d):
		var unc = SCData.get_debye_uncertainty(sym)
		text += "  θD = %.0f K" % theta_d
		if unc > 0:
			text += " ±%.0f" % unc
	if not is_nan(lam):
		var lam_unc = SCData.get_lambda_uncertainty(sym)
		text += "  λ = %.2f" % lam
		if lam_unc > 0:
			text += " ±%.2f" % lam_unc
	if SCData.is_ambient_superconductor(sym) and tc > 0:
		text += "\n常压超导: Tc = %.2f K" % tc
	var hp = SCData.get_high_pressure_records(sym)
	if not hp.is_empty():
		var best = hp[0]
		for rec in hp:
			if float(rec.get("tc_K", 0.0)) > float(best.get("tc_K", 0.0)):
				best = rec
		text += "\n高压最高: Tc = %.0f K @%.0f GPa" % [
			float(best.get("tc_K", 0.0)), float(best.get("pressure_GPa", 0.0))]
	if SCData.is_ambient_superconductor(sym):
		_detail_labels.sc.add_theme_color_override("font_color", Color(0.4, 0.95, 0.55))
	else:
		_detail_labels.sc.add_theme_color_override("font_color", Color(0.75, 0.8, 0.9))
	_detail_labels.sc.text = text

func _on_molecule_changed():
	_calc_pending = true
	_calc_timer = 0.0
	_take_undo_snapshot()
	_update_annotations()

func _unhandled_input(event):
	# 输入串扰防护: 鼠标悬停在 GUI 控件(左右面板/滚动区/弹窗)上时, 3D 视口不响应
	if event is InputEventMouse:
		var hover = get_viewport().gui_get_hovered_control()
		var dragging_vp = _is_orbiting or _is_panning or _brush_painting or _arrow_drag_mode > 0 \
			or _grab_mode or _rotate_mode or _scale_mode or _drag_axis > 0 or _box_selecting
		if hover != null and hover != _top_svc and hover != _bottom_svc and not dragging_vp:
			return
	if event is InputEventKey and event.pressed:
		# 焦点在文本输入框时不触发快捷键
		var focus = get_viewport().gui_get_focus_owner()
		if focus is LineEdit or focus is TextEdit or focus is SpinBox:
			return
	if event is InputEventMouseButton:
		var mouse_in_vp = _is_in_top_viewport(event.position) or _is_in_bottom_viewport(event.position)
		match event.button_index:
			MOUSE_BUTTON_LEFT:
				if event.pressed:
					_left_down_pos = event.position
					_left_dragged = false
					var arrow_hit = _check_arrow_hit(event.position)
					if arrow_hit > 0:
						_arrow_drag_mode = arrow_hit
						var dir_key = "pressure_dir" if arrow_hit == 1 else "mag_field_dir"
						_arrow_drag_init_dir = _selected_group_params.get(dir_key, Vector3.UP)
						_left_dragged = true
					elif not mouse_in_vp:
						pass
					elif event.alt_pressed and _is_in_top_viewport(event.position):
						# Alt+左键拖动 = 轨道旋转 (无中键鼠标/触控板)
						_active_vp = 1
						_is_orbiting = true
						_left_dragged = true
					elif event.double_click and not _brush_mode \
							and _is_in_top_viewport(event.position) \
							and _find_atom_at(event.position) == null:
						# 双击空白 = 快速放置当前元素 (省去右键菜单两步)
						_try_place_atom(event.position)
						_left_dragged = true
					elif _brush_mode:
						_start_brush_paint(event.position)
						_left_dragged = true
					elif Input.is_key_pressed(KEY_L) and (_workspace.selected_atom or _selected_atoms.size() > 1):
						_try_l_connect(event.position)
						_left_dragged = true
					elif Input.is_key_pressed(KEY_S) and _is_molecule_selected():
						_try_secondary_select(event.position, event.ctrl_pressed)
						_left_dragged = true
					elif event.ctrl_pressed:
						_try_ctrl_select(event.position)
						_left_dragged = true
					elif _grab_mode:
						_exit_grab_mode(true)
					elif _rotate_mode:
						_exit_rotate_mode(true)
					elif _scale_mode:
						_exit_scale_mode(true)
					elif _gizmo.visible and _try_gizmo_click(event.position):
						pass
				else:
					if _is_orbiting and _active_vp == 1:
						_is_orbiting = false
						_active_vp = 0
					elif _arrow_drag_mode > 0:
						_arrow_drag_mode = 0
					elif _brush_painting:
						_stop_brush_paint()
					elif _drag_axis > 0:
						_drag_axis = 0
						_update_annotations()
					elif _box_selecting:
						_finish_box_select()
					elif not _left_dragged and not _grab_mode and not _rotate_mode and not _scale_mode:
						_try_select_atom(event.position)
			MOUSE_BUTTON_RIGHT:
				if event.pressed:
					_right_down_pos = event.position
					_right_dragged = false
					if _is_in_top_viewport(event.position):
						_active_vp = 1
					elif _is_in_bottom_viewport(event.position):
						_active_vp = 2
					else:
						_active_vp = 0
					if _grab_mode:
						_exit_grab_mode(false)
					elif _rotate_mode:
						_exit_rotate_mode(false)
					elif _scale_mode:
						_exit_scale_mode(false)
				else:
					if not _right_dragged and not _grab_mode and not _rotate_mode and not _scale_mode:
						if mouse_in_vp:
							_show_context_menu(event.position)
					_active_vp = 0
			MOUSE_BUTTON_MIDDLE:
				if event.pressed:
					if _is_in_top_viewport(event.position):
						_active_vp = 1
					elif _is_in_bottom_viewport(event.position):
						_active_vp = 2
					else:
						_active_vp = 0
					if _active_vp > 0:
						if event.shift_pressed:
							_is_panning = true
						else:
							_is_orbiting = true
				else:
					_is_orbiting = false
					_is_panning = false
					_active_vp = 0
			MOUSE_BUTTON_WHEEL_UP:
				var arrow_hit = _check_arrow_hit(event.position)
				if arrow_hit > 0:
					_adjust_arrow_magnitude(arrow_hit, 1)
				elif _is_in_bottom_viewport(event.position):
					_bot_target_dist = max(3.0, _bot_target_dist - 1.0)
				elif _is_in_top_viewport(event.position):
					_top_target_dist = max(3.0, _top_target_dist - 1.0)
			MOUSE_BUTTON_WHEEL_DOWN:
				var arrow_hit2 = _check_arrow_hit(event.position)
				if arrow_hit2 > 0:
					_adjust_arrow_magnitude(arrow_hit2, -1)
				elif _is_in_bottom_viewport(event.position):
					_bot_target_dist = min(80.0, _bot_target_dist + 1.0)
				elif _is_in_top_viewport(event.position):
					_top_target_dist = min(80.0, _top_target_dist + 1.0)
	elif event is InputEventMouseMotion:
		if _arrow_drag_mode > 0:
			_update_arrow_drag(event.position)
		elif _brush_painting:
			_update_brush_paint(event.position)
		elif _grab_mode:
			_update_grab(event.position)
		elif _rotate_mode:
			_update_rotate(event.position)
		elif _scale_mode:
			_update_scale(event.position)
		elif _drag_axis > 0:
			_update_gizmo_drag(event.position)
		elif _is_orbiting:
			if _active_vp == 1:
				_top_yaw -= event.relative.x * 0.005
				_top_pitch = clamp(_top_pitch - event.relative.y * 0.005, -1.4, 1.4)
			elif _active_vp == 2:
				_bot_yaw -= event.relative.x * 0.005
				_bot_pitch = clamp(_bot_pitch - event.relative.y * 0.005, -1.4, 1.4)
		elif _is_panning:
			if _active_vp == 1:
				var r = _camera.global_transform.basis.x
				var u = _camera.global_transform.basis.y
				_top_pan -= r * event.relative.x * 0.01 * _top_cam_dist
				_top_pan += u * event.relative.y * 0.01 * _top_cam_dist
			elif _active_vp == 2:
				var r = _brush_camera.global_transform.basis.x
				var u = _brush_camera.global_transform.basis.y
				_bot_pan -= r * event.relative.x * 0.01 * _bot_cam_dist
				_bot_pan += u * event.relative.y * 0.01 * _bot_cam_dist
		elif Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT) and event.relative.length() > 1:
			_right_dragged = true
			if _active_vp == 1:
				var r = _camera.global_transform.basis.x
				var u = _camera.global_transform.basis.y
				_top_pan -= r * event.relative.x * 0.01 * _top_cam_dist
				_top_pan += u * event.relative.y * 0.01 * _top_cam_dist
			elif _active_vp == 2:
				var r = _brush_camera.global_transform.basis.x
				var u = _brush_camera.global_transform.basis.y
				_bot_pan -= r * event.relative.x * 0.01 * _bot_cam_dist
				_bot_pan += u * event.relative.y * 0.01 * _bot_cam_dist
		elif Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and not _box_selecting and event.relative.length() > 3:
			_left_dragged = true
			if _is_in_top_viewport(event.position) or _is_in_bottom_viewport(event.position):
				if not _workspace.selected_atom or not _gizmo.visible:
					_start_box_select(_left_down_pos)
				elif not _try_gizmo_click(event.position):
					_start_box_select(_left_down_pos)
				if _box_selecting:
					# 启动后立即用当前位置更新矩形 (单次大位移/输入合并时否则矩形为0)
					_update_box_select(event.position)
		elif _box_selecting:
			_left_dragged = true
			_update_box_select(event.position)

	if event is InputEventKey and event.pressed:
		var in_transform = _grab_mode or _rotate_mode or _scale_mode
		if event.ctrl_pressed:
			match event.keycode:
				KEY_S:
					_save_project_dialog()
					get_viewport().set_input_as_handled()
					return
				KEY_O:
					_load_project_dialog()
					get_viewport().set_input_as_handled()
					return
				KEY_Z:
					_do_undo()
					get_viewport().set_input_as_handled()
					return
				KEY_Y:
					_do_redo()
					get_viewport().set_input_as_handled()
					return
		if event.keycode == KEY_G and _workspace.selected_atom and not in_transform:
			_enter_grab_mode()
		elif event.keycode == KEY_R and _workspace.selected_atom and not in_transform:
			_enter_rotate_mode()
		elif event.keycode == KEY_S and _workspace.selected_atom and not in_transform:
			_enter_scale_mode()
		elif event.keycode == KEY_X and in_transform:
			_set_transform_axis(1)
		elif event.keycode == KEY_Y and in_transform:
			_set_transform_axis(2)
		elif event.keycode == KEY_Z and in_transform:
			_set_transform_axis(3)
		elif event.keycode == KEY_ESCAPE:
			if _brush_mode:
				_toggle_brush_mode()
			elif _grab_mode: _exit_grab_mode(false)
			elif _rotate_mode: _exit_rotate_mode(false)
			elif _scale_mode: _exit_scale_mode(false)
			elif _box_selecting:
				_finish_box_select()
		elif event.keycode == KEY_P:
			_toggle_brush_mode()
		elif event.keycode == KEY_A:
			_select_all()
		elif event.keycode == KEY_B and not in_transform:
			_box_selecting = true
			_box_start = get_viewport().get_mouse_position()
			_update_box_select(_box_start)
		elif event.keycode == KEY_M and not in_transform:
			_toggle_measure_mode()
			get_viewport().set_input_as_handled()
		elif event.is_action_pressed("delete"):
			if _workspace.selected_atom:
				_workspace.remove_atom(_workspace.selected_atom)
		elif event.is_action_pressed("calculate"):
			_execute_calculation()

func _set_transform_axis(axis: int):
	if _grab_mode:
		_grab_axis = axis if _grab_axis != axis else 0
	elif _rotate_mode:
		_rotate_axis = axis if _rotate_axis != axis else 0
	elif _scale_mode:
		_scale_axis = axis if _scale_axis != axis else 0

func _deselect():
	_clear_secondary()
	for atom in _selected_atoms:
		if is_instance_valid(atom):
			atom.set_selected(false)
	_selected_atoms.clear()
	_selected_strokes.clear()
	if _workspace.selected_atom:
		_workspace.selected_atom.set_selected(false)
		_workspace.selected_atom = null
	_gizmo.visible = false
	_update_status("已取消选中")

func _reset_selection_state():
	_selected_atoms.clear()
	_secondary_selected_atoms.clear()
	_selected_strokes.clear()
	_atom_to_molecule.clear()
	_molecule_groups.clear()
	_workspace.selected_atom = null
	_l_connect_target = null
	if _gizmo:
		_gizmo.visible = false
	_drag_axis = 0
	_load_params_from_selected()
	_update_physics_panel()

func _find_atom_at(screen_pos: Vector2) -> Atom3D:
	if not _is_in_top_viewport(screen_pos):
		return null
	var local = _to_top_vp_local(screen_pos)
	var from = _camera.project_ray_origin(local)
	var dir = _camera.project_ray_normal(local)
	var best_atom = null
	var best_t = 1e9
	for atom in _workspace.atoms:
		var oc = atom.global_position - from
		var tca = oc.dot(dir)
		if tca < 0:
			continue
		var d2 = oc.dot(oc) - tca * tca
		var r = atom.atom_radius * 1.5
		if d2 > r * r:
			continue
		var thc = sqrt(r * r - d2)
		var t = tca - thc
		if t < best_t:
			best_t = t
			best_atom = atom
	return best_atom

func _try_select_atom(screen_pos: Vector2):
	if _is_in_top_viewport(screen_pos):
		var best_atom = _find_atom_at(screen_pos)
		if best_atom:
			_clear_secondary()
			for atom in _selected_atoms:
				atom.set_selected(false)
			_selected_atoms.clear()
			_selected_strokes.clear()
			if _atom_to_molecule.has(best_atom):
				var gid = _atom_to_molecule[best_atom]
				_select_molecule_group(gid)
			else:
				if _workspace.selected_atom and _workspace.selected_atom != best_atom:
					_workspace.selected_atom.set_selected(false)
				_workspace.selected_atom = best_atom
				best_atom.set_selected(true)
				_selected_atoms.append(best_atom)
				Events.emit_signal("atom_selected", best_atom)
		else:
			_deselect()
	elif _is_in_bottom_viewport(screen_pos):
		var stroke_idx = _find_stroke_at_screen_pos(screen_pos)
		if stroke_idx >= 0:
			_select_stroke(stroke_idx, false)
		else:
			_deselect()
	else:
		_deselect()

func _try_place_atom(screen_pos: Vector2):
	if not _is_in_top_viewport(screen_pos):
		return
	var local = _to_top_vp_local(screen_pos)
	var from = _camera.project_ray_origin(local)
	var dir = _camera.project_ray_normal(local)
	var t = -from.y / dir.y if abs(dir.y) > 0.01 else 0.0
	if t > 0:
		var pos = from + dir * t
		pos = pos.snapped(Vector3(0.25, 0.25, 0.25))
		_workspace.add_atom(_current_element, _current_isotope, pos)
		_update_status("放置: %s%d @ (%.1f,%.1f,%.1f)" % [_current_element, _current_isotope, pos.x, pos.y, pos.z])


func _update_camera():
	if _camera:
		var offset = Vector3(
			_top_cam_dist * cos(_top_pitch) * sin(_top_yaw),
			_top_cam_dist * sin(_top_pitch),
			_top_cam_dist * cos(_top_pitch) * cos(_top_yaw)
		)
		_camera.global_position = offset + _top_pan
		_camera.look_at(_top_pan, Vector3.UP)
	if _brush_camera:
		var offset = Vector3(
			_bot_cam_dist * cos(_bot_pitch) * sin(_bot_yaw),
			_bot_cam_dist * sin(_bot_pitch),
			_bot_cam_dist * cos(_bot_pitch) * cos(_bot_yaw)
		)
		_brush_camera.global_position = offset + _bot_pan
		_brush_camera.look_at(_bot_pan, Vector3.UP)

func _execute_calculation():
	var stroke_data = _get_selected_stroke_data()
	var stroke_pts: Array = stroke_data["points"]
	var stroke_syms: Array = stroke_data["symbols"]
	_compute_trajectory_geometry()

	if stroke_pts.is_empty():
		if _workspace.atoms.is_empty():
			_result_labels.verdict.text = "需画笔轨迹或原子"
			_result_labels.verdict.add_theme_color_override("font_color", Color(0.6, 0.6, 0.65))
			_result_labels.tc.text = "—"
			_result_labels.confidence.text = "—"
			_result_labels.gap.text = "—"
			_result_labels.coupling.text = "—"
			_result_labels.causal_t.text = "—"
			_result_labels.order_params.text = "—"
			_result_labels.atoms_bonds.text = "—"
			_result_labels.eigenvals.text = "请先用画笔绘制轨迹或在上方放置原子"
			_update_status("无画笔轨迹和原子，无法计算")
			return
		var ws_atom_data: Array = []
		for atom in _workspace.atoms:
			if is_instance_valid(atom):
				ws_atom_data.append({
					"symbol": atom.element_symbol,
					"isotope": atom.isotope_mass,
					"position": atom.global_position
				})
		var ws_bond_data: Array = []
		for bond in _workspace.bonds:
			if is_instance_valid(bond) and is_instance_valid(bond.atom_a) and is_instance_valid(bond.atom_b):
				var a_idx = _workspace.atoms.find(bond.atom_a)
				var b_idx = _workspace.atoms.find(bond.atom_b)
				if a_idx >= 0 and b_idx >= 0:
					ws_bond_data.append({"a": a_idx, "b": b_idx, "order": bond.bond_order})
		var ws_params = _selected_group_params.duplicate(true) if not _selected_strokes.is_empty() else _default_physical_params()
		var ws_results = CQMCalculator.evaluate_molecule(ws_atom_data, ws_bond_data, ws_params)
		Events.emit_signal("calculation_complete", ws_results)
		return

	var bond_pairs = _gen_bonds_from_points(stroke_pts, _compute_bond_dist())

	var density = _check_superconductor_density(stroke_pts, bond_pairs)
	if not density.can_compute:
		_result_labels.verdict.text = "密度不足"
		_result_labels.verdict.add_theme_color_override("font_color", Color(0.9, 0.7, 0.2))
		_result_labels.tc.text = "—"
		_result_labels.confidence.text = "—"
		_result_labels.gap.text = "—"
		_result_labels.coupling.text = "—"
		_result_labels.causal_t.text = "—"
		_result_labels.order_params.text = "—"
		_result_labels.atoms_bonds.text = "点:%d 键:%d" % [stroke_pts.size(), bond_pairs.size()]
		var reason_text = "超导密度条件未满足:\n"
		for r in density.reasons:
			reason_text += "  ✗ %s\n" % r
		reason_text += "\n指标:\n"
		reason_text += "  点数: %d (需≥4)\n" % density.metrics.atom_count
		reason_text += "  键数: %d\n" % density.metrics.bond_count
		reason_text += "  平均配位: %.2f (需≥2)\n" % density.metrics.avg_coord
		reason_text += "  连通分量: %d (需=1)\n" % density.metrics.components
		reason_text += "  四面体数: %d (需≥1)\n" % density.metrics.tetrahedra
		_result_labels.eigenvals.text = reason_text
		_update_status("密度不足: %s" % str(density.reasons))
		return

	Events.emit_signal("calculation_started")
	var atom_data: Array = []
	for i in range(stroke_pts.size()):
		var sym = str(stroke_syms[i]) if i < stroke_syms.size() else "H"
		atom_data.append({
			"symbol": sym,
			"isotope": ElementDB.most_abundant_isotope(sym),
			"position": stroke_pts[i]
		})

	var bond_data: Array = []
	for bp in bond_pairs:
		bond_data.append({
			"a": bp[0],
			"b": bp[1],
			"order": 1
		})

	var calc_params = _selected_group_params.duplicate(true) if not _selected_strokes.is_empty() else _default_physical_params()
	var results = CQMCalculator.evaluate_molecule(atom_data, bond_data, calc_params)
	Events.emit_signal("calculation_complete", results)

func _check_superconductor_density(atoms: Array, bond_pairs: Array) -> Dictionary:
	var n = atoms.size()
	var n_bonds = bond_pairs.size()
	var avg_coord = 2.0 * n_bonds / n if n > 0 else 0.0
	var reasons: Array = []

	var adj: Dictionary = {}
	for i in range(n):
		adj[i] = []
	for pair in bond_pairs:
		adj[pair[0]].append(pair[1])
		adj[pair[1]].append(pair[0])

	var visited: Dictionary = {}
	var components = 0
	for start in range(n):
		if visited.has(start):
			continue
		components += 1
		var queue: Array = [start]
		visited[start] = true
		while not queue.is_empty():
			var node = queue.pop_front()
			for neighbor in adj[node]:
				if not visited.has(neighbor):
					visited[neighbor] = true
					queue.append(neighbor)

	var tetrahedra = 0
	if n >= 4:
		for a in range(n):
			for b in adj[a]:
				if b <= a:
					continue
				var common_ab: Dictionary = {}
				for x in adj[a]:
					if x != b:
						common_ab[x] = true
				for c in adj[b]:
					if c <= b or not common_ab.has(c):
						continue
					for d in adj[b]:
						if d <= c or not common_ab.has(d):
							continue
						if not adj[c].has(d):
							continue
						tetrahedra += 1


	var can_compute = true
	if n < 4:
		reasons.append("原子数<4，无法构成四面体")
		can_compute = false
	if components > 1:
		reasons.append("网络不连通(%d个分量)" % components)
		can_compute = false
	if avg_coord < 2.0:
		reasons.append("平均配位%.2f<2，网络过稀疏" % avg_coord)
		can_compute = false
	if tetrahedra == 0:
		reasons.append("无四面体(4-clique)，3D Regge平凡")
		can_compute = false

	return {
		"can_compute": can_compute,
		"reasons": reasons,
		"metrics": {
			"atom_count": n,
			"bond_count": n_bonds,
			"avg_coord": avg_coord,
			"components": components,
			"tetrahedra": tetrahedra,
		}
	}

func _compute_trajectory_geometry():
	if _traj_labels.is_empty():
		return
	if _get_total_stroke_points() < 2:
		_traj_labels.topology.text = "—"
		_traj_labels.arc_len.text = "—"
		_traj_labels.end_dist.text = "—"
		_traj_labels.compact.text = "—"
		_traj_labels.avg_curv.text = "—"
		_traj_labels.max_curv.text = "—"
		_traj_labels.avg_tors.text = "—"
		_traj_labels.bbox.text = "—"
		_traj_labels.branches.text = "—"
		_traj_labels.tortuosity.text = "—"
		_traj_labels.detail.text = ""
		return

	var pts = _get_all_stroke_points()
	var n = pts.size()
	if n < 2:
		return

	var arc_len = 0.0
	for i in range(1, n):
		arc_len += pts[i].distance_to(pts[i - 1])

	var end_dist = pts[0].distance_to(pts[n - 1])

	var mean_spacing = arc_len / (n - 1) if n > 1 else 0.0
	var is_closed = end_dist < mean_spacing * 0.5 and n >= 4

	var compactness = arc_len / end_dist if end_dist > 1e-9 else 999.0

	var avg_curv = 0.0
	var max_curv = 0.0
	var curv_count = 0
	for i in range(1, n - 1):
		var v1 = pts[i] - pts[i - 1]
		var v2 = pts[i + 1] - pts[i]
		var l1 = v1.length()
		var l2 = v2.length()
		var l3 = (v1 + v2).length()
		if l1 < 1e-9 or l2 < 1e-9 or l3 < 1e-9:
			continue
		var cross = v1.cross(v2)
		var kappa = 2.0 * cross.length() / (l1 * l2 * l3)
		avg_curv += kappa
		if kappa > max_curv:
			max_curv = kappa
		curv_count += 1
	avg_curv = avg_curv / curv_count if curv_count > 0 else 0.0

	var avg_tors = 0.0
	var tors_count = 0
	for i in range(1, n - 2):
		var v1 = pts[i] - pts[i - 1]
		var v2 = pts[i + 1] - pts[i]
		var v3 = pts[i + 2] - pts[i + 1]
		var cross12 = v1.cross(v2)
		var denom = cross12.length_squared()
		if denom < 1e-12:
			continue
		var tau = cross12.dot(v3) / denom
		avg_tors += tau
		tors_count += 1
	avg_tors = avg_tors / tors_count if tors_count > 0 else 0.0

	var bb_min = pts[0]
	var bb_max = pts[0]
	for p in pts:
		bb_min.x = minf(bb_min.x, p.x)
		bb_min.y = minf(bb_min.y, p.y)
		bb_min.z = minf(bb_min.z, p.z)
		bb_max.x = maxf(bb_max.x, p.x)
		bb_max.y = maxf(bb_max.y, p.y)
		bb_max.z = maxf(bb_max.z, p.z)
	var bb_size = bb_max - bb_min
	var max_diameter = bb_size.length()

	var branch_count = 0
	for i in range(n):
		var deg = 0
		for j in range(n):
			if i != j and pts[i].distance_to(pts[j]) < _compute_bond_dist():
				deg += 1
		if deg > 2:
			branch_count += 1

	var tortuosity = arc_len / max_diameter if max_diameter > 1e-9 else 999.0

	var topo_text = "开放"
	if is_closed:
		topo_text = "闭合"
	if branch_count > 0:
		topo_text += "+分支"

	_traj_labels.topology.text = topo_text
	_traj_labels.arc_len.text = "%.4f" % arc_len
	_traj_labels.end_dist.text = "%.4f" % end_dist
	_traj_labels.compact.text = "%.4f" % compactness
	_traj_labels.avg_curv.text = "%.6f" % avg_curv
	_traj_labels.max_curv.text = "%.6f" % max_curv
	_traj_labels.avg_tors.text = "%.6f" % avg_tors
	_traj_labels.bbox.text = "%.2f×%.2f×%.2f" % [bb_size.x, bb_size.y, bb_size.z]
	_traj_labels.branches.text = "%d" % branch_count
	_traj_labels.tortuosity.text = "%.4f" % tortuosity

	var detail = "轨迹分析:"
	detail += "\n  采样点: %d" % n
	detail += "\n  平均间距: %.4f" % mean_spacing
	detail += "\n  弧长/直径: %.4f" % tortuosity
	if is_closed:
		detail += "\n  闭合环: 端点距<%.4f" % (mean_spacing * 0.5)
	detail += "\n  曲率点数: %d" % curv_count
	detail += "\n  挠率点数: %d" % tors_count
	_traj_labels.detail.text = detail

func _on_results(results: Dictionary):
	_last_results = results
	var verdict = results.get("verdict", "—")
	var verdict_text: String
	var verdict_color: Color
	match verdict:
		"superconducting":
			verdict_text = "超导"
			verdict_color = Color(0.3, 0.85, 0.4)
		"borderline":
			verdict_text = "临界"
			verdict_color = Color(0.9, 0.8, 0.2)
		"normal":
			verdict_text = "常规"
			verdict_color = Color(0.85, 0.3, 0.3)
		"brush_material":
			verdict_text = "画笔材料"
			verdict_color = Color(0.3, 0.85, 0.4)
		_:
			verdict_text = "数据不足"
			verdict_color = Color(0.6, 0.6, 0.65)
	_result_labels.verdict.text = verdict_text
	_result_labels.verdict.add_theme_color_override("font_color", verdict_color)

	if verdict == "brush_material":
		var regge = results.get("regge", {})
		_result_labels.tc.text = "S_Regge: %.6f" % regge.get("regge_action", 0.0)
		_result_labels.confidence.text = "S_scaled: %s" % _fmt_sci(regge.get("regge_action_scaled", 0.0))
		_result_labels.gap.text = "四面体: %d" % regge.get("tetrahedra_count", 0)
		_result_labels.coupling.text = "亏格边: %d" % regge.get("edges_with_deficit", 0)
		_result_labels.causal_t.text = "尺度: %s" % regge.get("scale_name", "—")
		_result_labels.order_params.text = "最大亏格: %.6f" % regge.get("max_deficit", 0.0)
		_result_labels.atoms_bonds.text = "原子: %d | 键: %d" % [results.get("atom_count",0), results.get("bond_count",0)]

		var ev_text = "Regge作用量详情:"
		ev_text += "\n  S = %.6f" % regge.get("regge_action", 0.0)
		ev_text += "\n  S×scale = %s" % _fmt_sci(regge.get("regge_action_scaled", 0.0))
		ev_text += "\n  四面体数: %d" % regge.get("tetrahedra_count", 0)
		ev_text += "\n  边数: %d" % regge.get("edge_count", 0)
		ev_text += "\n  总亏格: %.6f" % regge.get("total_deficit", 0.0)
		ev_text += "\n  均二面角: %.6f" % regge.get("mean_dihedral", 0.0)
		_result_labels.eigenvals.text = ev_text

		_update_status("Regge: S=%.6f | 四面体:%d | 原子:%d" % [regge.get("regge_action", 0.0), regge.get("tetrahedra_count", 0), results.get("atom_count", 0)])
		return

	var tc = results.get("tc_estimate", 0.0)
	var confidence = results.get("confidence", 0.0)
	if tc > 0:
		_result_labels.tc.text = PhysicsNotation.format_tc(tc, confidence)
	else:
		_result_labels.tc.text = "不超导"
	_result_labels.confidence.text = "置信度: %.1f%%" % (confidence * 100.0)
	_result_labels.gap.text = PhysicsNotation.format_spectral_gap(results.get("spectral_gap", 0.0))
	var delta_0 = results.get("gap_0", 0.0)
	if delta_0 > 0 and tc > 0:
		_result_labels.gap.text += "\n" + PhysicsNotation.format_gap(delta_0, tc)
	var lambda_cov = results.get("lambda_coverage", 0.0)
	_result_labels.coupling.text = PhysicsNotation.format_coupling_constant(
		results.get("coupling", 0.0), results.get("mu_star", 0.0))
	if lambda_cov > 0:
		_result_labels.coupling.text += "\n文献λ覆盖: %.0f%%" % (lambda_cov * 100.0)
	var ct = results.get("causal_cutoff_temp", 0.0)
	_result_labels.causal_t.text = "T_causal = %s" % PhysicsNotation.format_temperature(ct)

	var ev = results.get("eigenvalues", [])
	var ev_text = "A₄本征值: %s" % PhysicsNotation.format_eigenvalues(ev)
	for i in range(min(ev.size(), 8)):
		ev_text += "\n  λ%d = %.4f" % [i + 1, float(ev[i])]
	if ev.size() > 8:
		ev_text += "\n  ... (共%d个)" % ev.size()
	_result_labels.eigenvals.text = ev_text

	var op = results.get("order_parameters", [])
	_result_labels.order_params.text = "序参量通道: %d" % op.size() if not op.is_empty() else "序参量: 无"
	_result_labels.atoms_bonds.text = "原子: %d | 键: %d" % [results.get("atom_count",0), results.get("bond_count",0)]

	ev_text += "\n\n电声参数 (Allen-Dynes 链):"
	ev_text += "\n  公式: " + PhysicsNotation.FORMULA_ALLEN_DYNES
	ev_text += "\n  θ_D = %s" % PhysicsNotation.format_temperature(results.get("debye_temp", 0.0))
	ev_text += "\n  ω_log = %s (位点对数平均, %s)" % [
		PhysicsNotation.format_temperature(results.get("omega_log_temp", 0.0)),
		results.get("phonon_weights", "德拜模型")]
	ev_text += "\n  √⟨ω²⟩ = %s (0.7746·θ_D)" % PhysicsNotation.format_temperature(results.get("sqrt_omega2_temp", 0.0))
	ev_text += "\n  f₁ = %.4f | f₂ = %.4f (强耦合修正)" % [results.get("ad_f1", 1.0), results.get("ad_f2", 1.0)]
	ev_text += "\n  N(0)V = %s" % PhysicsNotation.format_number(results.get("n0v_product", 0.0))
	ev_text += "\n  来源: %s" % results.get("debye_source", "—")
	ev_text += "\n  μ* = %.4f (库仑赝势, Morel-Anderson)" % results.get("mu_star", 0.0)
	ev_text += "\n  Tc方法: %s (公式适用域: %s)" % [
		results.get("tc_method", "—"),
		"是" if results.get("mcmillan_valid", false) else "否"]
	var sens = results.get("tc_mu_star_sensitivity", {})
	if not sens.is_empty():
		ev_text += "\n  μ*敏感性: Tc(0.10)=%s K | Tc(0.13)=%s K | Tc(0.16)=%s K" % [
			PhysicsNotation.format_number(float(sens.get("0.10", 0.0))),
			PhysicsNotation.format_number(float(sens.get("0.13", 0.0))),
			PhysicsNotation.format_number(float(sens.get("0.16", 0.0)))]
	var iso_alpha = results.get("isotope_alpha", NAN)
	if not is_nan(iso_alpha):
		ev_text += "\n  同位素指数 α ≈ %.3f (BCS: 0.5; Ru类可负)" % iso_alpha

	var cf = results.get("critical_fields", {})
	if not cf.is_empty() and cf.get("hc2", 0.0) > 0:
		ev_text += "\n\n临界场与长度尺度:"
		ev_text += "\n  " + PhysicsNotation.format_hc(cf.get("hc1", 0.0), "Hc1")
		ev_text += "\n  " + PhysicsNotation.format_hc(cf.get("hc2", 0.0), "Hc2")
		ev_text += "\n  " + PhysicsNotation.format_hc(cf.get("hc", 0.0), "Hc")
		ev_text += "\n  " + PhysicsNotation.format_ginzburg_landau(cf.get("kappa", 0.0))
		ev_text += "\n  " + PhysicsNotation.format_coherence_length(cf.get("xi", 0.0))
		ev_text += "\n  " + PhysicsNotation.format_penetration_depth(cf.get("lambda_L", 0.0))
		var stepwise = results.get("cqm_stepwise", {})
		if stepwise.get("has_stepwise", false):
			ev_text += "\n\n分步相变 (A₄多分量):"
			for tr in stepwise.get("transitions", []):
				ev_text += "\n  通道%d: T_c=%s (λ=%.4f)" % [
					int(tr.channel), PhysicsNotation.format_temperature(float(tr.tc_channel)), float(tr.eigenvalue)]
		var actions = results.get("cqm_actions", {})
		if not actions.is_empty():
			ev_text += "\n\nCQM作用量 (§3):"
			var sc = actions.get("S_constraint", {})
			if sc is Dictionary:
				ev_text += "\n  S_constraint = %s (和乐 %s + 压强 %s)" % [
					_fmt_sci(float(sc.get("S_constraint", 0.0))),
					_fmt_sci(float(sc.get("S_holonomy", 0.0))),
					_fmt_sci(float(sc.get("S_pressure", 0.0)))]
			else:
				ev_text += "\n  S_constraint = %s" % _fmt_sci(float(sc))
			var sr = actions.get("S_reproduction", {})
			if sr is Dictionary:
				ev_text += "\n  S_reproduction = %s (动能 %s + 再生产 %s + 耦合 %s)" % [
					_fmt_sci(float(sr.get("S_reproduction", 0.0))),
					_fmt_sci(float(sr.get("S_kinetic", 0.0))),
					_fmt_sci(float(sr.get("S_reproduction_core", 0.0))),
					_fmt_sci(float(sr.get("S_coupling", 0.0)))]
			else:
				ev_text += "\n  S_reproduction = %s" % _fmt_sci(float(sr))
			var se = actions.get("S_electron", {})
			if se is Dictionary:
				ev_text += "\n  S_electron = %s (动能 %s + 辫群 %s + 磁 %s)" % [
					_fmt_sci(float(se.get("S_electron", 0.0))),
					_fmt_sci(float(se.get("S_kin", 0.0))),
					_fmt_sci(float(se.get("S_braid", 0.0))),
					_fmt_sci(float(se.get("S_mag", 0.0)))]
			else:
				ev_text += "\n  S_electron = %s" % _fmt_sci(float(se))
			ev_text += "\n  S_Regge = %s (四面体: %d)" % [
				_fmt_sci(float(actions.get("regge_action", 0.0))), int(actions.get("tetrahedra_count", 0))]
			var g16 = actions.get("G16_ricci", {})
			if g16 is Dictionary and int(g16.get("hinge_count", 0)) > 0:
				ev_text += "\n\nG16 Regge-嘉当 (亏角密度→Ricci标量):"
				ev_text += "\n  R_eff = %s (体积加权)" % _fmt_sci(float(g16.get("ricci_scalar_global", 0.0)))
				ev_text += "\n  R̄_hinge = %s | 闭式 R = %s" % [
					_fmt_sci(float(g16.get("ricci_scalar_mean", 0.0))),
					_fmt_sci(float(g16.get("ricci_scalar_closed_form", 0.0)))]
				ev_text += "\n  交叉验证相对误差 = %.1f%%" % (100.0 * float(g16.get("cross_check_rel_error", 0.0)))
				ev_text += "\n  κ = %.4f Å | λ̄ = %.4f | 单调性: %s" % [
					float(g16.get("kappa", 0.0)), float(g16.get("mean_spectral_weight", 0.0)),
					"成立" if g16.get("monotonicity_holds", false) else "不成立"]
			var g17 = actions.get("G17_newtonian", {})
			if g17 is Dictionary and int(g17.get("tet_count", 0)) > 0:
				ev_text += "\n\nG17 牛顿退化 (有效度规→Poisson方程):"
				ev_text += "\n  泊松残差(Regge) = %.1f%% | (牛顿基准) = %.1f%%" % [
					100.0 * float(g17.get("poisson_residual_regge", 0.0)),
					100.0 * float(g17.get("poisson_residual_newton", 0.0))]
				ev_text += "\n  高斯体积积分: Regge = %s | 牛顿 = %s | 目标 4πGM = %s" % [
					_fmt_sci(float(g17.get("laplacian_sum_regge", 0.0))),
					_fmt_sci(float(g17.get("laplacian_sum_newton", 0.0))),
					_fmt_sci(float(g17.get("gauss_target", 0.0)))]
				ev_text += "\n  |h₀₀|max = %s | 洛伦兹号差: %s" % [
					_fmt_sci(float(g17.get("h00_max", 0.0))),
					"有效" if g17.get("lorentz_signature_valid", false) else "反转"]
		_result_labels.eigenvals.text = ev_text

	var bench: Dictionary = {}
	var syms: Array = []
	for atom in _workspace.atoms:
		if is_instance_valid(atom):
			syms.append(str(atom.element_symbol))
	var single_element = not syms.is_empty()
	for s in syms:
		if s != syms[0]:
			single_element = false
			break
	if single_element:
		var tc_exp_el = SCData.get_experimental_tc(syms[0])
		if not is_nan(tc_exp_el):
			bench = {"formula": syms[0], "tc_K": tc_exp_el, "year": 0,
				"source": "元素常压实测 Tc", "pressure_GPa": 0.0}
	else:
		bench = SCData.find_benchmark(_compute_formula(_workspace.atoms))
	if not bench.is_empty() and tc > 0:
		var tc_exp = float(bench.get("tc_K", 0.0))
		ev_text += "\n\n实验基准对照:"
		if int(bench.get("year", 0)) > 0:
			ev_text += "\n  %s: Tc_exp = %s (%d年, %s)" % [
				bench.get("formula", ""), PhysicsNotation.format_temperature(tc_exp),
				int(bench.get("year", 0)), bench.get("source", "")]
		else:
			ev_text += "\n  %s: Tc_exp = %s (%s)" % [
				bench.get("formula", ""), PhysicsNotation.format_temperature(tc_exp),
				bench.get("source", "")]
		var p_exp = float(bench.get("pressure_GPa", 0.0))
		if p_exp > 0:
			ev_text += "\n  实验条件: %s" % PhysicsNotation.format_pressure(p_exp)
		if tc_exp > 0:
			ev_text += "\n  计算/实验 Tc 比 = %.2f" % (tc / tc_exp)
		_result_labels.eigenvals.text = ev_text

	var tc_str = "%sK (%.1f°C)" % [_fmt_sci(tc), tc - 273.15] if tc > 0 else "不超导"
	_update_status("判定: %s | T_c=%s | 原子:%d" % [verdict, tc_str, results.get("atom_count",0)])

func _load_preset(name: String):
	_reset_selection_state()
	_workspace.clear()
	_current_material_name = "预设: " + str(name)
	match name:
		"LaH10":
			_workspace.add_atom("La", 139, Vector3(0, 0, 0))
			for pos in [Vector3(1.5,0,0),Vector3(-1.5,0,0),Vector3(0,1.5,0),Vector3(0,-1.5,0),Vector3(0,0,1.5),Vector3(0,0,-1.5),Vector3(1,1,1),Vector3(-1,-1,1),Vector3(1,-1,-1),Vector3(-1,1,-1)]:
				_workspace.add_atom("H", 1, pos)
		"MgB2":
			var mg = _workspace.add_atom("Mg", 24, Vector3(0, 0, 0))
			var b1 = _workspace.add_atom("B", 11, Vector3(1.2, 0, 0))
			var b2 = _workspace.add_atom("B", 11, Vector3(-1.2, 0, 0))
			_workspace.add_bond(mg, b1)
			_workspace.add_bond(mg, b2)
		"FeSe":
			var fe = _workspace.add_atom("Fe", 56, Vector3(0, 0, 0))
			var se = _workspace.add_atom("Se", 80, Vector3(1.3, 0, 0))
			_workspace.add_bond(fe, se)
		"H2O":
			var o = _workspace.add_atom("O", 16, Vector3(0, 0, 0))
			var h1 = _workspace.add_atom("H", 1, Vector3(0.96, 0, 0.24))
			var h2 = _workspace.add_atom("H", 1, Vector3(-0.24, 0, 0.93))
			_workspace.add_bond(o, h1)
			_workspace.add_bond(o, h2)
	_update_status("已加载预设: %s" % name)

func _update_status(text: String):
	if _status_label:
		_status_label.text = text

func _setup_gizmo():
	_gizmo = Node3D.new()
	_gizmo.visible = false
	_top_sv.add_child(_gizmo)
	var axes_data = [
		{dir = Vector3(1,0,0), color = Color(0.9, 0.2, 0.2), rot = Vector3(0, 0, -PI/2)},
		{dir = Vector3(0,1,0), color = Color(0.2, 0.9, 0.2), rot = Vector3(0, 0, 0)},
		{dir = Vector3(0,0,1), color = Color(0.2, 0.5, 0.9), rot = Vector3(PI/2, 0, 0)},
	]
	for i in range(3):
		var arrow = _create_arrow(axes_data[i].color, axes_data[i].rot, i + 1)
		_gizmo.add_child(arrow)
		_gizmo_arrows.append(arrow)

func _create_arrow(color: Color, rot: Vector3, axis_idx: int) -> Area3D:
	var area = Area3D.new()
	area.rotation = rot
	area.input_ray_pickable = false
	var shaft = MeshInstance3D.new()
	var cyl = CylinderMesh.new()
	cyl.top_radius = 0.06
	cyl.bottom_radius = 0.06
	cyl.height = 1.5
	shaft.mesh = cyl
	shaft.position.y = 0.75
	var mat = StandardMaterial3D.new()
	mat.albedo_color = color
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.emission_enabled = true
	mat.emission = color * 0.8
	mat.emission_energy_multiplier = 1.5
	shaft.material_override = mat
	area.add_child(shaft)
	var tip = MeshInstance3D.new()
	var cone = CylinderMesh.new()
	cone.top_radius = 0.0
	cone.bottom_radius = 0.14
	cone.height = 0.3
	tip.mesh = cone
	tip.position.y = 1.65
	tip.material_override = mat
	area.add_child(tip)
	var col = CollisionShape3D.new()
	var shape = BoxShape3D.new()
	shape.size = Vector3(0.25, 1.8, 0.25)
	col.shape = shape
	col.position.y = 0.75
	area.add_child(col)
	area.input_event.connect(func(_cam, event, _pos, _normal, _shape):
		_on_gizmo_input(axis_idx, event))
	return area

func _on_gizmo_input(axis_idx: int, event: InputEvent):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			_drag_axis = axis_idx
			_drag_start_screen = event.position
			if _workspace.selected_atom:
				_drag_orig_pos = _workspace.selected_atom.position
		else:
			_drag_axis = 0

func _try_gizmo_click(screen_pos: Vector2) -> bool:
	if not _workspace.selected_atom or not _gizmo.visible:
		return false
	if not _is_in_top_viewport(screen_pos):
		return false
	var local = _to_top_vp_local(screen_pos)
	var center = _workspace.selected_atom.global_position
	var s = _gizmo.scale.x
	var axis_len = 1.5 * s
	var axis_dirs = [Vector3(1,0,0), Vector3(0,1,0), Vector3(0,0,1)]
	for i in range(3):
		var sample_ts = [0.15, 0.35, 0.55, 0.75, 0.9, 1.0]
		for t in sample_ts:
			var world_pt = center + axis_dirs[i] * (axis_len * t)
			var screen_pt = _camera.unproject_position(world_pt)
			var threshold = 28.0 if t >= 0.85 else 20.0
			if local.distance_to(screen_pt) < threshold:
				_drag_axis = i + 1
				_drag_orig_pos = _workspace.selected_atom.position
				_drag_init_hit = _compute_gizmo_init_hit(local, i + 1)
				return true
	return false

func _compute_gizmo_init_hit(local: Vector2, axis: int) -> Vector3:
	var from = _camera.project_ray_origin(local)
	var dir = _camera.project_ray_normal(local)
	var axis_vec = Vector3.ZERO
	match axis:
		1: axis_vec = Vector3(1, 0, 0)
		2: axis_vec = Vector3(0, 1, 0)
		3: axis_vec = Vector3(0, 0, 1)
	var orig = _drag_orig_pos
	var plane_normal = dir - axis_vec * (dir.dot(axis_vec))
	if plane_normal.length() < 0.001:
		return orig
	plane_normal = plane_normal.normalized()
	var denom = plane_normal.dot(dir)
	if abs(denom) < 0.001:
		return orig
	var t = plane_normal.dot(orig - from) / denom
	return from + dir * t

func _update_gizmo_drag(screen_pos: Vector2):
	if not _workspace.selected_atom:
		_drag_axis = 0
		return
	var local = _to_top_vp_local(screen_pos)
	var from = _camera.project_ray_origin(local)
	var dir = _camera.project_ray_normal(local)
	var axis_vec = Vector3.ZERO
	match _drag_axis:
		1: axis_vec = Vector3(1, 0, 0)
		2: axis_vec = Vector3(0, 1, 0)
		3: axis_vec = Vector3(0, 0, 1)
	var orig = _drag_orig_pos
	var plane_normal = dir - axis_vec * (dir.dot(axis_vec))
	if plane_normal.length() < 0.001:
		return
	plane_normal = plane_normal.normalized()
	var denom = plane_normal.dot(dir)
	if abs(denom) < 0.001:
		return
	var t = plane_normal.dot(orig - from) / denom
	var hit = from + dir * t
	var new_pos = orig
	match _drag_axis:
		1: new_pos.x = orig.x + (hit.x - _drag_init_hit.x)
		2: new_pos.y = orig.y + (hit.y - _drag_init_hit.y)
		3: new_pos.z = orig.z + (hit.z - _drag_init_hit.z)
	new_pos = ChemValidator.constrain_position(_workspace.selected_atom, new_pos, _workspace.bonds)
	_workspace.selected_atom.position = new_pos
	_update_gizmo_pos()
	_update_annotations()  # 标签实时跟随 gizmo 拖动

func _on_atom_selected(atom):
	if not is_instance_valid(atom):
		return
	if _measure_mode:
		if _measure_atoms.has(atom):
			_measure_atoms.erase(atom)
		else:
			_measure_atoms.append(atom)
		atom.set_selected(_measure_atoms.has(atom))
		if _measure_atoms.size() > 4:
			var extra = _measure_atoms.pop_front()
			if is_instance_valid(extra):
				extra.set_selected(false)
		_update_measurement()
		return
	_update_gizmo_pos()
	_gizmo.visible = true
	_update_atom_panel(atom)
	_update_status("已选中: %s | G=移动 L+点击=连接 Del=删除" % atom.get_info_text())

func _update_atom_panel(atom):
	if not is_instance_valid(atom):
		return
	_atom_labels.symbol.text = atom.element_symbol
	_atom_labels.z.text = str(atom.atomic_number)
	_atom_labels.mass.text = str(atom.isotope_mass)
	_atom_labels.neutrons.text = str(atom.neutron_count)
	_atom_labels.defect.text = "%.6f" % atom.neutron_defect

	var ci = atom.cartan_info
	if ci and not ci.is_empty():
		var ev = ci.get("eigenvalues", [])
		if not ev.is_empty():
			var ev_str = ""
			for i in range(ev.size()):
				if i > 0:
					ev_str += ", "
				ev_str += "%.3f" % float(ev[i])
			_atom_labels.cartan.text = ev_str
		else:
			_atom_labels.cartan.text = "—"
	else:
		_atom_labels.cartan.text = "—"

	var bond_count = 0
	var bond_lengths: Array = []
	for bond in _workspace.bonds:
		if bond.atom_a == atom or bond.atom_b == atom:
			bond_count += 1
			bond_lengths.append(bond.bond_length)
	_atom_labels.bond_count.text = str(bond_count)

	if bond_lengths.is_empty():
		_atom_labels.bond_info.text = "—"
	elif bond_lengths.size() == 1:
		_atom_labels.bond_info.text = "%.3f Å" % bond_lengths[0]
	else:
		var avg_l = 0.0
		for l in bond_lengths:
			avg_l += l
		avg_l /= bond_lengths.size()
		_atom_labels.bond_info.text = "均%.3f Å" % avg_l

	if atom.is_brush_material:
		_atom_labels.brush.text = "是"
		_atom_labels.brush.add_theme_color_override("font_color", Color(0.3, 0.85, 0.4))
		_atom_labels.scale.text = "%dx" % atom.brush_scale_level
		_atom_labels.scale.add_theme_color_override("font_color", Color(0.3, 0.85, 0.4))
	else:
		_atom_labels.brush.text = "否"
		_atom_labels.brush.add_theme_color_override("font_color", Color(0.85, 0.88, 0.95))
		_atom_labels.scale.text = "—"
		_atom_labels.scale.add_theme_color_override("font_color", Color(0.6, 0.6, 0.65))

	_atom_labels.config.text = _classify_geometry(atom, bond_count)
	_compute_atom_regge_cartan()

	var syms: Array = []
	for a in _selected_atoms:
		if is_instance_valid(a):
			syms.append(a.element_symbol)
	if syms.size() > 1:
		var idents = _identify_selected_groups()
		_formula_label.text = "化学式: %s" % "、".join(idents)
	else:
		_formula_label.text = "化学式: %s" % atom.element_symbol

func _classify_geometry(atom, bond_count: int) -> String:
	if bond_count == 0:
		return "孤立"
	if bond_count == 1:
		return "双原子"
	if bond_count == 2:
		return "线型"
	if bond_count == 3:
		return "三角平面"
	if bond_count == 4:
		var neighbors: Array = []
		for bond in _workspace.bonds:
			if bond.atom_a == atom:
				neighbors.append(bond.atom_b.global_position - atom.global_position)
			elif bond.atom_b == atom:
				neighbors.append(bond.atom_a.global_position - atom.global_position)
		if neighbors.size() >= 2:
			var angle_sum = 0.0
			var count = 0
			for i in range(neighbors.size()):
				for j in range(i + 1, neighbors.size()):
					var cos_a = neighbors[i].normalized().dot(neighbors[j].normalized())
					angle_sum += acos(clampf(cos_a, -1.0, 1.0))
					count += 1
			if count > 0:
				var avg_angle = rad_to_deg(angle_sum / count)
				if abs(avg_angle - 109.5) < 10:
					return "四面体"
				if abs(avg_angle - 90.0) < 10:
					return "平面四配"
		return "四配位"
	if bond_count == 5:
		return "三角双锥"
	if bond_count == 6:
		return "八面体"
	return "%d配位" % bond_count

func _compute_atom_regge_cartan():
	var sel_atoms: Array = []
	for a in _selected_atoms:
		if is_instance_valid(a):
			sel_atoms.append(a)
	if sel_atoms.is_empty():
		_atom_labels.regge.text = "—"
		_atom_labels.spec_gap.text = "—"
		_atom_labels.mol_dim.text = "—"
		return

	var positions: Array = []
	var atom_to_idx: Dictionary = {}
	for i in range(sel_atoms.size()):
		positions.append(sel_atoms[i].global_position)
		atom_to_idx[sel_atoms[i]] = i

	var bond_pairs: Array = []
	var cartan_bonds: Array = []
	for bond in _workspace.bonds:
		if atom_to_idx.has(bond.atom_a) and atom_to_idx.has(bond.atom_b):
			var a_idx = atom_to_idx[bond.atom_a]
			var b_idx = atom_to_idx[bond.atom_b]
			bond_pairs.append([a_idx, b_idx])
			var data_a = ElementDB.get_element(bond.atom_a.element_symbol)
			var data_b = ElementDB.get_element(bond.atom_b.element_symbol)
			cartan_bonds.append({
				"a": a_idx, "b": b_idx,
				"order": bond.bond_order,
				"length": bond.bond_length,
				"r_a": float(data_a.get("covalent_radius_pm", 50)) / 100.0,
				"r_b": float(data_b.get("covalent_radius_pm", 50)) / 100.0,
			})

	var regge = ReggeCalculator.compute_regge_3d(positions, bond_pairs, 1)
	_atom_labels.regge.text = "%.6f" % regge.get("regge_action", 0.0)
	if abs(regge.get("regge_action", 0.0)) > 1e-6:
		_atom_labels.regge.add_theme_color_override("font_color", Color(0.3, 0.85, 0.4))
	else:
		_atom_labels.regge.add_theme_color_override("font_color", Color(0.6, 0.6, 0.65))

	var cartan_atoms: Array = []
	for a in sel_atoms:
		cartan_atoms.append({
			"atomic_number": a.atomic_number,
			"neutron_defect": a.neutron_defect,
		})

	var mc = MolecularCartan.compute_molecular_cartan(cartan_atoms, cartan_bonds)
	_atom_labels.spec_gap.text = "%.6f" % mc.get("spectral_gap", 0.0)
	_atom_labels.mol_dim.text = "%d×%d" % [mc.get("dimension", 0), mc.get("dimension", 0)]

	var ev = mc.get("eigenvalues", [])
	if not ev.is_empty():
		var ev_str = ""
		for i in range(mini(ev.size(), 8)):
			if i > 0:
				ev_str += ", "
			ev_str += "%.3f" % float(ev[i])
		if ev.size() > 8:
			ev_str += "..."
		_atom_labels.cartan.text = ev_str
	else:
		_atom_labels.cartan.text = "—"

func _on_atom_removed(_atom):
	if _gizmo:
		_gizmo.visible = false
	_drag_axis = 0
	if _atom_to_molecule.has(_atom):
		var gid = _atom_to_molecule[_atom]
		_atom_to_molecule.erase(_atom)
		if gid >= 0 and gid < _molecule_groups.size() and _molecule_groups[gid] != null:
			_molecule_groups[gid]["atoms"].erase(_atom)
			if _molecule_groups[gid]["atoms"].is_empty():
				_molecule_groups[gid] = null
	_selected_atoms.erase(_atom)
	_secondary_selected_atoms.erase(_atom)

func _update_gizmo_pos():
	if _workspace.selected_atom and _gizmo:
		_gizmo.global_position = _workspace.selected_atom.global_position
		var s = _top_cam_dist * 0.04
		_gizmo.scale = Vector3(s, s, s)

func _enter_grab_mode():
	if not _workspace.selected_atom:
		return
	_grab_mode = true
	_grab_axis = 0
	_grab_orig_pos = _workspace.selected_atom.position
	# 整体移动组: 主原子属分子组 → 整组; 否则多选全体; 否则单原子
	var group_atoms: Array = []
	var primary_gid = _atom_to_molecule.get(_workspace.selected_atom, -1)
	if primary_gid >= 0:
		var g = _get_molecule_group(primary_gid)
		if g != null:
			group_atoms = g["atoms"]
	if group_atoms.is_empty():
		group_atoms = _selected_atoms if _selected_atoms.size() > 1 else [_workspace.selected_atom]
	_grab_group = []
	for atom in group_atoms:
		if is_instance_valid(atom):
			_grab_group.append({"atom": atom, "orig": atom.position})
	_grab_start_screen = get_viewport().get_mouse_position()
	var local = _to_top_vp_local(_grab_start_screen)
	var from0 = _camera.project_ray_origin(local)
	var dir0 = _camera.project_ray_normal(local)
	var t0 = -from0.y / dir0.y if abs(dir0.y) > 0.01 else 0.0
	_grab_init_hit = (from0 + dir0 * t0) if t0 > 0 else _grab_orig_pos
	_gizmo.visible = false
	if _grab_group.size() > 1:
		_update_status("整体移动 %d 原子: 鼠标移动 | X/Y/Z=约束轴 | 左键=确认 Esc=取消" % _grab_group.size())
	else:
		_update_status("移动模式: 鼠标移动 | X/Y/Z=约束轴 | 左键=确认 Esc=取消")

func _exit_grab_mode(confirm: bool):
	_grab_mode = false
	_grab_axis = 0
	if not confirm and _grab_group.size() > 0:
		# 取消: 整组恢复原位
		for entry in _grab_group:
			if is_instance_valid(entry["atom"]):
				entry["atom"].position = entry["orig"]
	_grab_group = []
	if _workspace.selected_atom:
		if not confirm:
			_workspace.selected_atom.position = _grab_orig_pos
		_gizmo.visible = true
		_update_gizmo_pos()
		_update_annotations()  # 标签跟随原子新位置
		if confirm:
			_update_status("已移动至 (%.1f, %.1f, %.1f)" % [_workspace.selected_atom.position.x, _workspace.selected_atom.position.y, _workspace.selected_atom.position.z])

func _update_grab(screen_pos: Vector2):
	if not _workspace.selected_atom:
		_exit_grab_mode(false)
		return
	var local = _to_top_vp_local(screen_pos)
	var from = _camera.project_ray_origin(local)
	var dir = _camera.project_ray_normal(local)
	var orig = _grab_orig_pos
	var new_pos = orig
	if _grab_axis == 0:
		var t = -from.y / dir.y if abs(dir.y) > 0.01 else 0.0
		if t > 0:
			var hit = from + dir * t
			new_pos.x = orig.x + (hit.x - _grab_init_hit.x)
			new_pos.z = orig.z + (hit.z - _grab_init_hit.z)
	else:
		var axis_vec = Vector3.ZERO
		match _grab_axis:
			1: axis_vec = Vector3(1, 0, 0)
			2: axis_vec = Vector3(0, 1, 0)
			3: axis_vec = Vector3(0, 0, 1)
		var denom = axis_vec.dot(dir)
		if abs(denom) > 0.001:
			var t = axis_vec.dot(orig - from) / denom
			var hit = from + dir * t

			match _grab_axis:
				1: new_pos.x = orig.x + (hit.x - _grab_init_hit.x)
				2: new_pos.y = orig.y + (hit.y - _grab_init_hit.y)
				3: new_pos.z = orig.z + (hit.z - _grab_init_hit.z)
	new_pos = ChemValidator.constrain_position(_workspace.selected_atom, new_pos, _workspace.bonds)
	# 分子整体移动: 选中组(多原子)时所有原子按相同位移平移
	var delta = new_pos - orig
	_workspace.selected_atom.position = new_pos
	if _grab_group.size() > 1:
		for entry in _grab_group:
			var atom = entry["atom"]
			if atom != _workspace.selected_atom and is_instance_valid(atom):
				atom.position = entry["orig"] + delta
	_update_annotations()  # 标签实时跟随移动

var _trail_sig_cached := ""
var _arrow_sig_cached := ""

func _process(delta):
	_top_cam_dist = lerp(_top_cam_dist, _top_target_dist, 1.0 - exp(-delta * 10.0))
	_bot_cam_dist = lerp(_bot_cam_dist, _bot_target_dist, 1.0 - exp(-delta * 10.0))
	_update_camera()
	# ImmediateMesh 重建按签名缓存: 无结构/选中/参数变化时跳过 (性能)
	var trail_sig := "%d|%d|%s|%d" % [_brush_strokes.size(), _get_total_stroke_points(),
		str(_selected_strokes), 1 if not _current_stroke.is_empty() else 0]
	if trail_sig != _trail_sig_cached:
		_trail_sig_cached = trail_sig
		_update_brush_trail()
	var arrow_sig := "%s|%s|%s|%s|%s" % [str(_selected_strokes),
		str(_selected_group_params.get("pressure_mag", 0.0)),
		str(_selected_group_params.get("mag_field_mag", 0.0)),
		str(_selected_group_params.get("pressure_dir", Vector3.ZERO)),
		str(_selected_group_params.get("temperature", 0.0))]
	if arrow_sig != _arrow_sig_cached:
		_arrow_sig_cached = arrow_sig
		_draw_physics_arrows()
	if _workspace.selected_atom and _gizmo.visible and not _grab_mode and not _rotate_mode and not _scale_mode and _drag_axis == 0:
		_update_gizmo_pos()
	if _calc_pending:
		_calc_timer += delta
		if _calc_timer >= CALC_DEBOUNCE:
			_calc_pending = false
			_execute_calculation()

func _setup_context_menu():
	_context_menu = PopupMenu.new()
	_context_menu.add_item("生成原子", 1)
	_context_menu.add_item("删除选中 (原子/分子/笔划)", 2)
	_context_menu.add_item("替换元素 (笔划)", 10)
	_context_menu.add_separator()
	_context_menu.add_item("设为画笔模板", 7)
	_context_menu.add_item("设为画桶模板", 8)
	_context_menu.add_item("加入自定义分子列表", 9)
	_context_menu.add_separator()
	_context_menu.add_item("全选 (A)", 3)
	_context_menu.add_item("清空所有", 4)
	_context_menu.add_separator()
	var geo_menu = PopupMenu.new()
	geo_menu.name = "GeometryMenu"
	geo_menu.add_item("自动连接", 100)
	geo_menu.add_separator()
	geo_menu.add_item("线型 (Linear)", 101)
	geo_menu.add_item("折线型 (Bent)", 102)
	geo_menu.add_item("三角平面 (Trigonal)", 103)
	geo_menu.add_item("四面体 (Tetrahedral)", 104)
	geo_menu.add_item("八面体 (Octahedral)", 105)
	geo_menu.id_pressed.connect(_on_geometry_menu_id)
	_context_menu.add_child(geo_menu)
	_context_menu.add_submenu_item("结合连接", "GeometryMenu")

	_context_menu.id_pressed.connect(_on_context_menu_id)
	$UI.add_child(_context_menu)
	_mol_connect_menu = PopupMenu.new()
	_mol_connect_menu.add_item("最近原子连接", 200)
	_mol_connect_menu.add_item("中心原子连接", 201)
	_mol_connect_menu.add_item("全部连接", 202)
	_mol_connect_menu.add_separator()
	_mol_connect_menu.add_item("线型排列", 203)
	_mol_connect_menu.add_item("折线型排列", 204)
	_mol_connect_menu.add_item("三角平面排列", 205)
	_mol_connect_menu.add_item("四面体排列", 206)
	_mol_connect_menu.add_item("八面体排列", 207)
	_mol_connect_menu.id_pressed.connect(_on_mol_connect_menu_id)
	$UI.add_child(_mol_connect_menu)
	_secondary_connect_menu = PopupMenu.new()
	_secondary_connect_menu.add_item("全部锚点连接", 300)
	_secondary_connect_menu.add_item("最近锚点连接", 301)
	_secondary_connect_menu.add_item("质心锚点连接", 302)
	_secondary_connect_menu.add_separator()
	_secondary_connect_menu.add_item("线型排列", 303)
	_secondary_connect_menu.add_item("折线型排列", 304)
	_secondary_connect_menu.add_item("三角平面排列", 305)
	_secondary_connect_menu.add_item("四面体排列", 306)
	_secondary_connect_menu.add_item("八面体排列", 307)
	_secondary_connect_menu.id_pressed.connect(_on_secondary_connect_menu_id)
	$UI.add_child(_secondary_connect_menu)

func _setup_box_select():
	_box_rect = ColorRect.new()
	_box_rect.color = Color(0.3, 0.6, 1.0, 0.15)

	_box_rect.visible = false
	_box_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	$UI.add_child(_box_rect)

func _canvas_to_screen(pos: Vector2) -> Vector2:
	# canvas (stretch 坐标系) → 物理窗口坐标
	# 注意: Window.popup() 的 Rect2 直接接受 canvas 坐标 (引擎自动换算), 勿对 popup 用本函数
	var vis = get_viewport().get_visible_rect().size
	var win = Vector2(DisplayServer.window_get_size())
	if vis.x <= 0 or vis.y <= 0:
		return pos
	return pos * (win / vis)

func _show_context_menu(pos: Vector2):
	if not _is_in_top_viewport(pos) and not _is_in_bottom_viewport(pos):
		return
	_menu_mouse_pos = pos
	_context_menu.hide()
	var in_bottom = _is_in_bottom_viewport(pos)
	var has_atom = _workspace.selected_atom != null
	var has_sel = _selected_atoms.size() >= 1
	_context_menu.set_item_disabled(_context_menu.get_item_index(1), in_bottom)
	var can_delete = (not in_bottom and (has_atom or has_sel)) \
		or (in_bottom and not _selected_strokes.is_empty())
	_context_menu.set_item_disabled(_context_menu.get_item_index(2), not can_delete)
	_context_menu.set_item_disabled(_context_menu.get_item_index(10), not (in_bottom and not _selected_strokes.is_empty()))
	_context_menu.set_item_disabled(_context_menu.get_item_index(7), in_bottom or not has_sel)
	_context_menu.set_item_disabled(_context_menu.get_item_index(8), in_bottom or not has_sel)
	_context_menu.set_item_disabled(_context_menu.get_item_index(9), in_bottom or not has_sel)
	_context_menu.set_item_disabled(_context_menu.get_item_index(3), in_bottom)
	var sub_idx = _context_menu.get_item_count() - 1
	_context_menu.set_item_disabled(sub_idx, in_bottom or not has_sel)
	_context_menu.size = Vector2i(200, 0)
	# 弹出位置 clamp 到窗口内 (防止边缘右键时菜单出屏)
	var vis_size = get_viewport().get_visible_rect().size
	var clamped = pos.clamp(Vector2(4, 4), vis_size - Vector2(204, 44))
	_context_menu.popup(Rect2(clamped, Vector2(200, 0)))

func _on_context_menu_id(id: int):
	match id:
		1: _try_place_atom(_menu_mouse_pos)
		2: _delete_selected()
		3: _select_all()
		4:
			_reset_selection_state()
			_workspace.clear()

		7: _set_brush_molecule_template()
		8: _set_fill_molecule_template()
		9: _add_to_custom_molecules()
		10: _replace_stroke_element()

## 删除选中内容: 原子/分子组(整组)/画笔笔划; 无选中时删除点击处原子
func _delete_selected():
	var deleted_atoms := 0
	var deleted_strokes := 0
	# 画笔笔划 (材料部分)
	if not _selected_strokes.is_empty():
		var idxs = (_selected_strokes.duplicate() as Array)
		idxs.sort()
		idxs.reverse()
		for idx in idxs:
			if idx >= 0 and idx < _brush_strokes.size():
				_brush_strokes.remove_at(idx)
				deleted_strokes += 1
		_selected_strokes.clear()
		for bs in _boundary_shapes:
			if int(bs.get("stroke_idx", -1)) >= _brush_strokes.size():
				bs["stroke_idx"] = -1
		_refresh_brush_atom_render()
		_boundary_count_lbl.text = "边界数: %d" % _boundary_shapes.size()
		_brush_count_lbl.text = "画笔点: %d" % _get_total_stroke_points()
	# 原子 (整组: 删除任一组成员原子会连组删除)
	var to_delete: Array = []
	var seen := {}
	for atom in _selected_atoms:
		if not is_instance_valid(atom) or seen.has(atom):
			continue
		if _atom_to_molecule.has(atom):
			var g = _get_molecule_group(_atom_to_molecule[atom])
			if g != null:
				for ga in g["atoms"]:
					if is_instance_valid(ga) and not seen.has(ga):
						seen[ga] = true
						to_delete.append(ga)
			else:
				seen[atom] = true
				to_delete.append(atom)
		else:
			seen[atom] = true
			to_delete.append(atom)
	if to_delete.is_empty() and _workspace.selected_atom and not seen.has(_workspace.selected_atom):
		to_delete.append(_workspace.selected_atom)
	if to_delete.is_empty() and not _workspace.atoms.is_empty():
		var hit = _find_atom_at(_menu_mouse_pos)
		if hit:
			to_delete.append(hit)
	for atom in to_delete:
		_workspace.remove_atom(atom)
		deleted_atoms += 1
	_reset_selection_state()
	_take_undo_snapshot()
	if deleted_atoms > 0 or deleted_strokes > 0:
		_update_status("已删除: %d 原子, %d 笔划" % [deleted_atoms, deleted_strokes])
	else:
		_update_status("无可删除内容")

func _start_box_select(pos: Vector2):
	_box_selecting = true
	_box_start = pos
	_update_box_select(pos)

func _update_box_select(pos: Vector2):
	var x = min(_box_start.x, pos.x)
	var y = min(_box_start.y, pos.y)
	var w = abs(pos.x - _box_start.x)
	var h = abs(pos.y - _box_start.y)
	_box_rect.position = Vector2(x, y)
	_box_rect.size = Vector2(w, h)
	_box_rect.visible = true

func _finish_box_select():
	_box_selecting = false
	_box_rect.visible = false
	var rect = Rect2(_box_rect.position, _box_rect.size)
	if rect.size.length() < 5:
		return
	_selected_atoms.clear()
	_selected_strokes.clear()
	var added = {}
	for atom in _workspace.atoms:
		var screen_pos = _camera.unproject_position(atom.global_position)
		var global_sp = Vector2(screen_pos.x + _vp_x, screen_pos.y + _vp_y)
		if rect.has_point(global_sp):
			if _atom_to_molecule.has(atom):
				var gid = _atom_to_molecule[atom]
				var group = _get_molecule_group(gid)
				if group == null:
					if not added.has(atom):
						atom.set_selected(true)
						_selected_atoms.append(atom)
						added[atom] = true
				else:
					for ga in group["atoms"]:
						if not added.has(ga):
							ga.set_selected(true)
							_selected_atoms.append(ga)
							added[ga] = true
					added[atom] = true
			elif not added.has(atom):
				# 独立原子 (未标记分子组) 直接选中
				atom.set_selected(true)
				_selected_atoms.append(atom)
				added[atom] = true
	if _selected_atoms.size() > 0:
		_workspace.selected_atom = _selected_atoms[0]
		_update_gizmo_pos()
		_gizmo.visible = true
		var idents = _identify_selected_groups()
		_formula_label.text = "化学式: %s" % "、".join(idents)
		# 框选仅选择, 不自动成键/成分子 (结合连接用右键菜单显式触发)
		var mol_count = 0
		var checked = {}
		for atom in _selected_atoms:
			if _atom_to_molecule.has(atom):
				var gid = _atom_to_molecule[atom]
				if not checked.has(gid):
					checked[gid] = true
					mol_count += 1
		if mol_count > 0:
			_update_status("框选 %d 原子 (含%d个已标记分子) → %s | 右键=结合连接/删除" % [_selected_atoms.size(), mol_count, "、".join(idents)])
		else:
			_update_status("框选 %d 原子 → %s | 右键=结合连接/删除" % [_selected_atoms.size(), "、".join(idents)])
	else:
		_formula_label.text = "化学式: —"
	_box_select_strokes(rect)
	if _selected_strokes.size() > 0:
		_update_status("框选: %d原子 + %d笔划" % [_selected_atoms.size(), _selected_strokes.size()])
	elif _selected_atoms.size() == 0:
		_update_status("框选完成（无选中）")

func _identify_selected_groups() -> Array:
	if _selected_atoms.is_empty():
		return []
	var visited = {}
	var groups = []
	for atom in _selected_atoms:
		if visited.has(atom):
			continue
		var comp = []
		var queue = [atom]
		visited[atom] = true
		while queue.size() > 0:
			var cur = queue.pop_front()
			comp.append(cur)
			for bond in _workspace.bonds:
				var nb = null
				if bond.atom_a == cur and _selected_atoms.has(bond.atom_b):
					nb = bond.atom_b
				elif bond.atom_b == cur and _selected_atoms.has(bond.atom_a):
					nb = bond.atom_a
				if nb != null and not visited.has(nb):
					visited[nb] = true
					queue.append(nb)
		var total_mass = 0
		for a in comp:
			total_mass += a.isotope_mass
		groups.append({"formula": _compute_formula(comp), "mass": total_mass})
	groups.sort_custom(func(a, b): return a["mass"] > b["mass"])
	var result = []
	for g in groups:
		result.append(g["formula"])
	return result

func _compute_formula(atoms: Array) -> String:
	var counts = {}
	for atom in atoms:
		var sym = atom.element_symbol
		counts[sym] = counts.get(sym, 0) + 1
	var result = ""
	if counts.has("C"):
		result += "C"
		if counts["C"] > 1: result += str(counts["C"])
		counts.erase("C")
	if counts.has("H"):
		result += "H"
		if counts["H"] > 1: result += str(counts["H"])
		counts.erase("H")
	var keys = counts.keys()
	keys.sort()
	for sym in keys:
		result += sym
		if counts[sym] > 1: result += str(counts[sym])
	return result

func _auto_connect(atoms: Array):
	for i in range(atoms.size()):
		var a = atoms[i]
		if not is_instance_valid(a):
			continue
		for j in range(i + 1, atoms.size()):
			var b = atoms[j]
			if not is_instance_valid(b):
				continue
			var dist = a.global_position.distance_to(b.global_position)
			var data_a = ElementDB.get_element(a.element_symbol)
			var data_b = ElementDB.get_element(b.element_symbol)
			var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
			var r_b = float(data_b.get("covalent_radius_pm", 50)) / 100.0
			var max_dist = (r_a + r_b) * 1.3
			if dist <= max_dist and dist > 0.1:
				var exists = false
				for bond in _workspace.bonds:
					if not is_instance_valid(bond):
						continue
					if (bond.atom_a == a and bond.atom_b == b) or (bond.atom_a == b and bond.atom_b == a):
						exists = true
						break
				if not exists:
					_workspace.add_bond(a, b)


func _auto_tag_molecules(atoms: Array) -> Array:
	var formulas = []
	var visited = {}
	for atom in atoms:
		if visited.has(atom):
			continue
		var comp = []
		var queue = [atom]
		visited[atom] = true
		while queue.size() > 0:
			var cur = queue.pop_front()
			comp.append(cur)
			for bond in _workspace.bonds:
				var nb = null
				if bond.atom_a == cur and atoms.has(bond.atom_b):
					nb = bond.atom_b
				elif bond.atom_b == cur and atoms.has(bond.atom_a):
					nb = bond.atom_a
				if nb != null and not visited.has(nb):
					visited[nb] = true
					queue.append(nb)
		if comp.size() >= 2:
			for a in comp:
				if _atom_to_molecule.has(a):
					var old_gid = _atom_to_molecule[a]
					_atom_to_molecule.erase(a)
					var old_g = _get_molecule_group(old_gid)
					if old_g != null:
						old_g["atoms"].erase(a)
						if old_g["atoms"].is_empty():
							_molecule_groups[old_gid] = null
			_tag_as_molecule(comp, true)
			formulas.append(_compute_formula(comp))
	return formulas

func _select_all():
	if _workspace.atoms.is_empty():
		return
	var all_selected = true
	for atom in _workspace.atoms:
		if not atom._is_selected:
			all_selected = false
			break
	if all_selected:
		for atom in _workspace.atoms:
			atom.set_selected(false)
		_selected_atoms.clear()
		_clear_secondary()
		_workspace.selected_atom = null
		_gizmo.visible = false
		_update_status("已取消全选")
	else:
		_selected_atoms.clear()
		_clear_secondary()
		for atom in _workspace.atoms:
			atom.set_selected(true)
			_selected_atoms.append(atom)
		_workspace.selected_atom = _workspace.atoms[0]
		_update_gizmo_pos()
		_gizmo.visible = true
		_update_status("已全选 %d 个原子 | 右键=结合连接/标记" % _workspace.atoms.size())

func _enter_rotate_mode():
	if not _workspace.selected_atom:
		return
	_rotate_mode = true
	_rotate_axis = 0
	_rotate_orig_rot = _workspace.selected_atom.rotation
	_rotate_start_angle = 0.0
	_rotate_init = false
	_gizmo.visible = false
	_update_status("旋转模式: 鼠标移动 | X/Y/Z=约束轴 | 左键=确认 Esc=取消")

func _exit_rotate_mode(confirm: bool):
	_rotate_mode = false
	_rotate_axis = 0
	if _workspace.selected_atom:
		if not confirm:
			_workspace.selected_atom.rotation = _rotate_orig_rot
		_gizmo.visible = true
		_update_gizmo_pos()
		_update_annotations()

func _update_rotate(screen_pos: Vector2):
	if not _workspace.selected_atom:
		_exit_rotate_mode(false)
		return
	var center = _camera.unproject_position(_workspace.selected_atom.global_position)
	var local = _to_top_vp_local(screen_pos)
	var angle = atan2(local.y - center.y, local.x - center.x)
	if not _rotate_init:
		_rotate_start_angle = angle
		_rotate_init = true
	var delta_angle = angle - _rotate_start_angle
	match _rotate_axis:
		0: _workspace.selected_atom.rotation.y = _rotate_orig_rot.y + delta_angle
		1: _workspace.selected_atom.rotation.x = _rotate_orig_rot.x + delta_angle
		2: _workspace.selected_atom.rotation.y = _rotate_orig_rot.y + delta_angle
		3: _workspace.selected_atom.rotation.z = _rotate_orig_rot.z + delta_angle

func _enter_scale_mode():
	if not _workspace.selected_atom:
		return
	_scale_mode = true
	_scale_axis = 0
	_scale_orig = _workspace.selected_atom.scale.x
	_scale_start_dist = 0.0
	_scale_init = false
	_gizmo.visible = false
	_update_status("缩放模式: 鼠标移动 | X/Y/Z=约束轴 | 左键=确认 Esc=取消")

func _exit_scale_mode(confirm: bool):
	_scale_mode = false
	_scale_axis = 0
	if _workspace.selected_atom:
		if not confirm:
			var s = _scale_orig
			_workspace.selected_atom.scale = Vector3(s, s, s)
		_gizmo.visible = true
		_update_gizmo_pos()
		_update_annotations()

func _update_scale(screen_pos: Vector2):
	if not _workspace.selected_atom:
		_exit_scale_mode(false)
		return
	var center = _camera.unproject_position(_workspace.selected_atom.global_position)
	var local = _to_top_vp_local(screen_pos)
	var dist = local.distance_to(center)
	if not _scale_init:
		_scale_start_dist = dist if dist > 0.01 else 0.01
		_scale_init = true
		return
	var factor = dist / _scale_start_dist
	var new_s = _scale_orig * factor
	new_s = clamp(new_s, 0.1, 10.0)
	_workspace.selected_atom.scale = Vector3(new_s, new_s, new_s)

func _fmt_sci(value: float) -> String:
	if value == 0.0:
		return "0"
	if is_inf(value) or is_nan(value):
		return "—"
	var abs_v = abs(value)
	if abs_v < 1e-4 or abs_v >= 1e6:
		var exp_n = int(floor(log(abs_v) / log(10.0)))
		var mantissa = value / pow(10.0, exp_n)
		return "%.2f×10^%d" % [mantissa, exp_n]
	return "%.4f" % value

func _try_l_connect(screen_pos: Vector2):
	var target = _find_atom_at(screen_pos)
	if not target:
		return
	if _secondary_selected_atoms.size() == 1:
		var sec = _secondary_selected_atoms[0]
		if target != sec:
			_connect_and_arrange(sec, target)
		return
	if _secondary_selected_atoms.size() > 1:
		if not (target in _secondary_selected_atoms):
			_l_connect_target = target
			_show_secondary_connect_menu(screen_pos)
		return
	if _selected_atoms.size() > 1 and not (target in _selected_atoms):
		_l_connect_target = target
		_show_mol_connect_menu(screen_pos)
	elif _workspace.selected_atom and target != _workspace.selected_atom:
		_connect_and_arrange(_workspace.selected_atom, target)

func _connect_and_arrange(a: Atom3D, b: Atom3D):
	var data_a = ElementDB.get_element(a.element_symbol)
	var data_b = ElementDB.get_element(b.element_symbol)
	var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
	var r_b = float(data_b.get("covalent_radius_pm", 50)) / 100.0
	var ideal_length = r_a + r_b
	var direction = (b.global_position - a.global_position)
	if direction.length() < 0.01:
		direction = _camera.global_transform.basis.x
	direction = direction.normalized()
	b.position = a.position + direction * ideal_length
	_workspace.add_bond(a, b)
	_update_status("L连接: %s-%s (键长%.3fÅ)" % [a.element_symbol, b.element_symbol, ideal_length])

func _on_geometry_menu_id(id: int):
	match id:
		100:
			# 无选中时作用于全部原子 (点击即有效, 不再静默要求先框选)
			var targets = _selected_atoms if not _selected_atoms.is_empty() else _workspace.atoms.duplicate()
			if targets.is_empty():
				_update_status("工作区无原子可连接")
				return
			_auto_connect(targets)
			var formulas = _auto_tag_molecules(targets)
			if formulas.is_empty():
				_update_status("已自动连接 %d 原子 (未形成分子)" % targets.size())
			else:
				_update_status("已自动连接 → 分子: %s (%d 原子)" % [", ".join(formulas), targets.size()])
				_formula_label.text = "化学式: %s" % " + ".join(formulas)
		101: _arrange_geometry("linear", _selected_atoms)
		102: _arrange_geometry("bent", _selected_atoms)
		103: _arrange_geometry("trigonal_planar", _selected_atoms)
		104: _arrange_geometry("tetrahedral", _selected_atoms)
		105: _arrange_geometry("octahedral", _selected_atoms)

func _arrange_geometry(geometry: String, atoms: Array):
	if atoms.size() < 2:
		_update_status("至少需要2个原子")
		return
	var center = atoms[0]
	for atom in atoms:
		if atom.atomic_number > center.atomic_number:
			center = atom
	var surrounding = []
	for atom in atoms:
		if atom != center:
			surrounding.append(atom)
	_arrange_around_center(center, surrounding, geometry)
	var formula = _compute_formula(atoms)
	var gname = _geometry_name(geometry)
	_formula_label.text = "化学式: %s (%s)" % [formula, gname]
	_update_status("已按%s排列 %d 原子 → %s" % [gname, atoms.size(), formula])

func _arrange_around_center(center: Atom3D, surrounding: Array, geometry: String):
	var center_pos = center.position
	var data_c = ElementDB.get_element(center.element_symbol)
	var r_c = float(data_c.get("covalent_radius_pm", 50)) / 100.0
	var positions = []
	match geometry:
		"linear":
			for i in range(surrounding.size()):
				var s = 1.0 if i % 2 == 0 else -1.0
				positions.append(Vector3(s * (i / 2 + 1), 0, 0))
		"bent":
			var angle = 104.5 * PI / 180.0
			for i in range(surrounding.size()):
				var theta = angle / 2.0 - i * angle
				positions.append(Vector3(sin(theta), 0, cos(theta)))
		"trigonal_planar":
			for i in range(surrounding.size()):
				var theta = i * 2.0 * PI / 3.0
				positions.append(Vector3(cos(theta), 0, sin(theta)))
		"tetrahedral":
			var tetra = [Vector3(1,1,1), Vector3(1,-1,-1), Vector3(-1,1,-1), Vector3(-1,-1,1)]
			for i in range(surrounding.size()):
				positions.append(tetra[i % 4].normalized())
		"octahedral":
			var oct = [Vector3(1,0,0), Vector3(-1,0,0), Vector3(0,1,0), Vector3(0,-1,0), Vector3(0,0,1), Vector3(0,0,-1)]
			for i in range(surrounding.size()):
				positions.append(oct[i % 6])
	for i in range(surrounding.size()):
		var atom = surrounding[i]
		var data_a = ElementDB.get_element(atom.element_symbol)
		var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
		var bond_len = r_c + r_a
		atom.position = center_pos + positions[i] * bond_len
		_workspace.add_bond(center, atom)

func _show_mol_connect_menu(screen_pos: Vector2):
	var mol_formula = _compute_formula(_selected_atoms)
	var target_sym = _l_connect_target.element_symbol
	var combined = _selected_atoms.duplicate()
	combined.append(_l_connect_target)
	var combined_formula = _compute_formula(combined)
	_update_status("分子 %s + %s → %s | 选择连接方式" % [mol_formula, target_sym, combined_formula])
	_mol_connect_menu.hide()
	_mol_connect_menu.size = Vector2i(220, 0)
	_mol_connect_menu.popup(Rect2(screen_pos, Vector2(220, 0)))

func _on_mol_connect_menu_id(id: int):
	if not _l_connect_target or _selected_atoms.is_empty():
		return
	var target = _l_connect_target
	match id:
		200: _connect_nearest_in_mol(target)
		201: _connect_center_in_mol(target)
		202: _connect_all_in_mol(target)
		203: _arrange_mol_to_target("linear", target)
		204: _arrange_mol_to_target("bent", target)
		205: _arrange_mol_to_target("trigonal_planar", target)
		206: _arrange_mol_to_target("tetrahedral", target)
		207: _arrange_mol_to_target("octahedral", target)

func _connect_nearest_in_mol(target: Atom3D):
	if _selected_atoms.is_empty() or not is_instance_valid(target):
		return
	var nearest = _selected_atoms[0]
	var min_dist = nearest.global_position.distance_to(target.global_position)
	for atom in _selected_atoms:
		if not is_instance_valid(atom):
			continue
		var d = atom.global_position.distance_to(target.global_position)
		if d < min_dist:
			min_dist = d
			nearest = atom
	_connect_and_arrange(nearest, target)

func _connect_center_in_mol(target: Atom3D):
	var center = _selected_atoms[0]
	for atom in _selected_atoms:
		if atom.atomic_number > center.atomic_number:
			center = atom
	_connect_and_arrange(center, target)

func _connect_all_in_mol(target: Atom3D):
	for atom in _selected_atoms:
		if atom != target:
			_connect_and_arrange(atom, target)
	_update_status("已连接全部 %d 原子到 %s" % [_selected_atoms.size(), target.element_symbol])

func _arrange_mol_to_target(geometry: String, target: Atom3D):
	var surrounding = []
	for atom in _selected_atoms:
		if atom != target:
			surrounding.append(atom)
	_arrange_around_center(target, surrounding, geometry)
	var all_atoms = surrounding.duplicate()
	all_atoms.append(target)
	var formula = _compute_formula(all_atoms)
	var gname = _geometry_name(geometry)
	_formula_label.text = "化学式: %s (%s)" % [formula, gname]
	_update_status("已按%s排列分子到%s → %s" % [gname, target.element_symbol, formula])

func _geometry_name(g: String) -> String:
	match g:
		"linear": return "线型"
		"bent": return "折线型"
		"trigonal_planar": return "三角平面"
		"tetrahedral": return "四面体"
		"octahedral": return "八面体"
		_: return g

func _is_molecule_selected() -> bool:
	for atom in _selected_atoms:
		if _atom_to_molecule.has(atom):
			return true
	return false

func _is_connected_group(atoms: Array) -> bool:
	if atoms.size() <= 1:
		return false
	var atom_set = {}
	for atom in atoms:
		atom_set[atom] = true
	var visited = {}
	var queue = [atoms[0]]
	visited[atoms[0]] = true
	while queue.size() > 0:
		var current = queue.pop_front()
		for bond in _workspace.bonds:
			var neighbor = null
			if bond.atom_a == current and atom_set.has(bond.atom_b):
				neighbor = bond.atom_b
			elif bond.atom_b == current and atom_set.has(bond.atom_a):
				neighbor = bond.atom_a
			if neighbor and not visited.has(neighbor):
				visited[neighbor] = true
				queue.append(neighbor)
	return visited.size() == atoms.size()

## 标记分子; silent=true 时供自动标记路径调用 (不成组/已分组则静默跳过)
## 返回是否成功成组
func _tag_as_molecule(atoms: Array, silent: bool = false) -> bool:
	if atoms.size() < 2:
		if not silent:
			_update_status("至少需要2个原子才能标记为分子")
		return false
	if not _is_connected_group(atoms):
		if not silent:
			_update_status("选中的原子未通过化学键连接，无法标记为分子")
		return false
	for atom in atoms:
		if _atom_to_molecule.has(atom):
			if not silent:
				_update_status("部分原子已属于分子，请先取消标记")
			return false
	var gid = _molecule_groups.size()
	var group = {
		"atoms": atoms.duplicate(),
		"label": _compute_formula(atoms),
		"id": gid
	}
	_molecule_groups.append(group)
	for atom in atoms:
		_atom_to_molecule[atom] = gid
	if not silent:
		_update_status("已标记分子: %s (%d 原子) | S+点击=二级选中" % [group["label"], atoms.size()])
	return true

func _get_molecule_group(gid: int):
	if gid < 0 or gid >= _molecule_groups.size():
		return null
	var g = _molecule_groups[gid]
	if g == null or g.get("atoms", []).is_empty():
		return null
	return g

func _select_molecule_group(gid: int):
	if gid < 0 or gid >= _molecule_groups.size():
		return
	var group = _molecule_groups[gid]
	if group == null or group.get("atoms", []).is_empty():
		return
	for atom in _selected_atoms:
		atom.set_selected(false)
	_selected_atoms.clear()
	for atom in group["atoms"]:
		atom.set_selected(true)
		_selected_atoms.append(atom)
	_workspace.selected_atom = group["atoms"][0]
	_update_gizmo_pos()
	_gizmo.visible = true
	Events.emit_signal("atom_selected", _workspace.selected_atom)
	_update_status("已选中分子: %s (%d 原子) | S+点击=二级选中 | L+点击=连接" % [group["label"], group["atoms"].size()])

func _try_secondary_select(screen_pos: Vector2, multi: bool):
	var target = _find_atom_at(screen_pos)
	if not target:
		return
	if not _atom_to_molecule.has(target):
		_update_status("该原子不属于分子，无法二级选中")
		return
	var gid = _atom_to_molecule[target]
	var group = _get_molecule_group(gid)
	if group == null:
		_update_status("该分子已失效，无法二级选中")
		return
	var in_selected = false
	for atom in _selected_atoms:
		if atom == target:
			in_selected = true
			break
	if not in_selected:
		_select_molecule_group(gid)
		_clear_secondary()
	if multi:
		if target in _secondary_selected_atoms:
			_secondary_selected_atoms.erase(target)
			target.set_secondary(false)
			target.set_selected(true)
		else:
			_secondary_selected_atoms.append(target)
			target.set_secondary(true)
	else:
		_clear_secondary()
		_secondary_selected_atoms.append(target)
		target.set_secondary(true)
	_workspace.selected_atom = target
	_update_gizmo_pos()
	_gizmo.visible = true
	if _secondary_selected_atoms.size() > 1:
		var syms = []
		for a in _secondary_selected_atoms:
			syms.append(a.element_symbol)
		_update_status("二级选中 %d 锚点 %s | L+点击=以锚点连接(保持分子结构)" % [_secondary_selected_atoms.size(), str(syms)])
	else:
		_update_status("二级选中: %s | L+点击=连接 | Ctrl+S=多选锚点" % target.get_info_text())

func _clear_secondary():
	for atom in _secondary_selected_atoms:
		atom.set_secondary(false)
	_secondary_selected_atoms.clear()

func _try_ctrl_select(screen_pos: Vector2):
	if _is_in_bottom_viewport(screen_pos):
		var stroke_idx = _find_stroke_at_screen_pos(screen_pos)
		if stroke_idx >= 0:
			_select_stroke(stroke_idx, true)
		return
	if not _is_in_top_viewport(screen_pos):
		return
	var target = _find_atom_at(screen_pos)
	if not target:
		return
	_clear_secondary()
	if _atom_to_molecule.has(target):
		var gid = _atom_to_molecule[target]
		var group = _get_molecule_group(gid)
		if group == null:
			_update_status("该分子已失效")
			return
		var already = true
		for atom in group["atoms"]:
			if not (atom in _selected_atoms):
				already = false
				break
		if already:
			for atom in group["atoms"]:
				atom.set_selected(false)
				_selected_atoms.erase(atom)
		else:
			for atom in group["atoms"]:
				if not (atom in _selected_atoms):
					atom.set_selected(true)
					_selected_atoms.append(atom)
		if _selected_atoms.size() > 0:
			_workspace.selected_atom = _selected_atoms[0]
			_update_gizmo_pos()
			_gizmo.visible = true
		else:
			_workspace.selected_atom = null
			_gizmo.visible = false
		_update_status("Ctrl多选: %d 原子/分子 | 右键=结合连接" % _selected_atoms.size())
	else:
		if target in _selected_atoms:
			target.set_selected(false)
			_selected_atoms.erase(target)
		else:
			target.set_selected(true)
			_selected_atoms.append(target)
		if _selected_atoms.size() > 0:
			_workspace.selected_atom = _selected_atoms[0]
			_update_gizmo_pos()
			_gizmo.visible = true
			Events.emit_signal("atom_selected", _workspace.selected_atom)
		else:
			_workspace.selected_atom = null
			_gizmo.visible = false
		_update_status("Ctrl多选: %d 原子 | 右键=结合连接" % _selected_atoms.size())

func _show_secondary_connect_menu(screen_pos: Vector2):
	var anchors = _secondary_selected_atoms
	var target = _l_connect_target
	var mol_formula = ""
	for atom in _selected_atoms:
		if _atom_to_molecule.has(atom):
			var gid = _atom_to_molecule[atom]
			var g = _get_molecule_group(gid)
			if g != null:
				mol_formula = g["label"]
				break
	if mol_formula == "":
		mol_formula = _compute_formula(_selected_atoms)
	var combined = _selected_atoms.duplicate()
	if not (target in combined):
		combined.append(target)
	var combined_formula = _compute_formula(combined)
	_update_status("锚点%d + %s → %s | 保持原分子结构" % [anchors.size(), target.element_symbol, combined_formula])
	_secondary_connect_menu.hide()
	_secondary_connect_menu.size = Vector2i(220, 0)
	_secondary_connect_menu.popup(Rect2(screen_pos, Vector2(220, 0)))

func _on_secondary_connect_menu_id(id: int):
	if _secondary_selected_atoms.is_empty() or not _l_connect_target:
		return
	var target = _l_connect_target
	match id:
		300: _connect_all_anchors(target)
		301: _connect_nearest_anchor(target)
		302: _connect_centroid_anchor(target)
		303: _arrange_via_anchors("linear", target)
		304: _arrange_via_anchors("bent", target)
		305: _arrange_via_anchors("trigonal_planar", target)
		306: _arrange_via_anchors("tetrahedral", target)
		307: _arrange_via_anchors("octahedral", target)

func _anchor_centroid() -> Vector3:
	if _secondary_selected_atoms.is_empty():
		return Vector3.ZERO
	var c = Vector3.ZERO
	for a in _secondary_selected_atoms:
		if is_instance_valid(a):
			c += a.global_position
	return c / _secondary_selected_atoms.size()

func _anchor_normal() -> Vector3:
	if _secondary_selected_atoms.is_empty() or not is_instance_valid(_l_connect_target):
		return Vector3.UP
	if _secondary_selected_atoms.size() == 1:
		return (_l_connect_target.global_position - _secondary_selected_atoms[0].global_position).normalized()
	var c = _anchor_centroid()
	var n = Vector3.ZERO
	for a in _secondary_selected_atoms:
		if not is_instance_valid(a):
			continue
		var d = (a.global_position - c).normalized()
		n += d
	if n.length() < 0.01 and _secondary_selected_atoms.size() >= 2:
		var a0 = _secondary_selected_atoms[0].global_position
		var a1 = _secondary_selected_atoms[1].global_position
		var bond_dir = (a1 - a0).normalized()
		n = bond_dir.cross(Vector3.UP).normalized()
		if n.length() < 0.01:
			n = bond_dir.cross(Vector3.FORWARD).normalized()
	else:
		n = -n.normalized()
	return n

func _connect_all_anchors(target: Atom3D):
	if _secondary_selected_atoms.is_empty() or not is_instance_valid(target):
		return
	var data_t = ElementDB.get_element(target.element_symbol)
	var r_t = float(data_t.get("covalent_radius_pm", 50)) / 100.0
	var avg_bond = 0.0
	for a in _secondary_selected_atoms:
		if not is_instance_valid(a):
			continue
		var data_a = ElementDB.get_element(a.element_symbol)
		var r_a = float(data_a.get("covalent_radius_pm", 50)) / 100.0
		avg_bond += r_a + r_t
		_workspace.add_bond(a, target)
	avg_bond /= max(_secondary_selected_atoms.size(), 1)
	var n = _anchor_normal()
	target.position = _anchor_centroid() + n * avg_bond
	_update_status("全部锚点连接: %d锚点→%s (保持分子结构)" % [_secondary_selected_atoms.size(), target.element_symbol])

func _connect_nearest_anchor(target: Atom3D):
	if _secondary_selected_atoms.is_empty() or not is_instance_valid(target):
		return
	var nearest = _secondary_selected_atoms[0]
	var min_d = nearest.global_position.distance_to(target.global_position)
	for a in _secondary_selected_atoms:
		var d = a.global_position.distance_to(target.global_position)
		if d < min_d:
			min_d = d
			nearest = a
	_connect_and_arrange(nearest, target)
	_update_status("最近锚点连接: %s→%s (保持分子结构)" % [nearest.element_symbol, target.element_symbol])

func _connect_centroid_anchor(target: Atom3D):
	var centroid = _anchor_centroid()
	var nearest = _secondary_selected_atoms[0]
	var min_d = nearest.global_position.distance_to(centroid)
	for a in _secondary_selected_atoms:
		var d = a.global_position.distance_to(centroid)
		if d < min_d:
			min_d = d
			nearest = a
	var data_n = ElementDB.get_element(nearest.element_symbol)
	var data_t = ElementDB.get_element(target.element_symbol)
	var r_n = float(data_n.get("covalent_radius_pm", 50)) / 100.0
	var r_t = float(data_t.get("covalent_radius_pm", 50)) / 100.0
	var bond_len = r_n + r_t
	var n = _anchor_normal()
	target.position = centroid + n * bond_len
	_workspace.add_bond(nearest, target)
	_update_status("质心锚点连接: 质心→%s (保持分子结构)" % target.element_symbol)

func _arrange_via_anchors(geometry: String, target: Atom3D):
	if _secondary_selected_atoms.is_empty() or not is_instance_valid(target):
		return
	var centroid = _anchor_centroid()
	var n = _anchor_normal()
	var data_t = ElementDB.get_element(target.element_symbol)
	var r_t = float(data_t.get("covalent_radius_pm", 50)) / 100.0
	var avg_r = 0.0
	for a in _secondary_selected_atoms:
		if not is_instance_valid(a):
			continue
		var data_a = ElementDB.get_element(a.element_symbol)
		avg_r += float(data_a.get("covalent_radius_pm", 50)) / 100.0
	avg_r /= max(_secondary_selected_atoms.size(), 1)
	var bond_len = avg_r + r_t
	var offset_dir = n
	match geometry:
		"linear":
			target.position = centroid + offset_dir * bond_len
		"bent":
			var angle = 104.5 * PI / 180.0
			target.position = centroid + (offset_dir * cos(angle) + Vector3.UP * sin(angle)) * bond_len
		"trigonal_planar":
			var angle = 120.0 * PI / 180.0
			target.position = centroid + (offset_dir * cos(angle) + Vector3.UP * sin(angle)) * bond_len
		"tetrahedral":
			var angle = 109.47 * PI / 180.0
			target.position = centroid + (offset_dir * cos(angle) + Vector3.UP * sin(angle)) * bond_len
		"octahedral":
			target.position = centroid + offset_dir * bond_len
	for a in _secondary_selected_atoms:
		_workspace.add_bond(a, target)
	var gname = _geometry_name(geometry)
	_update_status("锚点%s排列: %d锚点→%s (保持分子结构)" % [gname, _secondary_selected_atoms.size(), target.element_symbol])

# === 保存/加载/导出 ===

func _setup_file_dialog():
	_file_dialog = FileDialog.new()
	_file_dialog.access = FileDialog.ACCESS_FILESYSTEM
	_file_dialog.file_mode = FileDialog.FILE_MODE_SAVE_FILE
	_file_dialog.add_filter("*.cqm", "CQM项目文件")
	_file_dialog.size = Vector2i(600, 400)
	add_child(_file_dialog)
	_file_dialog.file_selected.connect(_on_file_selected)

func _save_project_dialog():
	_file_dialog_mode = 0
	_file_dialog.file_mode = FileDialog.FILE_MODE_SAVE_FILE
	_file_dialog.title = "保存项目"
	_file_dialog.current_file = "project.cqm"
	_file_dialog.popup_centered()

func _load_project_dialog():
	_file_dialog_mode = 1
	_file_dialog.file_mode = FileDialog.FILE_MODE_OPEN_FILE
	_file_dialog.title = "加载项目"
	_file_dialog.current_file = ""
	_file_dialog.popup_centered()

func _export_dialog():
	_file_dialog_mode = 2
	_file_dialog.file_mode = FileDialog.FILE_MODE_SAVE_FILE
	_file_dialog.title = "导出"
	_file_dialog.clear_filters()
	_file_dialog.add_filter("*.csv", "CSV计算结果")
	_file_dialog.add_filter("*.md", "Markdown学术报告")
	_file_dialog.add_filter("*.xyz", "XYZ 坐标文件")
	_file_dialog.add_filter("*.pdb", "PDB 蛋白质数据库格式")
	_file_dialog.add_filter("*.cif", "CIF 晶体学信息框架")
	_file_dialog.add_filter("*.poscar", "VASP POSCAR 格式")
	_file_dialog.add_filter("*.in", "Quantum ESPRESSO pw.x 输入")
	_file_dialog.add_filter("*.sdf", "SDF 结构数据文件")
	_file_dialog.current_file = "structure.xyz"
	_file_dialog.popup_centered()

func _on_file_selected(path: String):
	match _file_dialog_mode:
		0:
			var params = _selected_group_params if not _selected_strokes.is_empty() else _default_physical_params()
			var meta = {
				"material_name": _current_material_name,
				"formula": _compute_formula(_workspace.atoms) if not _workspace.atoms.is_empty() else "",
			}
			if ProjectManager.save_project(path, _workspace, _brush_strokes, _custom_molecules,
					params, {"metadata": meta, "results": _last_results}):
				_update_status("项目已保存: %s" % path)
			else:
				_update_status("保存失败: %s" % path)
		1:
			var data = ProjectManager.load_project(path)
			if data.is_empty():
				_update_status("加载失败: %s" % path)
				return
			_reset_selection_state()
			var restored = ProjectManager.apply_loaded_data(data, _workspace)
			_brush_strokes = restored.get("brush_strokes", [])
			_custom_molecules = restored.get("custom_molecules", [])
			var saved_params = restored.get("physics_params", {})
			if not saved_params.is_empty():
				_selected_group_params = saved_params
				_update_physics_panel()
			var saved_meta: Dictionary = data.get("metadata", {})
			_current_material_name = str(saved_meta.get("material_name", ""))
			var saved_results: Dictionary = data.get("results", {})
			if not saved_results.is_empty():
				_last_results = saved_results
				_on_results(saved_results)
			_refresh_brush_atom_render()
			_update_annotations()
			_take_undo_snapshot()
			_update_status("项目已加载: %d原子 %d键 %d笔划%s" % [_workspace.atoms.size(), _workspace.bonds.size(), _brush_strokes.size(),
				" (含计算结果)" if not saved_results.is_empty() else ""])
		2:
			var ext = path.get_extension().to_lower()
			if ext == "csv":
				if _last_results.is_empty():
					_update_status("无计算结果可导出")
					return
				if ProjectManager.export_results_csv(path, _last_results):
					_update_status("结果已导出: %s" % path)
				else:
					_update_status("导出失败: %s" % path)
			elif ext == "md":
				if _last_results.is_empty():
					_update_status("无计算结果可导出 (请先按 F5 计算)")
					return
				var bench: Dictionary = {}
				if not _workspace.atoms.is_empty():
					bench = SCData.find_benchmark(_compute_formula(_workspace.atoms))
				var info = {
					"material_name": _current_material_name if _current_material_name != "" else "工作区结构",
					"formula": _compute_formula(_workspace.atoms),
					"benchmark": bench,
				}
				if ProjectManager.export_report_md(path, _last_results, info):
					_update_status("学术报告已导出: %s" % path)
				else:
					_update_status("报告导出失败: %s" % path)
			elif ext == "in":
				if _workspace.atoms.is_empty():
					_update_status("无原子可导出")
					return
				var qe_title = "cqm_structure"
				if _current_material_name != "":
					qe_title = _current_material_name.get_file().get_basename()
				var qe_text = StructureIO.export_qe_input(_workspace.atoms, qe_title)
				var qf = FileAccess.open(path, FileAccess.WRITE)
				if qf:
					qf.store_string(qe_text)
					qf.close()
					_update_status("QE 输入已导出: %s (%d原子, SCF模板)" % [path, _workspace.atoms.size()])
				else:
					_update_status("QE 导出失败: %s" % path)
			else:
				if StructureIO.export_to_format(_workspace.atoms, _workspace.bonds, ext, path):
					_update_status("结构已导出: %s (%d原子)" % [path, _workspace.atoms.size()])
				else:
					_update_status("导出失败: %s" % path)
		3:
			_import_structure(path)
	_file_dialog.clear_filters()
	_file_dialog.add_filter("*.cqm", "CQM项目文件")

# === 撤销/重做 ===

func _take_undo_snapshot():
	if _undo_manager:
		_undo_manager.push_snapshot(_undo_manager.take_snapshot(_workspace, _brush_strokes))

func _do_undo():
	if not _undo_manager:
		return
	_reset_selection_state()
	var restored = _undo_manager.undo(_workspace, _brush_strokes)
	if restored.has("brush_strokes"):
		_brush_strokes = restored["brush_strokes"]
	_rebuild_molecule_groups()
	_refresh_brush_atom_render()
	_update_annotations()
	_update_status("撤销")

func _do_redo():
	if not _undo_manager:
		return
	_reset_selection_state()
	var restored = _undo_manager.redo(_workspace, _brush_strokes)
	if restored.has("brush_strokes"):
		_brush_strokes = restored["brush_strokes"]
	_rebuild_molecule_groups()
	_refresh_brush_atom_render()
	_update_annotations()
	_update_status("重做")

## 按键连通分量重建分子组 (撤销/重做后调用; 语义: 成键连接的整体=分子)
func _rebuild_molecule_groups():
	_molecule_groups = []
	_atom_to_molecule = {}
	var visited := {}
	for atom in _workspace.atoms:
		if not is_instance_valid(atom) or visited.has(atom):
			continue
		var comp: Array = []
		var queue = [atom]
		visited[atom] = true
		while queue.size() > 0:
			var cur = queue.pop_front()
			comp.append(cur)
			for bond in _workspace.bonds:
				var nb = null
				if bond.atom_a == cur:
					nb = bond.atom_b
				elif bond.atom_b == cur:
					nb = bond.atom_a
				if nb != null and not visited.has(nb):
					visited[nb] = true
					queue.append(nb)
		if comp.size() >= 2:
			_tag_as_molecule(comp, true)

func _on_undo_state_changed(can_undo: bool, can_redo: bool):
	if _undo_btn:
		_undo_btn.disabled = not can_undo
	if _redo_btn:
		_redo_btn.disabled = not can_redo

# === 测量工具 ===

func _toggle_measure_mode():
	_measure_mode = not _measure_mode
	_measure_atoms.clear()
	if _measure_btn:
		_measure_btn.modulate = Color(0.3, 0.9, 0.4) if _measure_mode else Color(1, 1, 1)
	if _measure_mode:
		_update_status("测量模式: 选中2=距离 3=角度 4=/二面角")
	else:
		_update_status("测量模式关闭")
		if _measure_label:
			_measure_label.text = ""

func _update_measurement():
	if not _measure_mode or _measure_atoms.size() < 2:
		if _measure_label:
			_measure_label.text = ""
		return
	var positions: Array = []
	for atom in _measure_atoms:
		if is_instance_valid(atom):
			positions.append(atom.global_position)
	var result = MeasurementTool.measure(positions)
	if _measure_label:
		_measure_label.text = result.get("label", "")
	_update_status(result.get("label", ""))

# === 等效几何窗口 ===

func _show_geometry_window():
	var atoms_to_show: Array = _selected_atoms if not _selected_atoms.is_empty() else _workspace.atoms
	if atoms_to_show.is_empty():
		_update_status("无选中原子可显示等效几何")
		return
	_geo_window = AcceptDialog.new()
	_geo_window.title = "等效几何构型 (%d原子)" % atoms_to_show.size()
	_geo_window.size = Vector2i(500, 600)
	_geo_window.exclusive = false
	add_child(_geo_window)
	var container = VBoxContainer.new()
	_geo_window.add_child(container)
	var info_text = "选中原子等效几何信息:\n\n"
	var positions: Array = []
	for atom in atoms_to_show:
		if is_instance_valid(atom):
			positions.append(atom.global_position)
			info_text += "  %s (A=%d) @ (%.3f, %.3f, %.3f)\n" % [atom.element_symbol, atom.isotope_mass, atom.global_position.x, atom.global_position.y, atom.global_position.z]
	var bbox = MeasurementTool.bounding_box(positions)
	info_text += "\n包围盒:\n"
	info_text += "  最小: (%.3f, %.3f, %.3f)\n" % [bbox.min.x, bbox.min.y, bbox.min.z]
	info_text += "  最大: (%.3f, %.3f, %.3f)\n" % [bbox.max.x, bbox.max.y, bbox.max.z]
	info_text += "  尺寸: (%.3f, %.3f, %.3f)\n" % [bbox.size.x, bbox.size.y, bbox.size.z]
	info_text += "  中心: (%.3f, %.3f, %.3f)\n" % [bbox.center.x, bbox.center.y, bbox.center.z]
	var com = MeasurementTool.center_of_mass(positions)
	info_text += "\n质心: (%.3f, %.3f, %.3f)\n" % [com.x, com.y, com.z]
	if positions.size() >= 2:
		info_text += "\n键长统计:\n"
		for i in range(positions.size()):
			for j in range(i + 1, positions.size()):
				var d = positions[i].distance_to(positions[j])
				info_text += "  d(%d-%d) = %.4f Å\n" % [i, j, d]
	if positions.size() >= 3:
		info_text += "\n键角统计:\n"
		for i in range(positions.size()):
			for j in range(positions.size()):
				if i == j:
					continue
				for k in range(j + 1, positions.size()):
					if k == i:
						continue
					var ang = MeasurementTool.measure_angle(positions[i], positions[j], positions[k])
					info_text += "  ∠(%d-%d-%d) = %.2f°\n" % [i, j, k, ang.value]
	var mom = MeasurementTool.principal_moments(positions)
	info_text += "\n惯性张量:\n"
	info_text += "  Ixx=%.4f Iyy=%.4f Izz=%.4f\n" % [mom.ixx, mom.iyy, mom.izz]
	info_text += "  Ixy=%.4f Ixz=%.4f Iyz=%.4f\n" % [mom.ixy, mom.ixz, mom.iyz]
	var lbl = Label.new()
	lbl.text = info_text
	lbl.add_theme_font_size_override("font_size", 12)
	lbl.add_theme_color_override("font_color", Color(0.85, 0.88, 0.95))
	container.add_child(lbl)
	_geo_window.confirmed.connect(func(): _geo_window.queue_free())
	_geo_window.canceled.connect(func(): _geo_window.queue_free())
	_geo_window.popup_centered()
	_update_status("等效几何窗口: %d原子" % atoms_to_show.size())

# === 导入结构 ===

func _import_structure_dialog():
	if not _file_dialog:
		_setup_file_dialog()
	_file_dialog.file_mode = FileDialog.FILE_MODE_OPEN_FILE
	_file_dialog.filters = PackedStringArray([
		"*.xyz ; XYZ 坐标文件",
		"*.pdb ; PDB 蛋白质数据库格式",
		"*.cif ; CIF 晶体学信息框架",
		"*.poscar ; VASP POSCAR 格式",
		"*.sdf ; SDF 结构数据文件",
		"*.mol ; MOL MDL分子文件"
	])
	_file_dialog.title = "导入结构文件"
	_file_dialog_mode = 3
	_file_dialog.popup_centered()

func _import_structure(path: String):
	var result = StructureIO.import_from_file(path)
	if result.has("error"):
		_update_status("导入失败: %s" % result.error)
		return
	var atoms = result.get("atoms", [])
	var bonds = result.get("bonds", [])
	if atoms.is_empty():
		_update_status("导入文件无有效原子")
		return
	for atom in atoms:
		var sym = atom.get("symbol", "H")
		var pos = atom.get("position", Vector3.ZERO)
		var data = ElementDB.get_element(sym)
		if data.is_empty():
			continue
		var isotopes = data.get("isotopes", [])
		var iso = 0
		if not isotopes.is_empty():
			for iso_data in isotopes:
				if bool(iso_data.get("is_stable", false)):
					iso = int(iso_data.get("mass_number", 1))
					break
			if iso == 0:
				iso = int(isotopes[0].get("mass_number", 1))
		_workspace.add_atom(sym, iso, pos)
	for bond_info in bonds:
		var a_idx = int(bond_info.get("a", -1))
		var b_idx = int(bond_info.get("b", -1))
		if a_idx >= 0 and b_idx >= 0 and a_idx < _workspace.atoms.size() and b_idx < _workspace.atoms.size():
			_workspace.add_bond(_workspace.atoms[a_idx], _workspace.atoms[b_idx])
	_update_status("导入: %d原子 %d键 (%s)" % [atoms.size(), bonds.size(), path.get_file()])
	_take_undo_snapshot()
	_update_annotations()

# === 对称性检测 ===

func _detect_symmetry():
	if _workspace.atoms.is_empty():
		_update_status("无原子可检测对称性")
		return
	var result = SymmetryDetector.detect_point_group(_workspace.atoms)
	var pairing = SymmetryDetector.symmetry_to_pairing(result.group)
	var win = AcceptDialog.new()
	win.title = "对称性分析"
	win.size = Vector2i(450, 350)
	win.exclusive = false
	add_child(win)
	var container = VBoxContainer.new()
	win.add_child(container)
	var info = "点群: %s (阶=%d)\n" % [result.group, result.order]
	info += "描述: %s\n" % result.description
	info += "对称元素: %s\n" % str(result.elements)
	info += "主轴: (%.3f, %.3f, %.3f), %d重旋转\n" % [result.principal_axis.x, result.principal_axis.y, result.principal_axis.z, result.n_fold]
	info += "反演对称: %s\n" % ("是" if result.has_inversion else "否")
	info += "镜面数: %d\n" % result.mirror_planes.size()
	info += "\n超导配对推断:\n"
	info += "  配对类型: %s\n" % pairing.pairing
	info += "  对称性: %s\n" % pairing.symmetry
	info += "  节点: %s\n" % pairing.nodes
	info += "  说明: %s" % pairing.description
	var lbl = Label.new()
	lbl.text = info
	lbl.add_theme_font_size_override("font_size", 13)
	lbl.add_theme_color_override("font_color", Color(0.85, 0.88, 0.95))
	container.add_child(lbl)
	win.confirmed.connect(func(): win.queue_free())
	win.canceled.connect(func(): win.queue_free())
	win.popup_centered()
	_update_status("对称性: %s → %s" % [result.group, pairing.pairing])

# === 图表窗口 ===

func _show_chart_window():
	if _last_results.is_empty():
		_update_status("请先执行计算 (F5)")
		return
	_chart_window = Window.new()
	_chart_window.title = "超导性质图表"
	_chart_window.size = Vector2i(640, 520)
	add_child(_chart_window)
	var tabs = TabContainer.new()
	tabs.set_anchors_preset(Control.PRESET_FULL_RECT)
	_chart_window.add_child(tabs)

	var tc = float(_last_results.get("tc_estimate", 0.0))

	var tc_tab = ChartPlotter.new()
	tc_tab.name = "Tc相变"
	tabs.add_child(tc_tab)
	tc_tab.plot_tc_vs_temperature(tc)

	var eigenvalues = _last_results.get("eigenvalues", [])
	if not eigenvalues.is_empty():
		var dos_tab = ChartPlotter.new()
		dos_tab.name = "态密度"
		tabs.add_child(dos_tab)
		dos_tab.plot_dos(eigenvalues)

	var delta_0 = float(_last_results.get("gap_0", 0.0))
	if tc > 0 and delta_0 > 0:
		var gap_tab = ChartPlotter.new()
		gap_tab.name = "能隙"
		tabs.add_child(gap_tab)
		gap_tab.plot_gap_vs_temperature(tc, delta_0)

	var order_params = _last_results.get("order_parameters", [])
	if not order_params.is_empty():
		var order_tab = ChartPlotter.new()
		order_tab.name = "序参量"
		tabs.add_child(order_tab)
		order_tab.plot_order_parameters(order_params)

	var transitions = _last_results.get("cqm_stepwise", {}).get("transitions", [])
	if not transitions.is_empty():
		var step_tab = ChartPlotter.new()
		step_tab.name = "分步相变"
		tabs.add_child(step_tab)
		step_tab.plot_stepwise_transitions(transitions)

	var cf = _last_results.get("critical_fields", {})
	var hc1 = float(cf.get("hc1", 0.0))
	var hc2 = float(cf.get("hc2", 0.0))
	if hc1 > 0 or hc2 > 0:
		var hc_tab = ChartPlotter.new()
		hc_tab.name = "临界磁场"
		tabs.add_child(hc_tab)
		hc_tab.plot_critical_fields(hc1, hc2)

	_chart_window.close_requested.connect(func(): _chart_window.queue_free())
	_chart_window.popup_centered()

# === 高通量参数扫描窗口 ===

func _show_sweep_window():
	var atoms = _workspace.get_atom_data()
	var bonds = _workspace.get_bond_data()
	if atoms.is_empty():
		_update_status("扫描需要至少1个原子")
		return

	var win = Window.new()
	win.title = "高通量参数扫描"
	win.size = Vector2i(760, 600)
	add_child(win)
	var tabs = TabContainer.new()
	tabs.set_anchors_preset(Control.PRESET_FULL_RECT)
	win.add_child(tabs)

	var base_params = _default_physical_params()

	var p_tab = VBoxContainer.new()
	p_tab.name = "压强-Tc相图"
	tabs.add_child(p_tab)
	var p_chart = ChartPlotter.new()
	p_chart.custom_minimum_size = Vector2(740, 400)
	p_tab.add_child(p_chart)
	var p_info = Label.new()
	p_info.add_theme_font_size_override("font_size", 12)
	p_info.add_theme_color_override("font_color", Color(0.8, 0.86, 0.95))
	p_tab.add_child(p_info)

	var t0 = Time.get_ticks_msec()
	var p_sweep = CQMCalculator.sweep_pressure(atoms, bonds, base_params, 0.0, 200.0, 21)
	var dt = Time.get_ticks_msec() - t0
	var p_points: Array = []
	var best_tc = -1.0
	var best_p = 0.0
	for r in p_sweep:
		var tc = float(r.get("tc", 0.0))
		p_points.append(Vector2(float(r.get("pressure_GPa", 0.0)), tc))
		if tc > best_tc:
			best_tc = tc
			best_p = float(r.get("pressure_GPa", 0.0))
	p_chart.set_title("Tc - 压强 相图 (%d点, %dms)" % [p_sweep.size(), dt])
	p_chart.set_labels("压强 P (GPa)", "Tc (K)")
	p_chart.add_line_scatter_series(p_points, Color(0.9, 0.5, 0.3), "Tc(P)", 2.0, 4.0)
	p_info.text = "最高Tc: %s @ %s" % [
		PhysicsNotation.format_temperature(max(0.0, best_tc)),
		PhysicsNotation.format_pressure(best_p)]

	var i_tab = VBoxContainer.new()
	i_tab.name = "同位素效应"
	tabs.add_child(i_tab)
	var i_chart = ChartPlotter.new()
	i_chart.custom_minimum_size = Vector2(740, 400)
	i_tab.add_child(i_chart)
	var i_info = Label.new()
	i_info.add_theme_font_size_override("font_size", 12)
	i_info.add_theme_color_override("font_color", Color(0.8, 0.86, 0.95))
	i_info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	i_tab.add_child(i_info)

	t0 = Time.get_ticks_msec()
	var iso = CQMCalculator.sweep_isotope(atoms, bonds, base_params, 0.5, 2.0, 11)
	dt = Time.get_ticks_msec() - t0
	var i_points: Array = []
	for r in iso.get("points", []):
		i_points.append(Vector2(float(r.get("avg_mass", 0.0)), float(r.get("tc", 0.0))))
	i_chart.set_title("Tc - 同位素质量 (%d点, %dms)" % [i_points.size(), dt])
	i_chart.set_labels("平均同位素质量 (u)", "Tc (K)")
	i_chart.add_line_scatter_series(i_points, Color(0.4, 0.7, 1.0), "Tc(M)", 2.0, 4.0)
	var alpha = iso.get("alpha", NAN)
	if is_nan(alpha):
		i_info.text = "同位素效应指数 α: 无法拟合 (需多点非零Tc)"
	else:
		i_info.text = "同位素效应指数 α = %.3f  (BCS 理论值 α = 0.5)" % alpha

	var c_tab = VBoxContainer.new()
	c_tab.name = "二元成分扫描"
	tabs.add_child(c_tab)
	var c_ctrl = HBoxContainer.new()
	c_tab.add_child(c_ctrl)
	var c_a = OptionButton.new()
	var c_b = OptionButton.new()
	for z in range(1, 119):
		var ed = ElementDB.get_element_by_number(z)
		if ed.is_empty():
			continue
		var label = "%s %s" % [ed.get("symbol", ""), ed.get("name", "")]
		c_a.add_item(label)
		c_a.set_item_metadata(c_a.item_count - 1, ed.get("symbol", ""))
		c_b.add_item(label)
		c_b.set_item_metadata(c_b.item_count - 1, ed.get("symbol", ""))
	var first_sym = str(atoms[0].get("symbol", "Nb")) if atoms[0] is Dictionary else str(atoms[0].element_symbol)
	var default_a = 40
	var default_b = 22
	for z_idx in range(c_a.item_count):
		var meta = str(c_a.get_item_metadata(z_idx))
		if meta == first_sym:
			default_a = z_idx
		if meta == "Ti":
			default_b = z_idx
	c_a.selected = default_a
	c_b.selected = default_b
	c_ctrl.add_child(c_a)
	c_ctrl.add_child(c_b)
	var c_run = Button.new()
	c_run.text = "扫描"
	c_ctrl.add_child(c_run)
	var c_chart = ChartPlotter.new()
	c_chart.custom_minimum_size = Vector2(740, 380)
	c_tab.add_child(c_chart)
	var c_info = Label.new()
	c_info.add_theme_font_size_override("font_size", 12)
	c_info.add_theme_color_override("font_color", Color(0.8, 0.86, 0.95))
	c_info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	c_tab.add_child(c_info)

	c_run.pressed.connect(func():
		var sym_a = str(c_a.get_item_metadata(c_a.selected))
		var sym_b = str(c_b.get_item_metadata(c_b.selected))
		if sym_a == sym_b:
			c_info.text = "请选择两种不同元素"
			return
		var t_start = Time.get_ticks_msec()
		var comp = CQMCalculator.sweep_composition(sym_a, sym_b, 27, base_params, 11)
		var d_time = Time.get_ticks_msec() - t_start
		var c_points: Array = []
		for r in comp.get("points", []):
			c_points.append(Vector2(float(r.get("x", 0.0)), float(r.get("tc", 0.0))))
		c_chart.set_title("Tc - 成分 %s-%s (%d点, %dms, 27原子简立方)" % [
			sym_a, sym_b, c_points.size(), d_time])
		c_chart.set_labels("%s 摩尔分数 x (%s₁₋ₓ%s)" % [sym_b, sym_a, sym_b], "Tc (K)")
		c_chart.add_line_scatter_series(c_points, Color(0.6, 0.9, 0.5), "Tc(x)", 2.0, 4.0)
		var best_c = comp.get("best", {})
		if best_c.is_empty():
			c_info.text = "无有效数据点"
		else:
			var exp_a = SCData.get_experimental_tc(sym_a)
			var bench_txt = ""
			if not is_nan(exp_a) and exp_a > 0:
				bench_txt = " | %s 实验 Tc = %s" % [
					sym_a, PhysicsNotation.format_temperature(exp_a)]
			c_info.text = "最高Tc: %s @ x(%s) = %.2f%s\n成分: %s" % [
				PhysicsNotation.format_temperature(float(best_c.get("tc", 0.0))),
				sym_b, float(best_c.get("x", 0.0)), bench_txt,
				str(best_c.get("formula", ""))]
		_update_status("成分扫描完成: %s-%s %d点" % [sym_a, sym_b, c_points.size()])
	)
	c_run.pressed.emit()

	win.close_requested.connect(func(): win.queue_free())
	win.popup_centered()
	_update_status("扫描完成: %d 压强点 + %d 同位素点" % [p_sweep.size(), i_points.size()])

# === 标注切换 ===

func _toggle_atom_labels():
	_show_atom_labels = not _show_atom_labels
	if _show_labels_btn:
		_show_labels_btn.button_pressed = _show_atom_labels
	if _annotation_overlay:
		_annotation_overlay.set_show_atom_labels(_show_atom_labels)
	if _show_atom_labels:
		_update_annotations()
	_update_status("原子标签: %s" % ("显示" if _show_atom_labels else "隐藏"))

func _toggle_bond_labels():
	_show_bond_labels = not _show_bond_labels
	if _show_bond_labels_btn:
		_show_bond_labels_btn.button_pressed = _show_bond_labels
	if _annotation_overlay:
		_annotation_overlay.set_show_bond_labels(_show_bond_labels)
	if _show_bond_labels:
		_update_annotations()
	_update_status("键长标注: %s" % ("显示" if _show_bond_labels else "隐藏"))

func _update_annotations():
	if not _annotation_overlay:
		return
	_annotation_overlay.clear_all()
	if _show_atom_labels:
		for atom in _workspace.atoms:
			if is_instance_valid(atom):
				_annotation_overlay.add_atom_label(atom)
	if _show_bond_labels:
		for bond in _workspace.bonds:
			if is_instance_valid(bond):
				_annotation_overlay.add_bond_label(bond)

# === 替换笔划元素 ===

func _replace_stroke_element():
	if _selected_strokes.is_empty():
		_update_status("请先选中要替换的笔划")
		return
	var new_elem = _current_element
	var count = 0
	for idx in _selected_strokes:
		if idx >= 0 and idx < _brush_strokes.size():
			_brush_strokes[idx]["element"] = new_elem
			count += 1
	_refresh_brush_atom_render()
	_update_brush_trail()
	_update_status("已替换 %d 个笔划元素为 %s" % [count, new_elem])
