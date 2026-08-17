extends Node

signal element_selected(symbol: String)
signal isotope_selected(symbol: String, mass_number: int)

signal atom_added(atom)
signal atom_removed(atom)
signal atom_selected(atom)
signal bond_added(bond)
signal bond_removed(bond)
signal bond_rejected(atom, reason: String)
signal molecule_changed()
signal molecule_cleared()

signal calculation_started()
signal calculation_complete(results: Dictionary)
signal calculation_error(message: String)

signal mode_changed(mode: int)

signal project_saved(path: String)
signal project_loaded(path: String)