extends Control
class_name IsotopeSelector

var _current_symbol: String = ""
var _isotope_container: HBoxContainer
var _detail_labels: Dictionary = {}

func _ready():
    _build_ui()
    Events.connect("element_selected", _on_element_changed)

func _build_ui():
    var vbox = VBoxContainer.new()
    vbox.size = size
    add_child(vbox)

    var title = Label.new()
    title.text = "同位素选择"
    title.add_theme_font_size_override("font_size", 14)
    vbox.add_child(title)

    _isotope_container = HBoxContainer.new()
    vbox.add_child(_isotope_container)

    var detail = VBoxContainer.new()
    vbox.add_child(detail)
    for key in ["selected", "neutrons", "defect", "spin", "abundance"]:
        var lbl = Label.new()
        lbl.name = key
        lbl.add_theme_font_size_override("font_size", 11)
        detail.add_child(lbl)
        _detail_labels[key] = lbl

func _on_element_changed(symbol: String):
    _current_symbol = symbol
    _refresh()

func _refresh():
    for child in _isotope_container.get_children():
        child.queue_free()

    var element = ElementDB.get_element(_current_symbol)
    if element.is_empty():
        return

    var isotopes = element.get("isotopes", [])
    isotopes.sort_custom(func(a, b): return int(a.mass_number) < int(b.mass_number))

    for iso in isotopes:
        var btn = Button.new()
        btn.text = str(iso.mass_number)
        btn.custom_minimum_size = Vector2(40, 32)
        btn.add_theme_font_size_override("font_size", 11)

        if bool(iso.get("is_stable", false)):
            btn.modulate = Color(0.85, 1.0, 0.85)
        else:
            btn.modulate = Color(1.0, 0.8, 0.8)

        btn.tooltip_text = _isotope_tooltip(iso)
        btn.pressed.connect(_select_isotope.bind(iso))
        _isotope_container.add_child(btn)

    var default_iso = _find_most_abundant(isotopes)
    if not default_iso.is_empty():
        _select_isotope(default_iso)

func _isotope_tooltip(iso: Dictionary) -> String:
    var stability = "稳定" if iso.get("is_stable", false) else "不稳定"
    return "A=%d, N=%d, %s" % [int(iso.mass_number), int(iso.neutrons), stability]

func _select_isotope(iso: Dictionary):
    var z = int(iso.mass_number) - int(iso.neutrons)
    var defect = CQMCartanBuilder.neutron_defect(int(iso.neutrons), _current_symbol)

    _detail_labels.selected.text = "选中: %d%s" % [int(iso.mass_number), _current_symbol]
    _detail_labels.neutrons.text = "中子数: %d" % int(iso.neutrons)
    _detail_labels.defect.text = "中子缺陷 ε: %.6f" % defect
    _detail_labels.spin.text = "核自旋: %s" % str(iso.get("spin", "—"))
    _detail_labels.abundance.text = "丰度: %.4f%%" % (float(iso.get("abundance", 0)) * 100)

    Events.emit_signal("isotope_selected", _current_symbol, int(iso.mass_number))

func _find_most_abundant(isotopes: Array) -> Dictionary:
    var best = {}
    var max_ab = -1.0
    for iso in isotopes:
        var ab = float(iso.get("abundance", 0))
        if ab > max_ab:
            max_ab = ab
            best = iso
    return best