extends Control
class_name ElementPalette

const PERIODS = 7
const GROUPS = 18

var _selected_symbol: String = "H"
var _buttons: Dictionary = {}
var _position_map: Dictionary = {}
var _placed_in_main: Dictionary = {}

func _ready():
	_build_position_map()
	_build_layout()
	Events.connect("element_selected", _on_element_selected)

func _on_element_selected(symbol: String):
	_selected_symbol = symbol
	for sym in _buttons.keys():
		_buttons[sym].set_pressed_no_signal(sym == symbol)

func _build_position_map():
	for symbol in ElementDB.get_all_symbols():
		var data = ElementDB.get_element(symbol)
		if data.is_empty():
			continue
		var key = "%d,%d" % [int(data.get("period", 0)), int(data.get("group", 0))]
		if not _position_map.has(key):
			_position_map[key] = data

func _build_layout():
	var scroll = ScrollContainer.new()
	scroll.size = size
	add_child(scroll)

	var grid = GridContainer.new()
	grid.columns = GROUPS
	scroll.add_child(grid)

	for period in range(1, PERIODS + 1):
		for group in range(1, GROUPS + 1):
			var element = _position_map.get("%d,%d" % [period, group], {})
			if element.is_empty():
				var spacer = Control.new()
				spacer.custom_minimum_size = Vector2(36, 36)
				grid.add_child(spacer)
			else:
				_placed_in_main[element.symbol] = true
				grid.add_child(_create_element_button(element))

	_build_f_block(grid)

func _build_f_block(grid: GridContainer):
	for _i in range(GROUPS * 2):
		var spacer = Control.new()
		spacer.custom_minimum_size = Vector2(36, 10)
		grid.add_child(spacer)

	grid.add_child(_create_f_block_row(range(58, 72), "镧系 Ce(58)–Lu(71)，La 在主表格第3族"))
	for _i in range(3):
		grid.add_child(_create_spacer())
	grid.add_child(_create_f_block_row(range(90, 104), "锕系 Th(90)–Lr(103)，Ac 在主表格第3族"))

func _create_f_block_row(z_range: Array, title: String) -> Control:
	var box = HBoxContainer.new()
	for z in z_range:
		var data = ElementDB.get_element_by_number(z)
		if data.is_empty() or _placed_in_main.has(data.symbol):
			continue
		box.add_child(_create_element_button(data))
	box.tooltip_text = title
	return box

func _create_element_button(data: Dictionary) -> Button:
	var btn = Button.new()
	btn.text = data.symbol
	btn.custom_minimum_size = Vector2(36, 36)
	btn.tooltip_text = "%s (Z=%d, %s)" % [
		data.get("name_en", data.symbol), int(data.get("atomic_number", 0)),
		data.get("category", "")]
	btn.modulate = Color.from_string(data.get("color", "#FFFFFF"), Color.WHITE)
	btn.add_theme_font_size_override("font_size", 10)
	btn.toggle_mode = true
	btn.pressed.connect(_select_element.bind(data.symbol))
	_buttons[data.symbol] = btn
	return btn

func _create_spacer() -> Control:
	var spacer = Control.new()
	spacer.custom_minimum_size = Vector2(36, 36)
	return spacer

func _select_element(symbol: String):
	_selected_symbol = symbol
	for sym in _buttons.keys():
		_buttons[sym].set_pressed_no_signal(sym == symbol)
	Events.emit_signal("element_selected", symbol)

func get_selected() -> String:
	return _selected_symbol
