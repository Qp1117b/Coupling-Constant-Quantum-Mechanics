extends Node

const INDEX_PATH = "res://data/elements/_index.json"
const ELEMENT_PATH = "res://data/elements/%s.json"

var _index: Dictionary = {}
var _cache: Dictionary = {}
var _by_number: Dictionary = {}

signal database_ready()
signal element_loaded(symbol: String)

func _ready():
	_load_index()
	database_ready.emit()

func _load_index():
	var file = FileAccess.open(INDEX_PATH, FileAccess.READ)
	if not file:
		push_warning("元素索引不存在: " + INDEX_PATH)
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed == null or not (parsed is Dictionary):
		push_warning("元素索引解析失败: " + INDEX_PATH)
		return
	_index = parsed
	_by_number.clear()
	for symbol in _index.get("elements", {}).keys():
		var z = int(_index["elements"][symbol].get("Z", 0))
		if z > 0:
			_by_number[z] = symbol

func _load_element(symbol: String) -> Dictionary:
	if _cache.has(symbol):
		return _cache[symbol]
	var path = ELEMENT_PATH % symbol
	var file = FileAccess.open(path, FileAccess.READ)
	if not file:
		return {}
	var data = JSON.parse_string(file.get_as_text())
	if data == null or not (data is Dictionary):
		return {}
	_cache[symbol] = data
	element_loaded.emit(symbol)
	return data

func get_element(symbol: String) -> Dictionary:
	return _load_element(symbol)

func get_element_by_number(z: int) -> Dictionary:
	if _by_number.is_empty():
		_load_index()
	var symbol = str(_by_number.get(z, ""))
	if symbol.is_empty():
		return {}
	return get_element(symbol)

func get_isotopes(symbol: String) -> Array:
	return get_element(symbol).get("isotopes", [])

func get_stable_isotopes(symbol: String) -> Array:
	return get_isotopes(symbol).filter(func(iso): return iso.get("is_stable", false))

func get_isotope(symbol: String, mass_number: int) -> Dictionary:
	for iso in get_isotopes(symbol):
		if int(iso.get("mass_number", 0)) == mass_number:
			return iso
	return {}

func most_abundant_isotope(symbol: String) -> int:
	var stable = get_stable_isotopes(symbol)
	var pool = stable if not stable.is_empty() else get_isotopes(symbol)
	if pool.is_empty():
		var z = int(_index.get("elements", {}).get(symbol, {}).get("Z", 0))
		return z + 1
	var best = pool[0]
	for iso in pool:
		if float(iso.get("abundance", 0.0)) > float(best.get("abundance", 0.0)):
			best = iso
	return int(best.get("mass_number", 1))

func get_all_symbols() -> Array:
	return _index.get("elements", {}).keys()

func get_index_data() -> Dictionary:
	return _index

func get_category_elements(category: String) -> Array:
	return _index.get("categories", {}).get(category, [])

func has_element(symbol: String) -> bool:
	return _index.get("elements", {}).has(symbol)
