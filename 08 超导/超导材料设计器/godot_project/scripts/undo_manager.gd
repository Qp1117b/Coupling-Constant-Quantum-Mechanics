extends RefCounted
class_name UndoManager

# 撤销/重做管理器（快照模式）
# 捕获原子+键的状态快照，支持撤销/重做

const MAX_HISTORY: int = 50

var _undo_stack: Array = []
var _redo_stack: Array = []
var _is_applying: bool = false

signal state_changed(can_undo: bool, can_redo: bool)

func take_snapshot(workspace: Node, brush_strokes: Array = []) -> Dictionary:
	var atoms: Array = []
	for atom in workspace.atoms:
		if is_instance_valid(atom):
			atoms.append({
				"symbol": atom.element_symbol,
				"isotope": atom.isotope_mass,
				"pos": [atom.global_position.x, atom.global_position.y, atom.global_position.z],
				"scale": [atom.scale.x, atom.scale.y, atom.scale.z]
			})
	var bonds: Array = []
	for bond in workspace.bonds:
		if is_instance_valid(bond) and is_instance_valid(bond.atom_a) and is_instance_valid(bond.atom_b):
			var a_idx = workspace.atoms.find(bond.atom_a)
			var b_idx = workspace.atoms.find(bond.atom_b)
			if a_idx >= 0 and b_idx >= 0:
				bonds.append({"a": a_idx, "b": b_idx, "order": bond.bond_order})
	var strokes: Array = []
	for s in brush_strokes:
		var pts: Array = []
		for p in s.get("points", []):
			if p is Vector3:
				pts.append([p.x, p.y, p.z])
		strokes.append({
			"shape": s.get("shape", 0),
			"is_boundary": s.get("is_boundary", false),
			"element": s.get("element", "H"),
			"points": pts
		})
	return {"atoms": atoms, "bonds": bonds, "brush_strokes": strokes}

func push_snapshot(snapshot: Dictionary):
	if _is_applying:
		return
	_undo_stack.append(snapshot)
	if _undo_stack.size() > MAX_HISTORY:
		_undo_stack.pop_front()
	_redo_stack.clear()
	state_changed.emit(can_undo(), can_redo())

func undo(workspace: Node, _brush_strokes: Array) -> Dictionary:
	if _undo_stack.size() < 2:
		return {}
	var current = _undo_stack.pop_back()
	_redo_stack.append(current)
	var previous = _undo_stack.back()
	_is_applying = true
	_apply_snapshot(workspace, previous)
	_is_applying = false
	state_changed.emit(can_undo(), can_redo())
	return _restore_strokes(previous)

func redo(workspace: Node, _brush_strokes: Array) -> Dictionary:
	if _redo_stack.is_empty():
		return {}
	var snapshot = _redo_stack.pop_back()
	_undo_stack.append(snapshot)
	_is_applying = true
	_apply_snapshot(workspace, snapshot)
	_is_applying = false
	state_changed.emit(can_undo(), can_redo())
	return _restore_strokes(snapshot)

func _apply_snapshot(workspace: Node, snapshot: Dictionary):
	workspace.clear()
	for atom_data in snapshot.get("atoms", []):
		var pos = atom_data.get("pos", [0, 0, 0])
		var atom = workspace.add_atom(
			atom_data.get("symbol", "H"),
			int(atom_data.get("isotope", 1)),
			Vector3(pos[0], pos[1], pos[2])
		)
		if atom and atom_data.has("scale"):
			var s = atom_data["scale"]
			atom.scale = Vector3(s[0], s[1], s[2])
	for bond_data in snapshot.get("bonds", []):
		var a_idx = int(bond_data.get("a", 0))
		var b_idx = int(bond_data.get("b", 0))
		if a_idx < workspace.atoms.size() and b_idx < workspace.atoms.size():
			workspace.add_bond(
				workspace.atoms[a_idx],
				workspace.atoms[b_idx],
				int(bond_data.get("order", 1))
			)

func _restore_strokes(snapshot: Dictionary) -> Dictionary:
	var strokes: Array = []
	for s in snapshot.get("brush_strokes", []):
		var pts: Array = []
		for p in s.get("points", []):
			pts.append(Vector3(p[0], p[1], p[2]))
		strokes.append({
			"shape": int(s.get("shape", 0)),
			"is_boundary": s.get("is_boundary", false),
			"element": s.get("element", "H"),
			"points": pts
		})
	return {"brush_strokes": strokes}

func can_undo() -> bool:
	return _undo_stack.size() >= 2

func can_redo() -> bool:
	return not _redo_stack.is_empty()

func clear():
	_undo_stack.clear()
	_redo_stack.clear()
	state_changed.emit(false, false)