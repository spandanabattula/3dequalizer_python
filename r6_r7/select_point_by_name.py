# 3DE4.script.name:	Select point by name...
# 3DE4.script.version:	v1.0
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.comment:	Selects point by name.
# Author : Patcha Saheb (patchasaheb@gmail.com)
# 15 March 2016.

window_title = "Patcha Select point by name_v1.0"

def Select(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pl = tde4.getPointList(pg,0)
	v = tde4.getWidgetValue(req,"point_name")
	if v != " " and v!= None:
		v = v.replace(" ","")
	else:
		tde4.postQuestionRequester(window_title,"Error, please enter point name.","Ok")	
	for point in pl:
		tde4.setPointSelectionFlag(pg,point,0)
		name = tde4.getPointName(pg,point)
		if name == v:
			tde4.setPointSelectionFlag(pg,point,1)

req = tde4.createCustomRequester()
tde4.addTextFieldWidget(req,"point_name","Point Name"," ")
tde4.setWidgetAttachModes(req,"point_name","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_AS_IS","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"point_name",100,20,25,10)
tde4.addButtonWidget(req,"select_button","Select",70,10)
tde4.setWidgetAttachModes(req,"select_button","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_AS_IS")
tde4.setWidgetLinks(req,"select_button","","","point_name","")
tde4.setWidgetOffsets(req,"select_button",240,20,30,10)
tde4.setWidgetCallbackFunction(req,"select_button","Select")
tde4.postCustomRequesterAndContinue(req,window_title,350,60)





