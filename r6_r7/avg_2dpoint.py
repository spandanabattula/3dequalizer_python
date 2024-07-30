# 3DE4.script.name:	Avg 2Dpoint
# 3DE4.script.version:	v1.0
# 3DE4.script.gui.button: Manual Tracking Controls::Avg_2Dpoint, align-bottom-left, 80, 20
# 3DE4.script.comment:creates a new 2dpoint at average position of selected two 2dpoints.
# Patcha Saheb(patchasaheb@gmail.com)
#August 06 2015.

# Spandana Test 1


window_title = "Avg 2DPoint v1.0"
pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frames = tde4.getCameraNoFrames(cam)
pl = tde4.getPointList(pg,1)
frames_list = []
if len(pl) == 2:
	point_a = pl[0]
	point_b = pl[1]
	point_avg = tde4.createPoint(pg)
	tde4.setPointName(pg,point_avg,"Avg_2dPoint_01")
	tde4.setPointTrackingDirection(pg,point_a,"TRACKING_FW")
	tde4.setPointTrackingDirection(pg,point_b,"TRACKING_FW")
	for frame in range(1,frames+1):
		point_a_status = tde4.getPointStatus2D(pg,point_a,cam,frame)
		point_b_status = tde4.getPointStatus2D(pg,point_b,cam,frame)
		if not point_a_status == "POINT_UNDEFINED" or point_a_status == "POINT_KEYFRAME_END":
			if point_b_status == "POINT_UNDEFINED" or point_b_status == "POINT_KEYFRAME_END":
				pass
			else:
				frames_list.append(frame)
		if not point_b_status == "POINT_UNDEFINED" or point_b_status == "POINT_KEYFRAME_END":
			if point_a_status == "POINT_UNDEFINED" or point_a_status == "POINT_KEYFRAME_END":
				pass
			else:
				frames_list.append(frame)
		if point_a_status == "POINT_KEYFRAME_END" and point_b_status == "POINT_KEYFRAME_END":
			frames_list.append(frame)
	frames_list = list(set(frames_list))
	frames_list.sort()
	count = 0
	for frame in frames_list:
		count = count + 1
		#points 2d position...
		point_a_2d = tde4.getPointPosition2D(pg,point_a,cam,frame)
		point_b_2d = tde4.getPointPosition2D(pg,point_b,cam,frame)
		#get average position...
		avg_x = (point_a_2d[0] + point_b_2d[0]) / 2
		avg_y = (point_a_2d[1] + point_b_2d[1]) / 2
		tde4.setPointPosition2D(pg,point_avg,cam,frame,[avg_x,avg_y])
		if count == len(frames_list):
			tde4.setPointStatus2D(pg,point_avg,cam,frame,"POINT_KEYFRAME_END")
		else:
			tde4.setPointStatus2D(pg,point_avg,cam,frame,"POINT_KEYFRAME")
else:
	tde4.postQuestionRequester(window_title,"Error, exactly two 2dpoints must be selected.","ok")


