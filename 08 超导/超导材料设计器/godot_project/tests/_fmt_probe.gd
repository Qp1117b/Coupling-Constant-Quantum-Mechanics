extends SceneTree

func _initialize():
	print("A: " + ("%.2e K" % 12345678.0))
	print("B: " + ("%.*f K" % [2, 9.25]))
	print("C: " + ("%.3e Pa" % 0.000000123))
	quit(0)
