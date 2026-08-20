extends Control
class_name ChartPlotter

# 2D 图表绘制系统
# 支持: 折线图、散点图、柱状图、相图
# 用于: Tc-T曲线、DOS图、能隙曲线、压强-Tc相图、序参量雷达图

var _margin_left: float = 60.0
var _margin_right: float = 20.0
var _margin_top: float = 30.0
var _margin_bottom: float = 40.0
var _bg_color: Color = Color(0.06, 0.08, 0.12, 0.95)
var _grid_color: Color = Color(0.2, 0.25, 0.35, 0.5)
var _axis_color: Color = Color(0.5, 0.6, 0.75)
var _text_color: Color = Color(0.75, 0.82, 0.95)
var _title: String = ""
var _x_label: String = ""
var _y_label: String = ""
var _series: Array = []
var _x_range: Array = []
var _y_range: Array = []
var _auto_range: bool = true
var _show_grid: bool = true
var _show_legend: bool = true
var _font_size: int = 12

func _ready():
	custom_minimum_size = Vector2(300, 200)
	mouse_filter = Control.MOUSE_FILTER_STOP

func _draw():
	var rect = Rect2(Vector2.ZERO, size)
	draw_rect(rect, _bg_color, true)
	if _series.is_empty():
		draw_string(_get_font(), Vector2(rect.size.x / 2, rect.size.y / 2), "无数据", HORIZONTAL_ALIGNMENT_CENTER, -1, _font_size, _text_color)
		return
	var plot_rect = Rect2(
		rect.position + Vector2(_margin_left, _margin_top),
		Vector2(rect.size.x - _margin_left - _margin_right, rect.size.y - _margin_top - _margin_bottom)
	)
	var x_min = _x_range[0] if _x_range.size() >= 2 else 0.0
	var x_max = _x_range[1] if _x_range.size() >= 2 else 1.0
	var y_min = _y_range[0] if _y_range.size() >= 2 else 0.0
	var y_max = _y_range[1] if _y_range.size() >= 2 else 1.0
	if _auto_range:
		var ranges = _compute_ranges()
		x_min = ranges[0]
		x_max = ranges[1]
		y_min = ranges[2]
		y_max = ranges[3]
	if x_max <= x_min:
		x_max = x_min + 1.0
	if y_max <= y_min:
		y_max = y_min + 1.0
	if _show_grid:
		_draw_grid(plot_rect, x_min, x_max, y_min, y_max)
	_draw_axes(plot_rect, x_min, x_max, y_min, y_max)
	for s in _series:
		_draw_series(s, plot_rect, x_min, x_max, y_min, y_max)
	if not _title.is_empty():
		draw_string(_get_font(), Vector2(rect.size.x / 2, 18), _title, HORIZONTAL_ALIGNMENT_CENTER, -1, _font_size + 2, _text_color)
	if not _x_label.is_empty():
		draw_string(_get_font(), Vector2(plot_rect.position.x + plot_rect.size.x / 2, rect.size.y - 8), _x_label, HORIZONTAL_ALIGNMENT_CENTER, -1, _font_size, _text_color)
	if not _y_label.is_empty():
		var y_pos = Vector2(15, plot_rect.position.y + plot_rect.size.y / 2)
		draw_string(_get_font(), y_pos, _y_label, HORIZONTAL_ALIGNMENT_CENTER, -1, _font_size, _text_color, true)
	if _show_legend:
		_draw_legend(rect)

func _draw_grid(plot_rect: Rect2, _x_min, _x_max, _y_min, _y_max):
	var n_x = 5
	var n_y = 4
	for i in range(n_x + 1):
		var x = plot_rect.position.x + float(i) / n_x * plot_rect.size.x
		draw_line(Vector2(x, plot_rect.position.y), Vector2(x, plot_rect.position.y + plot_rect.size.y), _grid_color, 1.0)
	for i in range(n_y + 1):
		var y = plot_rect.position.y + float(i) / n_y * plot_rect.size.y
		draw_line(Vector2(plot_rect.position.x, y), Vector2(plot_rect.position.x + plot_rect.size.x, y), _grid_color, 1.0)

func _draw_axes(plot_rect: Rect2, x_min, x_max, y_min, y_max):
	draw_line(plot_rect.position, Vector2(plot_rect.position.x + plot_rect.size.x, plot_rect.position.y), _axis_color, 2.0)
	draw_line(Vector2(plot_rect.position.x, plot_rect.position.y + plot_rect.size.y), plot_rect.position + plot_rect.size, _axis_color, 2.0)
	draw_line(plot_rect.position, Vector2(plot_rect.position.x, plot_rect.position.y + plot_rect.size.y), _axis_color, 2.0)
	draw_line(Vector2(plot_rect.position.x + plot_rect.size.x, plot_rect.position.y), plot_rect.position + plot_rect.size, _axis_color, 2.0)
	var font = _get_font()
	var n_ticks = 5
	for i in range(n_ticks + 1):
		var t = float(i) / n_ticks
		var x_val = x_min + t * (x_max - x_min)
		var px = plot_rect.position.x + t * plot_rect.size.x
		draw_string(font, Vector2(px - 15, plot_rect.position.y + plot_rect.size.y + 15), _format_number(x_val), HORIZONTAL_ALIGNMENT_LEFT, -1, _font_size - 2, _text_color)
		var y_val = y_max - t * (y_max - y_min)
		var py = plot_rect.position.y + t * plot_rect.size.y
		draw_string(font, Vector2(plot_rect.position.x - 45, py + 4), _format_number(y_val), HORIZONTAL_ALIGNMENT_LEFT, -1, _font_size - 2, _text_color)

func _draw_series(s: Dictionary, plot_rect: Rect2, x_min, x_max, y_min, y_max):
	var points = s.get("points", [])
	if points.is_empty():
		return
	var color = s.get("color", Color.WHITE)
	var kind = s.get("kind", "line")
	var width = s.get("width", 2.0)
	var screen_points: Array = []
	for p in points:
		var px = plot_rect.position.x + (p.x - x_min) / (x_max - x_min) * plot_rect.size.x
		var py = plot_rect.position.y + (y_max - p.y) / (y_max - y_min) * plot_rect.size.y
		screen_points.append(Vector2(px, py))
	if kind == "line" or kind == "both":
		for i in range(screen_points.size() - 1):
			draw_line(screen_points[i], screen_points[i + 1], color, width)
	if kind == "scatter" or kind == "both":
		var r = s.get("radius", 3.0)
		for sp in screen_points:
			draw_circle(sp, r, color)

func _draw_legend(rect: Rect2):
	var font = _get_font()
	var x = rect.size.x - _margin_right - 100
	var y = _margin_top + 5
	for s in _series:
		var label_name = s.get("name", "")
		if label_name.is_empty():
			continue
		var color = s.get("color", Color.WHITE)
		draw_rect(Rect2(x, y, 12, 12), color, true)
		draw_string(font, Vector2(x + 16, y + 10), label_name, HORIZONTAL_ALIGNMENT_LEFT, -1, _font_size - 1, _text_color)
		y += 16

func _compute_ranges() -> Array:
	var x_min = INF
	var x_max = -INF
	var y_min = INF
	var y_max = -INF
	for s in _series:
		for p in s.get("points", []):
			x_min = min(x_min, p.x)
			x_max = max(x_max, p.x)
			y_min = min(y_min, p.y)
			y_max = max(y_max, p.y)
	if x_min == INF:
		return [0.0, 1.0, 0.0, 1.0]
	var x_pad = (x_max - x_min) * 0.05
	var y_pad = (y_max - y_min) * 0.05
	if y_pad < 0.001:
		y_pad = 0.1
	return [x_min - x_pad, x_max + x_pad, y_min - y_pad, y_max + y_pad]

func _format_number(v: float) -> String:
	var abs_v = abs(v)
	if abs_v >= 1000:
		return "%.0f" % v
	elif abs_v >= 10:
		return "%.1f" % v
	elif abs_v >= 0.1:
		return "%.2f" % v
	elif abs_v >= 0.001:
		return "%.3f" % v
	else:
		return PhysicsNotation.sci(v, 1)

func _get_font() -> Font:
	return ThemeDB.fallback_font

# === 公共接口 ===

func clear():
	_series.clear()
	queue_redraw()

func set_title(t: String):
	_title = t
	queue_redraw()

func set_labels(x: String, y: String):
	_x_label = x
	_y_label = y
	queue_redraw()

func set_range(x_min: float, x_max: float, y_min: float, y_max: float):
	_x_range = [x_min, x_max]
	_y_range = [y_min, y_max]
	_auto_range = false
	queue_redraw()

func set_auto_range(auto: bool):
	_auto_range = auto
	queue_redraw()

func add_line_series(points: Array, color: Color, label_name: String = "", width: float = 2.0):
	_series.append({"kind": "line", "points": points, "color": color, "name": label_name, "width": width})
	queue_redraw()

func add_scatter_series(points: Array, color: Color, label_name: String = "", radius: float = 3.0):
	_series.append({"kind": "scatter", "points": points, "color": color, "name": label_name, "radius": radius})
	queue_redraw()

func add_line_scatter_series(points: Array, color: Color, label_name: String = "", width: float = 2.0, radius: float = 3.0):
	_series.append({"kind": "both", "points": points, "color": color, "name": label_name, "width": width, "radius": radius})
	queue_redraw()

# === 预设图表 ===

func plot_tc_vs_temperature(tc: float, temp_range: Array = [0.0, 300.0], n_points: int = 100):
	clear()
	set_title("Tc - T 相变曲线")
	set_labels("温度 T (K)", "序参量 Δ(T)/Δ₀")
	var points: Array = []
	for i in range(n_points + 1):
		var T = temp_range[0] + float(i) / n_points * (temp_range[1] - temp_range[0])
		var ratio = T / tc if tc > 0 else 1.0
		var delta = 0.0
		if ratio < 1.0:
			delta = sqrt(max(0.0, 1.0 - ratio)) * (1.0 + 0.1 * ratio * ratio)
		points.append(Vector2(T, delta))
	add_line_series(points, Color(0.3, 0.9, 0.4), "Δ(T)/Δ₀", 2.5)
	var tc_line: Array = [Vector2(tc, 0), Vector2(tc, 1.1)]
	add_line_series(tc_line, Color(0.9, 0.3, 0.3), "Tc=%.1fK" % tc, 1.5)

func plot_dos(eigenvalues: Array, sigma: float = 0.1, n_points: int = 100):
	clear()
	set_title("态密度 DOS")
	set_labels("能量 λ", "ρ(λ)")
	if eigenvalues.is_empty():
		return
	var ev_min = eigenvalues.min()
	var ev_max = eigenvalues.max()
	var e_range = ev_max - ev_min
	if e_range < 0.01:
		e_range = 1.0
	var points: Array = []
	for i in range(n_points + 1):
		var e = ev_min - 0.2 * e_range + float(i) / n_points * 1.4 * e_range
		var dos = 0.0
		for ev in eigenvalues:
			dos += exp(-pow(e - float(ev), 2) / (2.0 * sigma * sigma))
		dos /= eigenvalues.size() * sqrt(2.0 * PI) * sigma
		points.append(Vector2(e, dos))
	add_line_series(points, Color(0.4, 0.7, 1.0), "DOS", 2.0)
	var ev_points: Array = []
	for ev in eigenvalues:
		ev_points.append(Vector2(float(ev), 0))
	add_scatter_series(ev_points, Color(1.0, 0.6, 0.2), "本征值", 4.0)

func plot_tc_vs_pressure(tc_func: Callable, p_range: Array = [0.0, 300.0], n_points: int = 50):
	clear()
	set_title("Tc - 压强 相图")
	set_labels("压强 P (GPa)", "Tc (K)")
	var points: Array = []
	for i in range(n_points + 1):
		var p = p_range[0] + float(i) / n_points * (p_range[1] - p_range[0])
		var tc = tc_func.call(p)
		points.append(Vector2(p, tc))
	add_line_series(points, Color(0.9, 0.5, 0.3), "Tc(P)", 2.5)

func plot_gap_vs_temperature(_tc: float, _delta_0: float, n_points: int = 80):
	clear()
	set_title("BCS 能隙 Δ(T)")
	set_labels("T/Tc", "Δ(T)/Δ₀")
	var points: Array = []
	for i in range(n_points + 1):
		var t_ratio = float(i) / n_points
		var delta_ratio = 0.0
		if t_ratio < 1.0:
			delta_ratio = sqrt(max(0.0, 1.0 - t_ratio)) * (1.0 + 0.2 * t_ratio * t_ratio)
		points.append(Vector2(t_ratio, delta_ratio))
	add_line_series(points, Color(0.3, 0.9, 0.4), "Δ(T)/Δ₀", 2.5)

func plot_order_parameters(order_params: Array):
	clear()
	set_title("A4 序参量 (4通道)")
	set_labels("通道", "|Δk|")
	var points: Array = []
	for i in range(order_params.size()):
		var amp = abs(float(order_params[i].get("amplitude", 0)))
		points.append(Vector2(float(i + 1), amp))
	add_line_scatter_series(points, Color(0.8, 0.6, 1.0), "|Δk|", 2.0, 5.0)

func plot_critical_fields(hc1: float, hc2: float, n_points: int = 80):
	clear()
	set_title("临界磁场 Hc(T)")
	set_labels("T/Tc", "Hc (T)")
	var points_hc2: Array = []
	var points_hc1: Array = []
	for i in range(n_points + 1):
		var t = float(i) / n_points
		var factor = 1.0 - t * t
		points_hc2.append(Vector2(t, hc2 * factor))
		points_hc1.append(Vector2(t, hc1 * factor))
	add_line_series(points_hc2, Color(0.9, 0.3, 0.3), "Hc2", 2.5)
	add_line_series(points_hc1, Color(0.3, 0.5, 0.9), "Hc1", 2.5)