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

func _suppress_unused_signal_warnings() -> void:
	element_selected.emit("")
	isotope_selected.emit("", 0)
	atom_added.emit(null)
	atom_removed.emit(null)
	atom_selected.emit(null)
	bond_added.emit(null)
	bond_removed.emit(null)
	bond_rejected.emit(null, "")
	molecule_changed.emit()
	molecule_cleared.emit()
	calculation_started.emit()
	calculation_complete.emit({})
	calculation_error.emit("")
	mode_changed.emit(0)
	project_saved.emit("")
	project_loaded.emit("")