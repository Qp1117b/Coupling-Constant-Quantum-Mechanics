extends Node

## 元素超导电性文献数据库 (SCData)
## 数据源: data/element_superconductivity.json
## 所有数值均为文献汇编值(带来源与不确定度), 非本项目理论计算结果。
## 用于: 德拜温度文献值查询、电声耦合常数对照、实验 Tc 基准校准。

const DATA_PATH = "res://data/element_superconductivity.json"

var _data: Dictionary = {}
var _elements: Dictionary = {}
var _benchmarks: Array = []

func _ready() -> void:
	_load()

func _load() -> void:
	var file = FileAccess.open(DATA_PATH, FileAccess.READ)
	if not file:
		push_warning("超导材料文献数据不存在: " + DATA_PATH)
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed == null or not (parsed is Dictionary):
		push_warning("超导材料文献数据解析失败")
		return
	_data = parsed
	_elements = parsed.get("elements", {})
	_benchmarks = parsed.get("compound_benchmarks", [])

func reload() -> void:
	_load()

## 元素超导数据条目 (θD, λ, Tc实验值, 来源等); 无数据返回空字典
func get_entry(symbol: String) -> Dictionary:
	return _elements.get(symbol, {})

func has_entry(symbol: String) -> bool:
	return _elements.has(symbol)

## 文献德拜温度 (K); 无文献值返回 NAN
func get_debye_temperature(symbol: String) -> float:
	var e = get_entry(symbol)
	if e.is_empty():
		return NAN
	return float(e.get("theta_D_K", NAN))

func get_debye_uncertainty(symbol: String) -> float:
	var e = get_entry(symbol)
	if e.is_empty():
		return NAN
	return float(e.get("theta_D_unc", NAN))

## 文献电声耦合常数 λ; 无文献值返回 NAN
func get_lambda_epc(symbol: String) -> float:
	var e = get_entry(symbol)
	if e.is_empty():
		return NAN
	var lam = e.get("lambda_epc", null)
	if lam == null:
		return NAN
	return float(lam)

func get_lambda_uncertainty(symbol: String) -> float:
	var e = get_entry(symbol)
	if e.is_empty():
		return NAN
	return float(e.get("lambda_unc", NAN))

## 环境压实验 Tc (K); 明确非超导返回 0.0; 无数据返回 NAN
func get_experimental_tc(symbol: String) -> float:
	var e = get_entry(symbol)
	if e.is_empty():
		return NAN
	var tc = e.get("tc_ambient_K", null)
	if tc == null:
		if not bool(e.get("is_superconductor_ambient", true)):
			return 0.0
		return NAN
	return float(tc)

## 高压实验纪录列表 [{tc_K, pressure_GPa, source, status}]
func get_high_pressure_records(symbol: String) -> Array:
	var e = get_entry(symbol)
	if e.is_empty():
		return []
	return e.get("tc_hp", [])

func is_ambient_superconductor(symbol: String) -> bool:
	return bool(get_entry(symbol).get("is_superconductor_ambient", false))

## 分子平均德拜温度 (按原子数加权, 只统计有文献值的原子)
## 返回 {value, coverage, any_literature}
func average_debye_temperature(symbols: Array) -> Dictionary:
	if symbols.is_empty():
		return {"value": NAN, "coverage": 0.0, "any_literature": false}
	var sum = 0.0
	var count = 0
	for sym in symbols:
		var td = get_debye_temperature(str(sym))
		if not is_nan(td):
			sum += td
			count += 1
	if count == 0:
		return {"value": NAN, "coverage": 0.0, "any_literature": false}
	return {
		"value": sum / count,
		"coverage": float(count) / symbols.size(),
		"any_literature": true
	}

## 分子平均电声耦合常数 (几何平均更利于跨元素外推, 此处用算术平均与覆盖度)
func average_lambda_epc(symbols: Array) -> Dictionary:
	if symbols.is_empty():
		return {"value": NAN, "coverage": 0.0, "any_literature": false}
	var sum = 0.0
	var count = 0
	for sym in symbols:
		var lam = get_lambda_epc(str(sym))
		if not is_nan(lam):
			sum += lam
			count += 1
	if count == 0:
		return {"value": NAN, "coverage": 0.0, "any_literature": false}
	return {
		"value": sum / count,
		"coverage": float(count) / symbols.size(),
		"any_literature": true
	}

## 化合物基准列表 [{formula, tc_K, pressure_GPa, family, year, source}]
func get_benchmarks() -> Array:
	return _benchmarks

## 解析化学式为元素计数字典 (如 "LaH10" → {"La":1, "H":10})
static func formula_counts(formula: String) -> Dictionary:
	var counts: Dictionary = {}
	var i = 0
	var n = formula.length()
	while i < n:
		var c = formula[i]
		if c == c.to_upper() and c != c.to_lower():
			var sym = c
			i += 1
			while i < n and formula[i] != formula[i].to_upper():
				sym += formula[i]
				i += 1
			var num = ""
			while i < n and formula[i].is_valid_int():
				num += formula[i]
				i += 1
			counts[sym] = counts.get(sym, 0) + (int(num) if num != "" else 1)
		else:
			i += 1
	return counts

## 按化学式匹配实验基准 (元素多重集合比较, 忽略书写顺序); 无匹配返回空字典
func find_benchmark(formula: String) -> Dictionary:
	var target = formula_counts(formula)
	if target.is_empty():
		return {}
	for b in _benchmarks:
		if formula_counts(str(b.get("formula", ""))) == target:
			return b
	return {}

func get_data_sources() -> Array:
	return _data.get("data_sources", [])

func get_typical_mu_star() -> float:
	return float(_data.get("mu_star_typical", {}).get("value", 0.13))
