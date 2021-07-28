#
# 3DE4.script.name:	Print Zoom Curve min, max values
# 3DE4.script.version:	v1.0
#
# 3DE4.script.gui:	Curve Editor::Edit
#
# 3DE4.script.comment:	Prints Zoom Curve min,max values.
#
# Patcha Saheb(patchasaheb@gmail.com)
# 16 Feb 2018(Montreal)

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
frames = tde4.getCameraNoFrames(cam)

if tde4.getCameraZoomingFlag(cam) == 1:
	zoom_curve = tde4.getCameraZoomCurve(cam)
	kl = tde4.getCurveKeyList(zoom_curve,0)
	key_value_list = []
	for frame in range(1,frames+1):
		pos2d_y = tde4.evaluateCurve(zoom_curve,frame)
		key_value_list.append(pos2d_y)

	zoom_value_min = min(key_value_list) * 10.0
	zoom_value_max = max(key_value_list) * 10.0

	print "Zoom Curve minimum value is " + str(zoom_value_min)
	print "Zoom Curve maximum value is " + str(zoom_value_max)

else:
	print "Camera Dynamic(Zooming) is not turned on."





