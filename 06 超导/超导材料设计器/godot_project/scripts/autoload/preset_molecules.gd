extends Node

const DEG2RAD := 0.017453292519943295

var _molecules: Dictionary = {}

func _ready() -> void:
	_build_library()

func _build_library() -> void:
	_molecules.clear()
	_molecules["H2"] = _mol("H2", "氢气", "H₂", [
		{"sym": "H", "pos": Vector3(-0.371, 0, 0)},
		{"sym": "H", "pos": Vector3(0.371, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 1 }])

	_molecules["N2"] = _mol("N2", "氮气", "N₂", [
		{"sym": "N", "pos": Vector3(-0.549, 0, 0)},
		{"sym": "N", "pos": Vector3(0.549, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 3 }])

	_molecules["O2"] = _mol("O2", "氧气", "O₂", [
		{"sym": "O", "pos": Vector3(-0.604, 0, 0)},
		{"sym": "O", "pos": Vector3(0.604, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 2 }])

	_molecules["CO"] = _mol("CO", "一氧化碳", "CO", [
		{"sym": "C", "pos": Vector3(-0.564, 0, 0)},
		{"sym": "O", "pos": Vector3(0.564, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 3 }])

	_molecules["HCl"] = _mol("HCl", "氯化氢", "HCl", [
		{"sym": "H", "pos": Vector3(-0.638, 0, 0)},
		{"sym": "Cl", "pos": Vector3(0.638, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 1 }])

	_molecules["HF"] = _mol("HF", "氟化氢", "HF", [
		{"sym": "H", "pos": Vector3(-0.459, 0, 0)},
		{"sym": "F", "pos": Vector3(0.459, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 1 }])

	_molecules["H2O"] = _mol("H2O", "水", "H₂O", [
		{"sym": "O", "pos": Vector3(0, 0, 0)},
		{"sym": "H", "pos": Vector3(0.757, 0, -0.239)},
		{"sym": "H", "pos": Vector3(-0.757, 0, -0.239)},
	], [{ "a": 0, "b": 1, "order": 1 }, { "a": 0, "b": 2, "order": 1 }])

	_molecules["H2S"] = _mol("H2S", "硫化氢", "H₂S", [
		{"sym": "S", "pos": Vector3(0, 0, 0)},
		{"sym": "H", "pos": Vector3(0.961, 0, -0.928)},
		{"sym": "H", "pos": Vector3(-0.961, 0, -0.928)},
	], [{ "a": 0, "b": 1, "order": 1 }, { "a": 0, "b": 2, "order": 1 }])

	_molecules["CO2"] = _mol("CO2", "二氧化碳", "CO₂", [
		{"sym": "C", "pos": Vector3(0, 0, 0)},
		{"sym": "O", "pos": Vector3(1.163, 0, 0)},
		{"sym": "O", "pos": Vector3(-1.163, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 2 }, { "a": 0, "b": 2, "order": 2 }])

	_molecules["SO2"] = _mol("SO2", "二氧化硫", "SO₂", [
		{"sym": "S", "pos": Vector3(0, 0, 0)},
		{"sym": "O", "pos": Vector3(1.237, 0, -0.721)},
		{"sym": "O", "pos": Vector3(-1.237, 0, -0.721)},
	], [{ "a": 0, "b": 1, "order": 2 }, { "a": 0, "b": 2, "order": 2 }])

	_molecules["HCN"] = _mol("HCN", "氰化氢", "HCN", [
		{"sym": "H", "pos": Vector3(1.065, 0, 0)},
		{"sym": "C", "pos": Vector3(0, 0, 0)},
		{"sym": "N", "pos": Vector3(-1.153, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 1 }, { "a": 1, "b": 2, "order": 3 }])

	_molecules["C2H2"] = _mol("C2H2", "乙炔", "C₂H₂", [
		{"sym": "H", "pos": Vector3(1.662, 0, 0)},
		{"sym": "C", "pos": Vector3(0.602, 0, 0)},
		{"sym": "C", "pos": Vector3(-0.602, 0, 0)},
		{"sym": "H", "pos": Vector3(-1.662, 0, 0)},
	], [{ "a": 0, "b": 1, "order": 1 }, { "a": 1, "b": 2, "order": 3 }, { "a": 2, "b": 3, "order": 1 }])

	_molecules["NH3"] = _mol("NH3", "氨", "NH₃", [
		{"sym": "N", "pos": Vector3(0, 0.374, 0)},
		{"sym": "H", "pos": Vector3(0.940, 0, 0)},
		{"sym": "H", "pos": Vector3(-0.470, 0, 0.814)},
		{"sym": "H", "pos": Vector3(-0.470, 0, -0.814)},
	], [{ "a": 0, "b": 1, "order": 1 }, { "a": 0, "b": 2, "order": 1 }, { "a": 0, "b": 3, "order": 1 }])

	_molecules["NH4"] = _mol("NH4", "铵离子", "NH₄⁺", [
		{"sym": "N", "pos": Vector3(0, 0, 0)},
		{"sym": "H", "pos": Vector3(0.595, 0.595, 0.595)},
		{"sym": "H", "pos": Vector3(0.595, -0.595, -0.595)},
		{"sym": "H", "pos": Vector3(-0.595, 0.595, -0.595)},
		{"sym": "H", "pos": Vector3(-0.595, -0.595, 0.595)},
	], [
		{ "a": 0, "b": 1, "order": 1 }, { "a": 0, "b": 2, "order": 1 },
		{ "a": 0, "b": 3, "order": 1 }, { "a": 0, "b": 4, "order": 1 },
	])

	_molecules["CH4"] = _mol("CH4", "甲烷", "CH₄", [
		{"sym": "C", "pos": Vector3(0, 0, 0)},
		{"sym": "H", "pos": Vector3(0.627, 0.627, 0.627)},
		{"sym": "H", "pos": Vector3(0.627, -0.627, -0.627)},
		{"sym": "H", "pos": Vector3(-0.627, 0.627, -0.627)},
		{"sym": "H", "pos": Vector3(-0.627, -0.627, 0.627)},
	], [
		{ "a": 0, "b": 1, "order": 1 }, { "a": 0, "b": 2, "order": 1 },
		{ "a": 0, "b": 3, "order": 1 }, { "a": 0, "b": 4, "order": 1 },
	])

	_molecules["BF3"] = _mol("BF3", "三氟化硼", "BF₃", [
		{"sym": "B", "pos": Vector3(0, 0, 0)},
		{"sym": "F", "pos": Vector3(0, 1.313, 0)},
		{"sym": "F", "pos": Vector3(-1.137, -0.657, 0)},
		{"sym": "F", "pos": Vector3(1.137, -0.657, 0)},
	], [{ "a": 0, "b": 1, "order": 1 }, { "a": 0, "b": 2, "order": 1 }, { "a": 0, "b": 3, "order": 1 }])

	_molecules["C2H4"] = _mol("C2H4", "乙烯", "C₂H₄", [
		{"sym": "C", "pos": Vector3(0.670, 0, 0)},
		{"sym": "C", "pos": Vector3(-0.670, 0, 0)},
		{"sym": "H", "pos": Vector3(1.234, 0.929, 0)},
		{"sym": "H", "pos": Vector3(1.234, -0.929, 0)},
		{"sym": "H", "pos": Vector3(-1.234, 0.929, 0)},
		{"sym": "H", "pos": Vector3(-1.234, -0.929, 0)},
	], [
		{ "a": 0, "b": 1, "order": 2 },
		{ "a": 0, "b": 2, "order": 1 }, { "a": 0, "b": 3, "order": 1 },
		{ "a": 1, "b": 4, "order": 1 }, { "a": 1, "b": 5, "order": 1 },
	])

	_molecules["C2H6"] = _mol("C2H6", "乙烷", "C₂H₆", [
		{"sym": "C", "pos": Vector3(0.768, 0, 0)},
		{"sym": "C", "pos": Vector3(-0.768, 0, 0)},
		{"sym": "H", "pos": Vector3(1.133, 1.030, 0)},
		{"sym": "H", "pos": Vector3(1.133, -0.515, 0.892)},
		{"sym": "H", "pos": Vector3(1.133, -0.515, -0.892)},
		{"sym": "H", "pos": Vector3(-1.133, 0.515, 0.892)},
		{"sym": "H", "pos": Vector3(-1.133, -1.030, 0)},
		{"sym": "H", "pos": Vector3(-1.133, 0.515, -0.892)},
	], [
		{ "a": 0, "b": 1, "order": 1 },
		{ "a": 0, "b": 2, "order": 1 }, { "a": 0, "b": 3, "order": 1 }, { "a": 0, "b": 4, "order": 1 },
		{ "a": 1, "b": 5, "order": 1 }, { "a": 1, "b": 6, "order": 1 }, { "a": 1, "b": 7, "order": 1 },
	])

	_molecules["C6H6"] = _mol_benzene()

	_molecules["SF6"] = _mol("SF6", "六氟化硫", "SF₆", [
		{"sym": "S", "pos": Vector3(0, 0, 0)},
		{"sym": "F", "pos": Vector3(1.561, 0, 0)},
		{"sym": "F", "pos": Vector3(-1.561, 0, 0)},
		{"sym": "F", "pos": Vector3(0, 1.561, 0)},
		{"sym": "F", "pos": Vector3(0, -1.561, 0)},
		{"sym": "F", "pos": Vector3(0, 0, 1.561)},
		{"sym": "F", "pos": Vector3(0, 0, -1.561)},
	], [
		{ "a": 0, "b": 1, "order": 1 }, { "a": 0, "b": 2, "order": 1 },
		{ "a": 0, "b": 3, "order": 1 }, { "a": 0, "b": 4, "order": 1 },
		{ "a": 0, "b": 5, "order": 1 }, { "a": 0, "b": 6, "order": 1 },
	])

	_molecules["CH3OH"] = _mol_methanol()

func _mol(key: String, cn_name: String, formula: String, atoms: Array, bonds: Array) -> Dictionary:
	return {
		"key": key,
		"name": cn_name,
		"formula": formula,
		"atoms": atoms,
		"bonds": bonds,
	}

func _mol_benzene() -> Dictionary:
	var cc := 1.397
	var ch := 1.084
	var r := cc
	var rh := cc + ch
	var atoms: Array = []
	var bonds: Array = []
	for i in range(6):
		var ang := i * 60.0 * DEG2RAD
		atoms.append({"sym": "C", "pos": Vector3(r * cos(ang), r * sin(ang), 0)})
	for i in range(6):
		var ang := i * 60.0 * DEG2RAD
		atoms.append({"sym": "H", "pos": Vector3(rh * cos(ang), rh * sin(ang), 0)})
	for i in range(6):
		bonds.append({"a": i, "b": (i + 1) % 6, "order": 2 if i % 2 == 0 else 1})
	for i in range(6):
		bonds.append({"a": i, "b": i + 6, "order": 1})
	return _mol("C6H6", "苯", "C₆H₆", atoms, bonds)

func _mol_methanol() -> Dictionary:
	var atoms := [
		{"sym": "C", "pos": Vector3(0, 0, 0)},
		{"sym": "O", "pos": Vector3(1.421, 0, 0)},
		{"sym": "H", "pos": Vector3(1.116, 0.911, 0)},
		{"sym": "H", "pos": Vector3(-0.365, 1.030, 0)},
		{"sym": "H", "pos": Vector3(-0.365, -0.515, 0.892)},
		{"sym": "H", "pos": Vector3(-0.365, -0.515, -0.892)},
	]
	var bonds := [
		{ "a": 0, "b": 1, "order": 1 },
		{ "a": 1, "b": 2, "order": 1 },
		{ "a": 0, "b": 3, "order": 1 }, { "a": 0, "b": 4, "order": 1 }, { "a": 0, "b": 5, "order": 1 },
	]
	return _mol("CH3OH", "甲醇", "CH₃OH", atoms, bonds)

func get_all() -> Array:
	var list: Array = []
	for key in _molecules:
		list.append(_molecules[key])
	return list

func get_keys_sorted() -> Array:
	var keys := _molecules.keys()
	keys.sort()
	return keys

func get_molecule(key: String) -> Dictionary:
	return _molecules.get(key, {})

func get_display_name(key: String) -> String:
	var m: Dictionary = _molecules.get(key, {})
	if m.is_empty():
		return key
	return "%s (%s)" % [m.formula, m.name]

func get_formula(key: String) -> String:
	var m: Dictionary = _molecules.get(key, {})
	return m.get("formula", key)

func get_atoms(key: String) -> Array:
	var m: Dictionary = _molecules.get(key, {})
	return m.get("atoms", [])

func get_bonds(key: String) -> Array:
	var m: Dictionary = _molecules.get(key, {})
	return m.get("bonds", [])

func has_molecule(key: String) -> bool:
	return _molecules.has(key)

func count() -> int:
	return _molecules.size()
