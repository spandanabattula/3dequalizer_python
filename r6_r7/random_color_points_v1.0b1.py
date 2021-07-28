# 3DE4.script.name:	Random Color Points...
# 3DE4.script.version:	v1.0b1
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui:	Manual Tracking Controls::Edit
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.comment:Sets random color to 2D/3D Points.
# Patcha Saheb(patchasaheb@gmail.com)

from vl_sdv import *
import random

def Random_Color(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	allpoints = tde4.getWidgetValue(req,"all_points")
	selectedpoints = tde4.getWidgetValue(req,"selected_points")
	if allpoints == 1:
		pl = tde4.getPointList(pg,0)
	if selectedpoints == 1:
		pl = tde4.getPointList(pg,1)
	if len(pl) > 0:
		n = [0,1,2,3,4,5,7,8,9,10,11]
		if widget == "2dpoints_color":
			for point in pl:
				random.shuffle(n)
				tde4.setPointColor2D(pg,point,n[0])
		if widget == "3dpoints_color":
			for point in pl:
				random.shuffle(n)
				tde4.setPointColor3D(pg,point,n[0])
		if widget == "2dpoints_uniform_color":
				random.shuffle(n)
				for point in pl:
					tde4.setPointColor2D(pg,point,n[0])
		if widget == "3dpoints_uniform_color":
				random.shuffle(n)
				for point in pl:
					tde4.setPointColor3D(pg,point,n[0])
	else:
		tde4.postQuestionRequester(window_title, "Error, there are no points or selected points.", "OK")

def Sensitivity(req,widget,action):
	allpoints = tde4.getWidgetValue(req,"all_points")
	selectedpoints = tde4.getWidgetValue(req,"selected_points")
	if widget == "all_points":
		if allpoints == 1:
			tde4.setWidgetValue(req,"all_points","1")
			tde4.setWidgetValue(req,"selected_points","0")
		else:
			tde4.setWidgetValue(req,"all_points","0")
			tde4.setWidgetValue(req,"selected_points","1")					
	if widget == "selected_points":
		if selectedpoints == 1:
			tde4.setWidgetValue(req,"all_points","0")
			tde4.setWidgetValue(req,"selected_points","1")
		else:
			tde4.setWidgetValue(req,"all_points","1")
			tde4.setWidgetValue(req,"selected_points","0")

window_title = "Patcha Random Color Points v1.0b1"
req = tde4.createCustomRequester()
#add 2dpoints random color button...
tde4.addButtonWidget(req,"2dpoints_color","Random color for individual 2D Points",70,10)
tde4.setWidgetAttachModes(req,"2dpoints_color","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_AS_IS","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"2dpoints_color",40,40,10,10)
#add 3dpoints random color button...
tde4.addButtonWidget(req,"3dpoints_color","Random color for individual 3D Points",70,10)
tde4.setWidgetAttachModes(req,"3dpoints_color","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_AS_IS")
tde4.setWidgetLinks(req,"3dpoints_color","","","2dpoints_color","")
tde4.setWidgetOffsets(req,"3dpoints_color",40,40,30,10)
#add 2dpoints uniform random color button...
tde4.addButtonWidget(req,"2dpoints_uniform_color","Random color for PGroup 2D Points",70,10)
tde4.setWidgetAttachModes(req,"2dpoints_uniform_color","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_AS_IS")
tde4.setWidgetLinks(req,"2dpoints_uniform_color","","","3dpoints_color","")
tde4.setWidgetOffsets(req,"2dpoints_uniform_color",40,40,30,10)
#add 3dpoints uniform random color button...
tde4.addButtonWidget(req,"3dpoints_uniform_color","Random color for PGroup 3D Points",70,10)
tde4.setWidgetAttachModes(req,"3dpoints_uniform_color","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_AS_IS")
tde4.setWidgetLinks(req,"3dpoints_uniform_color","","","2dpoints_uniform_color","")
tde4.setWidgetOffsets(req,"3dpoints_uniform_color",40,40,30,10)
#toggle buttons...
tde4.addToggleWidget(req,"all_points","All Points",1)
tde4.setWidgetAttachModes(req,"all_points","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_AS_IS")
tde4.setWidgetLinks(req,"all_points","","","3dpoints_uniform_color","")
tde4.setWidgetOffsets(req,"all_points",37,43,30,10)
tde4.addToggleWidget(req,"selected_points","Selected Points",0)
tde4.setWidgetAttachModes(req,"selected_points","ATTACH_POSITION","ATTACH_POSITION","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetLinks(req,"selected_points","all_points","","all_points","")
tde4.setWidgetOffsets(req,"selected_points",78,84,00,10)
#Widget callbacks...
tde4.setWidgetCallbackFunction(req,"all_points","Sensitivity")
tde4.setWidgetCallbackFunction(req,"selected_points","Sensitivity")
tde4.setWidgetCallbackFunction(req,"2dpoints_color","Random_Color")
tde4.setWidgetCallbackFunction(req,"3dpoints_color","Random_Color")
tde4.setWidgetCallbackFunction(req,"2dpoints_uniform_color","Random_Color")
tde4.setWidgetCallbackFunction(req,"3dpoints_uniform_color","Random_Color")

tde4.postCustomRequesterAndContinue(req,window_title,380,160)









