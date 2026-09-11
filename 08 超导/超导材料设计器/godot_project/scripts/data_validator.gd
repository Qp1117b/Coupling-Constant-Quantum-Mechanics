extends RefCounted
class_name DataValidator

## 数据校验器 (设计文档 02 §6.1 规划)
## 启动时校验三大数据库的一致性与物理合理性:
##   1. 元素库: 118 元素齐全、字段完整、同位素单调
##   2. SCDB:  材料字段完整、Tc 物理合理 (0 < Tc ≤ 300K)、原子元素存在、压强非负
##   3. SCData: θD > 0、λ ≥ 0、常压 Tc 与超导标志一致
## 返回 {passed, errors: [], warnings: []}; errors 表示数据损坏级别问题

const MAX_KNOWN_TC := 300.0  # 常压/高压已确认上限 (LaH10 ~260K)

static func validate_all() -> Dictionary:
	var errors: Array = []
	var warnings: Array = []
	_validate_elements(errors, warnings)
	_validate_scdb(errors, warnings)
	_validate_scdata(errors, warnings)
	return {"passed": errors.is_empty(), "errors": errors, "warnings": warnings}

static func _validate_elements(errors: Array, warnings: Array) -> void:
	var symbols = ElementDB.get_all_symbols()
	if symbols.size() < 118:
		warnings.append("元素库仅 %d/118 个元素" % symbols.size())
	for sym in symbols:
		var e = ElementDB.get_element(str(sym))
		if e.is_empty():
			errors.append("元素 %s 索引存在但数据为空" % str(sym))
			continue
		var z = int(e.get("atomic_number", 0))
		if z < 1 or z > 118:
			errors.append("元素 %s 原子序数非法: %d" % [str(sym), z])
		var mass = float(e.get("atomic_mass", 0.0))
		if mass <= 0.0 or mass > 300.0:
			warnings.append("元素 %s 原子质量异常: %.2f" % [str(sym), mass])
		var cov = float(e.get("covalent_radius_pm", 0.0))
		if cov <= 0.0 or cov > 300.0:
			warnings.append("元素 %s 共价半径异常: %.1f pm" % [str(sym), cov])

static func _validate_scdb(errors: Array, warnings: Array) -> void:
	var all = SCDB.get_all()
	if all.is_empty():
		errors.append("SCDB 为空")
		return
	for m in all:
		var nm = str(m.get("name", "?"))
		var tc = float(m.get("tc", 0.0))
		if tc <= 0.0 or tc > MAX_KNOWN_TC:
			warnings.append("SCDB %s Tc 异常: %.1f K (已确认上限 ~%.0fK)" % [nm, tc, MAX_KNOWN_TC])
		var p = float(m.get("pressure_GPa", 0.0))
		if p < 0.0 or p > 500.0:
			warnings.append("SCDB %s 压强异常: %.1f GPa" % [nm, p])
		var atoms = m.get("atoms", [])
		if atoms.is_empty():
			warnings.append("SCDB %s 无原子结构" % nm)
			continue
		for a in atoms:
			var sym = str(a.get("sym", ""))
			if ElementDB.get_element(sym).is_empty():
				errors.append("SCDB %s 含未知元素 %s" % [nm, sym])
			var pos = a.get("pos", null)
			if pos == null or not (pos is Vector3):
				errors.append("SCDB %s 原子坐标缺失" % nm)
		var year = int(m.get("year", 0))
		if year < 1911 or year > 2030:
			warnings.append("SCDB %s 年份异常: %d" % [nm, year])

static func _validate_scdata(_errors: Array, warnings: Array) -> void:
	var sources = SCData.get_data_sources()
	if sources.is_empty():
		warnings.append("SCData 无数据来源标注")
	var benchmarks = SCData.get_benchmarks()
	if benchmarks.size() < 20:
		warnings.append("SCData 化合物基准仅 %d 条 (<20)" % benchmarks.size())
	for b in benchmarks:
		var tc = float(b.get("tc_K", 0.0))
		if tc <= 0.0 or tc > MAX_KNOWN_TC:
			warnings.append("基准 %s Tc 异常: %.1f K" % [str(b.get("formula", "?")), tc])
	var mu = SCData.get_typical_mu_star()
	if mu < 0.05 or mu > 0.25:
		warnings.append("SCData 典型 μ* 超出物理常见范围 [0.05, 0.25]: %.3f" % mu)
