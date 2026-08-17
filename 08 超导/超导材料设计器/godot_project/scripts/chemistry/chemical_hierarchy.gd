extends Node
class_name ChemicalHierarchy

## 化学物质五层层次模型统一管理器
##
## 第一层：化学式 (FormulaLayer)       — 完全可控
## 第二层：结合方式 (ConnectivityLayer) — 高度可控
## 第三层：相对位置 (GeometryLayer)     — 部分可控
## 第四层：晶型 (CrystalFormLayer)      — 间接调控
## 第五层：晶型布局 (CrystalLayoutLayer)— 工艺涌现
##
## 核心规律：越往上层，自由度越离散，控制越精确；
##          越往下层，自由度越连续(或越复杂)，控制越依赖外部条件。

signal layer_changed(layer_index: int)
signal hierarchy_rebuilt()

var formula_layer: FormulaLayer
var connectivity_layer: ConnectivityLayer
var geometry_layer: GeometryLayer
var crystal_form_layer: CrystalFormLayer
var crystal_layout_layer: CrystalLayoutLayer

var _current_layer: int = 1
var _layer_history: Array = []

func _ready():
	formula_layer = FormulaLayer.new()
	connectivity_layer = ConnectivityLayer.new()
	geometry_layer = GeometryLayer.new()
	crystal_form_layer = CrystalFormLayer.new()
	crystal_layout_layer = CrystalLayoutLayer.new()
	_connect_signals()

func _connect_signals():
	formula_layer.composition_changed.connect(_on_formula_changed)
	connectivity_layer.topology_changed.connect(_on_connectivity_changed)
	geometry_layer.geometry_changed.connect(_on_geometry_changed)
	crystal_form_layer.crystal_form_changed.connect(_on_crystal_form_changed)
	crystal_layout_layer.microstructure_changed.connect(_on_crystal_layout_changed)

func get_layer(index: int) -> RefCounted:
	match index:
		1: return formula_layer
		2: return connectivity_layer
		3: return geometry_layer
		4: return crystal_form_layer
		5: return crystal_layout_layer
		_: return null

func get_layer_info(index: int) -> Dictionary:
	var layer = get_layer(index)
	if layer == null:
		return {}
	return {
		"index": index,
		"name": layer.get_layer_name(),
		"controllability": layer.get_controllability(),
		"description": layer.get_description(),
	}

func get_all_layer_info() -> Array:
	var result: Array = []
	for i in range(1, 6):
		result.append(get_layer_info(i))
	return result

func set_current_layer(index: int) -> void:
	if index < 1 or index > 5:
		return
	_current_layer = index
	layer_changed.emit(index)

func get_current_layer() -> int:
	return _current_layer

func build_from_formula(formula_str: String) -> void:
	var composition = formula_layer.parse_formula(formula_str)
	connectivity_layer.set_from_formula(composition)
	_layer_history.append({"action": "build_from_formula", "formula": formula_str})
	hierarchy_rebuilt.emit()

func build_from_composition(composition: Dictionary) -> void:
	formula_layer.set_composition(composition)
	connectivity_layer.set_from_formula(composition)
	_layer_history.append({"action": "build_from_composition", "composition": composition.duplicate()})
	hierarchy_rebuilt.emit()

func set_connectivity(atoms: Array, bonds: Array) -> void:
	connectivity_layer._atoms = atoms.duplicate(true)
	connectivity_layer._bonds = bonds.duplicate(true)
	connectivity_layer.topology_changed.emit()

func set_geometry(positions: Dictionary) -> void:
	geometry_layer.set_all_positions(positions)

func set_crystal_form(cell_params: Dictionary, space_group: int, z: int = 1) -> void:
	crystal_form_layer.set_cell_parameters(
		cell_params.a, cell_params.b, cell_params.c,
		cell_params.alpha, cell_params.beta, cell_params.gamma
	)
	crystal_form_layer.set_space_group(space_group)
	crystal_form_layer.set_z(z)

func set_microstructure(grain_size: float, morphology: String = "bulk") -> void:
	crystal_layout_layer.set_grain_size(grain_size)
	crystal_layout_layer.set_morphology(morphology)

func cascade_down(from_layer: int = 1) -> void:
	match from_layer:
		1:
			var comp = formula_layer.get_composition()
			connectivity_layer.set_from_formula(comp)
			_on_formula_changed(comp)
		2:
			_on_connectivity_changed()
		3:
			_on_geometry_changed()
		4:
			_on_crystal_form_changed()
	hierarchy_rebuilt.emit()

func _on_formula_changed(composition: Dictionary) -> void:
	layer_changed.emit(1)

func _on_connectivity_changed() -> void:
	layer_changed.emit(2)

func _on_geometry_changed() -> void:
	layer_changed.emit(3)

func _on_crystal_form_changed() -> void:
	layer_changed.emit(4)

func _on_crystal_layout_changed() -> void:
	layer_changed.emit(5)

func get_hierarchy_summary() -> Dictionary:
	return {
		"current_layer": _current_layer,
		"formula": formula_layer.to_dict(),
		"connectivity": connectivity_layer.to_dict(),
		"geometry": geometry_layer.to_dict(),
		"crystal_form": crystal_form_layer.to_dict(),
		"crystal_layout": crystal_layout_layer.to_dict(),
	}

func to_dict() -> Dictionary:
	return {
		"current_layer": _current_layer,
		"formula": formula_layer.to_dict(),
		"connectivity": connectivity_layer.to_dict(),
		"geometry": geometry_layer.to_dict(),
		"crystal_form": crystal_form_layer.to_dict(),
		"crystal_layout": crystal_layout_layer.to_dict(),
		"history": _layer_history.duplicate(true),
	}

func from_dict(data: Dictionary) -> void:
	if data.has("formula"):
		formula_layer.from_dict(data.formula)
	if data.has("connectivity"):
		connectivity_layer.from_dict(data.connectivity)
	if data.has("geometry"):
		geometry_layer.from_dict(data.geometry)
	if data.has("crystal_form"):
		crystal_form_layer.from_dict(data.crystal_form)
	if data.has("crystal_layout"):
		crystal_layout_layer.from_dict(data.crystal_layout)
	_current_layer = data.get("current_layer", 1)
	_layer_history = data.get("history", []).duplicate(true)
	hierarchy_rebuilt.emit()

func get_control_flow_description() -> String:
	return """
=== 五层递进关系 ===

第一层 化学式 → 决定元素组成与比例 (完全可控)
  ↓ 涌现: 从清单到结构
第二层 结合方式 → 决定化学身份与反应性 (高度可控)
  ↓ 涌现: 从拓扑到形状
第三层 相对位置 → 决定立体化学与精细物性 (部分可控)
  ↓ 涌现: 从分子到固体
第四层 晶型 → 决定溶解度/熔点/密度/稳定性 (间接调控)
  ↓ 涌现: 从固体到材料
第五层 晶型布局 → 决定力学/传输/加工性能 (工艺涌现)

核心规律: 越往上, 自由度越离散, 控制越精确
         越往下, 自由度越连续, 控制越依赖外部条件
"""