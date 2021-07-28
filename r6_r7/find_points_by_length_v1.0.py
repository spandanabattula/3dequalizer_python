#
#
# 3DE4.script.name: Find points by track length...
#
# 3DE4.script.version:		v1.0
#
# 3DE4.script.gui:		Manual Tracking Controls::Edit
# 3DE4.script.gui:		Lineup Controls::Edit
#
# 3DE4.script.comment:Finds 2d points by their track length.
#
# Patcha Saheb(patchasaheb@gmail.com)
# 30 January 2018.


def _mainCallback(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(cam)
	pl = tde4.getPointList(pg,0)
	v = int(tde4.getWidgetValue(req,"length"))


	#deselect all points...
	for point in pl:
		tde4.setPointSelectionFlag(pg,point,0)

	for point in pl:
		track_length_list = []
		count = 0
		for frame in range(1,frames+1):
			track_status = tde4.getPointStatus2D(pg,point,cam,frame)
			if track_status != "POINT_UNDEFINED" and track_status != "POINT_INTERPOLATED":
				track_length_list.append(count)
				count = count + 1
		if len(track_length_list) <= v:
			if widget == "select":
				tde4.setPointSelectionFlag(pg,point,1)
			if widget == "delete":
				tde4.deletePoint(pg,point)

























window_title = "Find points by track length v1.0"

req = tde4.createCustomRequester()

#add textfield widget...
tde4.addTextFieldWidget(req,"length","Track Length")
tde4.setWidgetAttachModes(req,"length","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"length",25,95,20,0)

#add select tracks button widget...
tde4.addButtonWidget(req,"select","Select Tracks",70)
tde4.setWidgetAttachModes(req,"select","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"select",5,45,60,0)

#add delete tracks button widget...
tde4.addButtonWidget(req,"delete","Delete Tracks",70)
tde4.setWidgetAttachModes(req,"delete","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"delete",55,95,60,0)









#callbacks...
tde4.setWidgetCallbackFunction(req,"select","_mainCallback")
tde4.setWidgetCallbackFunction(req,"delete","_mainCallback")



tde4.postCustomRequesterAndContinue(req,window_title,400,100)
