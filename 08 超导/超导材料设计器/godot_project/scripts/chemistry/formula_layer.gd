extends RefCounted
class_name FormulaLayer

## 第一层：化学式 (Chemical Formula)
## 原子种类与数目的最粗粒度表达
## 可控性：完全可控 — 化学式是人为设定的起点

signal composition_changed(composition: Dictionary)

var _composition: Dictionary = {}  # element_symbol -> count

func get_layer_name() -> String:
	return "化学式"

func get_layer_index() -> int:
	return 1

func get_controllability() -> String:
	return "完全可控"

func get_description() -> String:
	return "原子种类与数目的最粗粒度表达。决定元素组成、分子量、粗略物性区间。"

func set_composition(composition: Dictionary) -> void:
	_composition = composition.duplicate()
	composition_changed.emit(_composition)

func get_composition() -> Dictionary:
	return _composition.duplicate()

func parse_formula(formula_str: String) -> Dictionary:
	var result: Dictionary = {}
	var i = 0
	while i < formula_str.length():
		var ch = formula_str[i]
		if ch == " " or ch == "·":
			i += 1
			continue
		if not ch.is_valid_identifier():
			i += 1
			continue
		var symbol = ch
		i += 1
		if i < formula_str.length() and formula_str[i].to_lower() == formula_str[i] and formula_str[i].is_valid_identifier():
			symbol += formula_str[i]
			i += 1
		var count_str = ""
		while i < formula_str.length() and formula_str[i].is_valid_int():
			count_str += formula_str[i]
			i += 1
		var count = int(count_str) if count_str != "" else 1
		result[symbol] = result.get(symbol, 0) + count
	set_composition(result)
	return result

func format_formula(composition: Dictionary = {}) -> String:
	var comp = composition if not composition.is_empty() else _composition
	var keys = comp.keys()
	keys.sort()
	var parts: Array = []
	for sym in keys:
		var n = comp[sym]
		parts.append(sym + (str(n) if n > 1 else ""))
	return "".join(parts)

func compute_molecular_weight(composition: Dictionary = {}) -> float:
	var comp = composition if not composition.is_empty() else _composition
	var total = 0.0
	for sym in comp:
		var data = ElementDB.get_element(sym)
		var mass = float(data.get("atomic_mass", 1.0)) if not data.is_empty() else 1.0
		total += mass * comp[sym]
	return total

func get_element_count(symbol: String) -> int:
	return _composition.get(symbol, 0)

func get_total_atom_count() -> int:
	var total = 0
	for sym in _composition:
		total += _composition[sym]
	return total

func get_elements() -> Array:
	return _composition.keys()

func is_same_composition(other: FormulaLayer) -> bool:
	var other_comp = other.get_composition()
	if _composition.size() != other_comp.size():
		return false
	for sym in _composition:
		if other_comp.get(sym, 0) != _composition[sym]:
			return false
	return true

func to_dict() -> Dictionary:
	return {
		"layer": "formula",
		"composition": _composition.duplicate(),
		"formula_str": format_formula(),
		"molecular_weight": compute_molecular_weight(),
	}

func from_dict(data: Dictionary) -> void:
	_composition = data.get("composition", {}).duplicate()