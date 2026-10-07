extends Node

## 超导材料模式引擎：双轨工作流 + 会话状态栈
## 管理L0-L4五层模式的挂载、适用性检查、跨层联动与延迟校验
## 物理硬约束与软提示直接内置（不依赖外部JSON）

signal formula_changed(formula: String)
signal pattern_mounted(layer: int, pattern_id: String)
signal pattern_unmounted(layer: int)
signal work_mode_changed(mode: int)


enum WorkMode { PATTERN, FREE }
enum Layer { L0, L1, L2, L3, L4 }

const BOND_ANGLE_MIN := 0.0
const BOND_ANGLE_MAX := 180.0
const BOND_LENGTH_DEVIATION_THRESHOLD := 20.0
const SPACE_GROUP_MIN := 1
const SPACE_GROUP_MAX := 230
const MIN_DIST_FACTOR := 0.5
const RING_TENSION_WARN := 80.0
const UNUSUAL_COORDINATION_DELTA := 2
const LOW_DENSITY_THRESHOLD := 1.0
const EXTREME_PRESSURE := 200.0

var _work_mode: int = WorkMode.PATTERN
var _pattern_library: Dictionary = {}
var _session: Dictionary = {}
var _pending_checks: Array = []

func _ready() -> void:
	_load_pattern_library()
	_init_session()

func _load_pattern_library() -> void:
	var lib_path := "res://data/pattern_library.json"
	if FileAccess.file_exists(lib_path):
		var f := FileAccess.open(lib_path, FileAccess.READ)
		var text := f.get_as_text()
		f.close()
		var parsed = JSON.parse_string(text)
		if parsed is Dictionary:
			_pattern_library = parsed

func _init_session() -> void:
	_session = {
		"L0": {"formula": "", "locked": false, "elements": []},
		"L1": {"pattern_id": "", "output": {}, "locked": false, "dangling": true},
		"L2": {"pattern_id": "", "output": {}, "locked": false, "dangling": true},
		"L3": {"pattern_id": "", "output": {}, "locked": false, "dangling": true},
		"L4": {"grain_distribution": "single_crystal", "params": {}, "locked": false},
		"import_links": {}
	}

func set_work_mode(mode: int) -> void:
	_work_mode = mode
	work_mode_changed.emit(mode)

func get_work_mode() -> int:
	return _work_mode

func get_work_mode_name() -> String:
	return ["模式设计", "自由设计"][_work_mode]

func set_formula(formula_str: String) -> void:
	var elements := _parse_elements(formula_str)
	_session["L0"]["formula"] = formula_str
	_session["L0"]["elements"] = elements
	_session["L0"]["locked"] = true
	formula_changed.emit(formula_str)
	_refresh_applicability()

func get_formula() -> String:
	return _session["L0"]["formula"]

func get_elements() -> Array:
	return _session["L0"]["elements"]

func _parse_elements(formula_str: String) -> Array:
	var elements: Array = []
	var regex := RegEx.new()
	regex.compile("[A-Z][a-z]?")
	var results := regex.search_all(formula_str)
	for r in results:
		var elem := r.get_string()
		if not (elem in elements):
			elements.append(elem)
	return elements

func _refresh_applicability() -> void:
	for layer_key in ["L1", "L2", "L3"]:
		var current_id: String = _session[layer_key]["pattern_id"]
		if current_id != "":
			if not is_pattern_applicable(current_id):
				unmount_pattern(_layer_key_to_int(layer_key))

func get_all_patterns() -> Array:
	return _pattern_library.get("patterns", [])

func get_pattern(pattern_id: String) -> Dictionary:
	for p in get_all_patterns():
		if p.get("pattern_id", "") == pattern_id:
			return p
	return {}

func get_patterns_by_family(family: String) -> Array:
	var result: Array = []
	for p in get_all_patterns():
		if p.get("pattern_family", "") == family:
			result.append(p)
	return result

func get_families() -> Array:
	var families: Array = []
	for p in get_all_patterns():
		var f: String = p.get("pattern_family", "")
		if not (f in families):
			families.append(f)
	return families

func is_pattern_applicable(pattern_id: String) -> bool:
	var p := get_pattern(pattern_id)
	if p.is_empty():
		return false
	var cond: Dictionary = p.get("applicable_when", {})
	var elements: Array = _session["L0"]["elements"]
	if elements.is_empty():
		return true
	var must_contain: Array = cond.get("must_contain", [])
	for elem in must_contain:
		if not (elem in elements):
			return false
	var any_of: Array = cond.get("any_of", [])
	if any_of.size() > 0:
		var found := false
		for elem in any_of:
			if elem in elements:
				found = true
				break
		if not found:
			return false
	return true

func get_applicable_patterns() -> Array:
	var result: Array = []
	for p in get_all_patterns():
		if is_pattern_applicable(p.get("pattern_id", "")):
			result.append(p)
	return result

func mount_pattern(layer: int, pattern_id: String) -> bool:
	if not is_pattern_applicable(pattern_id):
		return false
	var layer_key := _layer_int_to_key(layer)
	if layer_key == "":
		return false
	_session[layer_key]["pattern_id"] = pattern_id
	_session[layer_key]["dangling"] = false
	_session[layer_key]["output"] = _extract_layer_output(layer, pattern_id)
	pattern_mounted.emit(layer, pattern_id)
	_apply_cross_layer_rules(layer, pattern_id)
	return true

func _extract_layer_output(layer: int, pattern_id: String) -> Dictionary:
	var p := get_pattern(pattern_id)
	if p.is_empty():
		return {}
	var layers: Dictionary = p.get("layers", {})
	var layer_key := _layer_int_to_key(layer)
	if not layers.has(layer_key):
		return {}
	var layer_data: Dictionary = layers[layer_key]
	var output: Dictionary = {"pattern_id": pattern_id}
	match layer:
		Layer.L1:
			output["conserved_substructures"] = layer_data.get("conserved_substructures", [])
			output["variable_modules"] = layer_data.get("variable_modules", [])
			output["forbidden_topologies"] = layer_data.get("forbidden_topologies", [])
			output["skeleton_rule"] = layer_data.get("skeleton_rule", "")
		Layer.L2:
			output["key_parameters"] = layer_data.get("key_parameters", {})
			output["conformation_notes"] = layer_data.get("conformation_notes", "")
		Layer.L3:
			output["space_group_map"] = layer_data.get("space_group_map", {})
			output["packing_constraints"] = layer_data.get("packing_constraints", {})
	return output

func get_layer_output_summary(layer: int) -> String:
	var layer_key := _layer_int_to_key(layer)
	if layer_key == "":
		return ""
	var pid: String = _session[layer_key].get("pattern_id", "")
	if pid == "":
		return "未挂载"
	var output: Dictionary = _session[layer_key].get("output", {})
	if output.is_empty():
		return "已挂载 %s (无参数提取)" % pid
	var lines: Array = ["%s:" % pid]
	match layer:
		Layer.L1:
			var cs: Array = output.get("conserved_substructures", [])
			if not cs.is_empty():
				lines.append("  保守子结构: %s" % ", ".join(cs))
			var vm: Array = output.get("variable_modules", [])
			if not vm.is_empty():
				lines.append("  可变模块: %s" % ", ".join(vm))
			var sr: String = output.get("skeleton_rule", "")
			if sr != "":
				lines.append("  骨架规则: %s" % sr)
		Layer.L2:
			var kp: Dictionary = output.get("key_parameters", {})
			for param_name in kp:
				var pd: Dictionary = kp[param_name]
				var formula: String = pd.get("formula", "?")
				var unit: String = pd.get("unit", "")
				lines.append("  %s = %s %s" % [param_name, formula, unit])
			var cn: String = output.get("conformation_notes", "")
			if cn != "":
				lines.append("  备注: %s" % cn)
		Layer.L3:
			var sgm: Dictionary = output.get("space_group_map", {})
			for case_key in sgm:
				lines.append("  %s → %s" % [case_key, sgm[case_key]])
			var pc: Dictionary = output.get("packing_constraints", {})
			var bl: String = pc.get("bravais_lattice", "")
			if bl != "":
				lines.append("  Bravais: %s" % bl)
			var zf: String = pc.get("z_formula", "")
			if zf != "":
				lines.append("  Z公式: %s" % zf)
	return "\n".join(lines)

func unmount_pattern(layer: int) -> void:
	var layer_key := _layer_int_to_key(layer)
	if layer_key == "":
		return
	_session[layer_key]["pattern_id"] = ""
	_session[layer_key]["dangling"] = true
	_session[layer_key]["output"] = {}
	pattern_unmounted.emit(layer)

func get_mounted_pattern(layer: int) -> String:
	var layer_key := _layer_int_to_key(layer)
	if layer_key == "":
		return ""
	return _session[layer_key].get("pattern_id", "")

func is_layer_dangling(layer: int) -> bool:
	var layer_key := _layer_int_to_key(layer)
	if layer_key == "":
		return true
	return _session[layer_key].get("dangling", true)

func _apply_cross_layer_rules(layer: int, pattern_id: String) -> void:
	var p := get_pattern(pattern_id)
	if p.is_empty():
		return
	var rules: Array = p.get("cross_layer_rules", [])
	for rule in rules:
		_pending_checks.append({"layer": layer, "rule": rule})

func get_pending_cross_layer_effects() -> Array:
	return _pending_checks.duplicate()

func clear_pending_checks() -> void:
	_pending_checks.clear()

func get_layer_output(layer: int) -> Dictionary:
	var layer_key := _layer_int_to_key(layer)
	if layer_key == "":
		return {}
	return _session[layer_key].get("output", {})

func set_layer_output(layer: int, output: Dictionary) -> void:
	var layer_key := _layer_int_to_key(layer)
	if layer_key == "":
		return
	_session[layer_key]["output"] = output
	_session[layer_key]["dangling"] = false

func set_grain_distribution(grain_type: String, params: Dictionary = {}) -> void:
	_session["L4"]["grain_distribution"] = grain_type
	_session["L4"]["params"] = params

func get_grain_distribution() -> String:
	return _session["L4"].get("grain_distribution", "single_crystal")

func get_session_state() -> Dictionary:
	return _session.duplicate(true)

func get_session_summary() -> String:
	var lines: Array = []
	lines.append("=== 会话状态 ===")
	lines.append("工作模式: %s" % get_work_mode_name())
	lines.append("L0 化学式: %s (元素: %s)" % [_session["L0"]["formula"], str(_session["L0"]["elements"])])
	for layer_key in ["L1", "L2", "L3"]:
		var pid: String = _session[layer_key]["pattern_id"]
		var dangling: bool = _session[layer_key]["dangling"]
		var status := "悬空" if dangling else "已挂载"
		if pid == "":
			lines.append("%s: 未挂载 (%s)" % [layer_key, status])
		else:
			var p := get_pattern(pid)
			var family: String = p.get("pattern_family", "?")
			lines.append("%s: %s [%s] (%s)" % [layer_key, pid, family, status])
			var layer_int := _layer_key_to_int(layer_key)
			var summary := get_layer_output_summary(layer_int)
			if summary != "" and summary != "未挂载":
				for sl in summary.split("\n"):
					lines.append("  " + sl)
	lines.append("L4 晶胞分布: %s" % _session["L4"].get("grain_distribution", "single_crystal"))
	if _pending_checks.size() > 0:
		lines.append("待校验跨层规则: %d 条" % _pending_checks.size())
	return "\n".join(lines)

func _layer_int_to_key(layer: int) -> String:
	match layer:
		Layer.L1: return "L1"
		Layer.L2: return "L2"
		Layer.L3: return "L3"
		Layer.L4: return "L4"
		_: return ""

func _layer_key_to_int(key: String) -> int:
	match key:
		"L1": return Layer.L1
		"L2": return Layer.L2
		"L3": return Layer.L3
		"L4": return Layer.L4
		_: return -1

func check_hard_constraint(layer: int, params: Dictionary) -> Array:
	var violations: Array = []
	match layer:
		Layer.L0:
			if params.has("charge_sum") and float(params["charge_sum"]) != 0.0:
				violations.append({"constraint": "charge_neutrality", "value": params["charge_sum"]})
		Layer.L1:
			if params.has("bond_order"):
				var bo: float = float(params["bond_order"])
				if not (bo == 1.0 or bo == 2.0 or bo == 3.0 or bo == 1.5 or bo == 0.5):
					violations.append({"constraint": "bond_order_validity", "value": bo})
		Layer.L2:
			if params.has("angle"):
				var angle: float = float(params["angle"])
				if angle <= BOND_ANGLE_MIN or angle >= BOND_ANGLE_MAX:
					violations.append({"constraint": "bond_angle_range", "value": angle})
			if params.has("distance") and params.has("min_distance"):
				var dist: float = float(params["distance"])
				var min_d: float = float(params["min_distance"])
				if dist <= min_d:
					violations.append({"constraint": "min_atomic_distance", "value": dist})
			if params.has("volume"):
				var vol: float = float(params["volume"])
				if vol <= 0.0:
					violations.append({"constraint": "cell_volume_positive", "value": vol})
		Layer.L3:
			if params.has("space_group"):
				var sg: int = int(params["space_group"])
				if sg < SPACE_GROUP_MIN or sg > SPACE_GROUP_MAX:
					violations.append({"constraint": "space_group_valid", "value": sg})
			if params.has("z") and int(params["z"]) <= 0:
				violations.append({"constraint": "z_positive_integer", "value": params["z"]})
	return violations

func check_soft_hints(layer: int, params: Dictionary) -> Array:
	var hints: Array = []
	match layer:
		Layer.L1:
			if params.has("coordination_deviation"):
				var dev: float = float(params["coordination_deviation"])
				if absf(dev) > UNUSUAL_COORDINATION_DELTA:
					hints.append({"hint": "unusual_coordination", "severity": "info", "message": "配位数偏离常见值%.1f" % dev})
		Layer.L2:
			if params.has("deviation_pct"):
				var dev: float = float(params["deviation_pct"])
				if absf(dev) > BOND_LENGTH_DEVIATION_THRESHOLD:
					hints.append({"hint": "bond_length_deviation", "severity": "warning", "message": "键长偏离经验均值%.1f%%" % dev})
		Layer.L3:
			if params.has("mismatch") and bool(params["mismatch"]):
				hints.append({"hint": "symmetry_mismatch", "severity": "warning", "message": "空间群与分子对称性不匹配"})
			if params.has("density") and float(params["density"]) < LOW_DENSITY_THRESHOLD:
				hints.append({"hint": "low_density", "severity": "info", "message": "计算密度<1.0 g/cm³"})
	return hints

func reset_session() -> void:
	_init_session()
	_pending_checks.clear()
