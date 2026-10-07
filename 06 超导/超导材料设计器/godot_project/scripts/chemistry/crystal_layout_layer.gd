extends RefCounted
class_name CrystalLayoutLayer

## L4 第五层：晶胞分布 (Grain Distribution / Microstructure)
## 晶胞确定后，晶胞在空间中的分布排列（晶粒结构）
## 包括单晶/多晶/薄膜/线材/粉末，及加工条件
## 可控性：用户自由定义 — 系统仅提供参考建议，不封装经验模式
## L4晶胞分布是Regge单元剖分的对象，角亏场直接给出FG退相干场强度

signal microstructure_changed()

var _grain_size_nm: float = 1000.0  # nm, 1000nm = 1μm = polycrystalline
var _grain_orientation: Dictionary = {}  # Euler angles or fiber texture
var _texture_type: String = "random"  # random, fiber, cube, sheet
var _porosity: float = 0.0  # 0-1
var _defect_density: float = 0.0  # per cm²
var _residual_stress: float = 0.0  # MPa
var _grain_distribution: String = "single_crystal"  # single_crystal, polycrystal, film, wire, powder
var _film_thickness_nm: float = 0.0  # nm, for thin films
var _grain_boundary_type: String = "random"  # random, low_angle, special (CSL)

func get_layer_name() -> String:
	return "晶胞分布"

func get_layer_index() -> int:
	return 5

func get_controllability() -> String:
	return "用户自由定义 (系统仅提供参考建议)"

func get_description() -> String:
	return "晶胞分布（晶粒结构）。决定Regge剖分、FG退相干场、力学/传输/加工性能。晶胞是砖块，晶胞分布是墙怎么砌。包括单晶/多晶/薄膜/线材/粉末等。"

func set_grain_size(size_nm: float) -> void:
	_grain_size_nm = maxf(size_nm, 0.1)
	microstructure_changed.emit()

func get_grain_size() -> float:
	return _grain_size_nm

func set_texture(texture_type: String, orientation: Dictionary = {}) -> void:
	_texture_type = texture_type
	_grain_orientation = orientation.duplicate()
	microstructure_changed.emit()

func get_texture_type() -> String:
	return _texture_type

func get_grain_orientation() -> Dictionary:
	return _grain_orientation.duplicate()

func set_porosity(p: float) -> void:
	_porosity = clampf(p, 0.0, 1.0)
	microstructure_changed.emit()

func get_porosity() -> float:
	return _porosity

func set_defect_density(d: float) -> void:
	_defect_density = maxf(d, 0.0)
	microstructure_changed.emit()

func get_defect_density() -> float:
	return _defect_density

func set_residual_stress(stress: float) -> void:
	_residual_stress = stress
	microstructure_changed.emit()

func get_residual_stress() -> float:
	return _residual_stress

func set_grain_distribution(morph: String) -> void:
	_grain_distribution = morph
	microstructure_changed.emit()

func get_grain_distribution() -> String:
	return _grain_distribution

func set_film_thickness(thickness_nm: float) -> void:
	_film_thickness_nm = maxf(thickness_nm, 0.0)
	microstructure_changed.emit()

func get_film_thickness() -> float:
	return _film_thickness_nm

func set_grain_boundary_type(gb_type: String) -> void:
	_grain_boundary_type = gb_type
	microstructure_changed.emit()

func get_grain_boundary_type() -> String:
	return _grain_boundary_type

func is_single_crystal() -> bool:
	return _grain_size_nm >= 1e6 or _grain_distribution == "single_crystal"

func is_nanocrystalline() -> bool:
	return _grain_size_nm < 100.0

func is_polycrystalline() -> bool:
	return not is_single_crystal() and not is_nanocrystalline()

func compute_effective_resistivity(bulk_resistivity: float) -> float:
	if is_single_crystal():
		return bulk_resistivity
	var scattering_factor = 1.0 + _defect_density * 1e-11
	var porosity_factor = 1.0 / maxf(1.0 - _porosity, 0.01) ** 1.5
	var grain_factor = 1.0
	if is_nanocrystalline():
		grain_factor = 1.0 + 10.0 / _grain_size_nm
	return bulk_resistivity * scattering_factor * porosity_factor * grain_factor

func compute_effective_thermal_conductivity(bulk_k: float) -> float:
	if is_single_crystal():
		return bulk_k
	var k = bulk_k
	k *= maxf(1.0 - _porosity, 0.01) ** 1.5
	if is_nanocrystalline():
		k *= _grain_size_nm / (_grain_size_nm + 10.0)
	k *= 1.0 / (1.0 + _defect_density * 1e-12)
	return k

func compute_hall_petch(yield_strength_0: float, k_hp: float = 0.5) -> float:
	if is_single_crystal():
		return yield_strength_0
	var d_m = _grain_size_nm * 1e-9  # nm to m
	return yield_strength_0 + k_hp / sqrt(d_m)

func get_microstructure_summary() -> Dictionary:
	return {
		"grain_size_nm": _grain_size_nm,
		"texture": _texture_type,
		"porosity": _porosity,
		"defect_density": _defect_density,
		"residual_stress": _residual_stress,
		"grain_distribution": _grain_distribution,
		"is_single_crystal": is_single_crystal(),
		"is_nanocrystalline": is_nanocrystalline(),
		"is_polycrystalline": is_polycrystalline(),
	}

func to_dict() -> Dictionary:
	return {
		"layer": "crystal_layout",
		"grain_size_nm": _grain_size_nm,
		"texture_type": _texture_type,
		"grain_orientation": _grain_orientation.duplicate(),
		"porosity": _porosity,
		"defect_density": _defect_density,
		"residual_stress": _residual_stress,
		"grain_distribution": _grain_distribution,
		"film_thickness_nm": _film_thickness_nm,
		"grain_boundary_type": _grain_boundary_type,
	}

func from_dict(data: Dictionary) -> void:
	_grain_size_nm = data.get("grain_size_nm", 1000.0)
	_texture_type = data.get("texture_type", "random")
	_grain_orientation = data.get("grain_orientation", {}).duplicate()
	_porosity = data.get("porosity", 0.0)
	_defect_density = data.get("defect_density", 0.0)
	_residual_stress = data.get("residual_stress", 0.0)
	_grain_distribution = data.get("grain_distribution", "bulk")
	_film_thickness_nm = data.get("film_thickness_nm", 0.0)
	_grain_boundary_type = data.get("grain_boundary_type", "random")
	microstructure_changed.emit()