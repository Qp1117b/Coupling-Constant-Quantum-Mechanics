extends Node

const CONFIG_PATH = "res://data/cqm_theory_config.json"

var data: Dictionary = {}
var fixed: Dictionary = {}
var models: Dictionary = {}
var overrides: Dictionary = {}

func _ready():
    _load()

func _load():
    var file = FileAccess.open(CONFIG_PATH, FileAccess.READ)
    if not file:
        push_warning("CQM配置不存在，使用默认值: " + CONFIG_PATH)
        _init_defaults()
        return
    data = JSON.parse_string(file.get_as_text())
    fixed = data.get("fixed_constants", {})
    models = data.get("model_choices", {})
    overrides = data.get("element_overrides", {})

func _init_defaults():
    fixed = {
        "A4_matrix": [[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]],
        "A4_eigenvalues": [0.381966, 1.381966, 2.618034, 3.618034],
        "spectral_gap": 0.38196601125,
        "spectral_quantum_C": 0.02309570897,
        "bcs_prefactor": 1.1339,
        "universal_gap_ratio": 3.5278
    }
    models = {
        "defect_mode": {"type": "diagonal", "pattern": [1,0,0,0]},
        "neutron_defect_function": {"type": "linear", "default_eps_0": 0.0012, "default_beta": 0.1},
        "proton_sector_model": {"type": "pure_A4"},
        "cross_element_coupling": {"type": "scalar_identity"},
        "tc_estimation": {"method": "bcs_cqm_corrected"}
    }
    overrides = {"H": {"force_neutron_defect": 0.0}}

func get_A4() -> PackedFloat32Array:
    var m = fixed.get("A4_matrix", [[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]])
    var mat = PackedFloat32Array()
    for row in m:
        for v in row:
            mat.append(float(v))
    return mat

func get_eigenvalues() -> PackedFloat32Array:
    var vals = fixed.get("A4_eigenvalues", [0.382, 1.382, 2.618, 3.618])
    var mat = PackedFloat32Array()
    for v in vals:
        mat.append(float(v))
    return mat

func get_spectral_gap() -> float:
    return float(fixed.get("spectral_gap", 0.381966))

func get_bcs_prefactor() -> float:
    return float(fixed.get("bcs_prefactor", 1.1339))

func get_spectral_quantum_c() -> float:
    return float(fixed.get("spectral_quantum_C", 0.02309570897))

func get_universal_gap_ratio() -> float:
    return float(fixed.get("universal_gap_ratio", 3.5278))

func get_defect_pattern() -> Array:
    return models.get("defect_mode", {}).get("pattern", [1,0,0,0])

func get_eps_0() -> float:
    return float(models.get("neutron_defect_function", {}).get("default_eps_0", 0.0012))

func get_beta() -> float:
    return float(models.get("neutron_defect_function", {}).get("default_beta", 0.1))

func get_defect_function_type() -> String:
    return models.get("neutron_defect_function", {}).get("type", "linear")

func get_proton_model_type() -> String:
    return models.get("proton_sector_model", {}).get("type", "pure_A4")

func get_element_override(symbol: String) -> Dictionary:
    return overrides.get(symbol, {})

func reload():
    _load()