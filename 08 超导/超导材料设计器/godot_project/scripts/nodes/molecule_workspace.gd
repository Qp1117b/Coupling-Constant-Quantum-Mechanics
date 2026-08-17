extends Node3D
class_name MoleculeWorkspace

enum Mode { PLACE, SELECT, BOND, DELETE }

@export var current_mode: Mode = Mode.PLACE

var atoms: Array[Atom3D] = []
var bonds: Array[Bond3D] = []
var selected_atom: Atom3D = null
var pending_bond_from: Atom3D = null

var _atom_scene: PackedScene

func _ready():
    _atom_scene = preload("res://scenes/Atom.tscn")

func add_atom(symbol: String, isotope: int, pos: Vector3) -> Atom3D:
    var atom = _atom_scene.instantiate() as Atom3D
    atom.element_symbol = symbol
    atom.isotope_mass = isotope
    atom.position = pos
    $Atoms.add_child(atom)
    atoms.append(atom)
    atom.atom_clicked.connect(_on_atom_clicked)
    Events.emit_signal("atom_added", atom)
    Events.emit_signal("molecule_changed")
    return atom

func add_bond(a: Atom3D, b: Atom3D, order: int = 1) -> Bond3D:
    for existing in bonds:
        if (existing.atom_a == a and existing.atom_b == b) or \
           (existing.atom_a == b and existing.atom_b == a):
            return existing

    if not ChemValidator.can_add_bond(a, bonds):
        Events.emit_signal("bond_rejected", a, "配位数已满")
        return null
    if not ChemValidator.can_add_bond(b, bonds):
        Events.emit_signal("bond_rejected", b, "配位数已满")
        return null

    var bond = Bond3D.new()
    bond.atom_a = a
    bond.atom_b = b
    bond.bond_order = order
    $Bonds.add_child(bond)
    bonds.append(bond)
    Events.emit_signal("bond_added", bond)
    Events.emit_signal("molecule_changed")
    return bond

func remove_atom(atom: Atom3D):
    var to_remove = []
    for bond in bonds:
        if bond.atom_a == atom or bond.atom_b == atom:
            to_remove.append(bond)
    for bond in to_remove:
        remove_bond(bond)
    atoms.erase(atom)
    if selected_atom == atom:
        selected_atom = null
    if pending_bond_from == atom:
        pending_bond_from = null
    atom.queue_free()
    Events.emit_signal("atom_removed", atom)
    Events.emit_signal("molecule_changed")

func remove_bond(bond: Bond3D):
    bonds.erase(bond)
    bond.queue_free()
    Events.emit_signal("bond_removed", bond)
    Events.emit_signal("molecule_changed")

func clear():
    for bond in bonds:
        bond.queue_free()
    bonds.clear()
    for atom in atoms:
        atom.queue_free()
    atoms.clear()
    selected_atom = null
    pending_bond_from = null
    Events.emit_signal("molecule_cleared")
    Events.emit_signal("molecule_changed")

func select_atom(atom: Atom3D):
    selected_atom = atom
    Events.emit_signal("atom_selected", atom)

func _on_atom_clicked(atom: Atom3D):
    if selected_atom and selected_atom != atom:
        selected_atom.set_selected(false)
    selected_atom = atom
    atom.set_selected(true)
    Events.emit_signal("atom_selected", atom)

func get_atom_data() -> Array:
    var result = []
    for atom in atoms:
        result.append({
            "symbol": atom.element_symbol,
            "isotope": atom.isotope_mass,
            "position": atom.position
        })
    return result

func get_bond_data() -> Array:
    var result = []
    for bond in bonds:
        result.append({
            "a": atoms.find(bond.atom_a),
            "b": atoms.find(bond.atom_b),
            "order": bond.bond_order
        })
    return result

func set_mode(mode: Mode):
    current_mode = mode
    pending_bond_from = null
    Events.emit_signal("mode_changed", mode)
