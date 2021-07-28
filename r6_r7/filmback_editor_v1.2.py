# 3DE4.script.name:	Filmback Editor...
# 3DE4.script.version:	v1.2
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui:	Object Browser::Context Menu Lenses
# 3DE4.script.gui:	Object Browser::Context Menu Lens
# 3DE4.script.comment:
# Patcha Saheb(patchasaheb@gmail.com)
# June 1, 2018(Montreal)

def closeButton(req,widget,action):
	tde4.unpostCustomRequester(req)

def optionMenuUpdate(req,widget,action):
	units_menu_value = tde4.getWidgetValue(req,"units_menu")
	tde4.setWidgetSensitiveFlag(req,"new_value_menu",1)
	tde4.setWidgetSensitiveFlag(req,"new_value_text",1)
	tde4.setWidgetSensitiveFlag(req,"convert_btn",1)
	tde4.setWidgetSensitiveFlag(req,"close_btn",1)
	if units_menu_value == 1:
		units_menu_label = " (m)"
	if units_menu_value == 2:
		units_menu_label =  " (cm)"
	if units_menu_value == 3:
		units_menu_label =  " (mm)"	
	if units_menu_value == 4:
		units_menu_label =  " (in)"
	if units_menu_value == 5:
		units_menu_label =  " (ft)"
	if units_menu_value == 6:
		units_menu_label =  " (yd)"
	tde4.setWidgetLabel(req,"units_label",units_menu_label)

def convertCallback(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	lens = tde4.getCameraLens(cam)
	current_width = tde4.getLensFBackWidth(lens)
	current_height = tde4.getLensFBackHeight(lens)
	pixelaspect = tde4.getLensPixelAspect(lens)
	focal_mode = tde4.getCameraFocalLengthMode(cam)
	new_value = float(tde4.getWidgetValue(req,"new_value_text"))
	units_menu_value = tde4.getWidgetValue(req,"units_menu")
	if units_menu_value == 1:
		new_value_conversion = new_value * 100.0
	if units_menu_value == 2:
		new_value_conversion = new_value
	if units_menu_value == 3:
		new_value_conversion = new_value * 0.1
	if units_menu_value == 4:
		new_value_conversion = new_value * 2.54
	if units_menu_value == 5:
		new_value_conversion = new_value * 30.48
	if units_menu_value == 6:
		new_value_conversion = new_value * 91.44
	#if width selected...
	if tde4.getWidgetValue(req,"new_value_menu") == 1:
		tde4.setParameterAdjustFlag(lens,"ADJUST_LENS_FOCAL_LENGTH","",0)
		tde4.updateGUI()
		tde4.setParameterAdjustFlag(lens,"ADJUST_LENS_PIXEL_ASPECT","",0)
		tde4.updateGUI()
		tde4.setParameterAdjustFlag(lens,"ADJUST_LENS_FBACK_WIDTH","",0)
		tde4.updateGUI()
		tde4.setLensFBackWidth(lens,new_value_conversion)
		tde4.setLensPixelAspect(lens,pixelaspect)
		delta = new_value_conversion / current_width

	#if height selected...
	if tde4.getWidgetValue(req,"new_value_menu") == 2:
		tde4.setParameterAdjustFlag(lens,"ADJUST_LENS_FOCAL_LENGTH","",0)
		tde4.updateGUI()
		tde4.setParameterAdjustFlag(lens,"ADJUST_LENS_PIXEL_ASPECT","",0)
		tde4.updateGUI()
		tde4.setParameterAdjustFlag(lens,"ADJUST_LENS_FBACK_HEIGHT","",0)
		tde4.updateGUI()
		tde4.setLensFBackHeight(lens,new_value_conversion)
		tde4.setLensPixelAspect(lens,pixelaspect)
		delta = new_value_conversion / current_height

	if focal_mode == "FOCAL_DYNAMIC":
		zoom_curve = tde4.getCameraZoomCurve(cam)
		keylist = tde4.getCurveKeyList(zoom_curve)
		for key in keylist:
			pos2d = tde4.getCurveKeyPosition(zoom_curve,key)
			pos2d[1] = pos2d[1] * delta
			tde4.setCurveKeyPosition(zoom_curve,key,[pos2d[0],pos2d[1]])
	else:
		tde4.setCameraFocalLength(cam,frame,tde4.getCameraFocalLength(cam,frame) * delta)



window_title = "Patcha Filmback Editor v1.2"
req = tde4.createCustomRequester()
tde4.addOptionMenuWidget(req,"units_menu","Units","m","cm","mm","in","ft","yd")
tde4.setWidgetAttachModes(req,"units_menu","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"units_menu",12,25,23,0)

tde4.addOptionMenuWidget(req,"new_value_menu","","New Filmback Width","New Filmback Height")
tde4.setWidgetAttachModes(req,"new_value_menu","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"new_value_menu",35,70,23,0)
tde4.setWidgetSensitiveFlag(req,"new_value_menu",0)

tde4.addTextFieldWidget(req,"new_value_text","","")
tde4.setWidgetAttachModes(req,"new_value_text","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"new_value_text",72,90,23,0)
tde4.setWidgetSensitiveFlag(req,"new_value_text",0)

tde4.addLabelWidget(req,"units_label","(m)","ALIGN_LABEL_RIGHT")
tde4.setWidgetAttachModes(req,"units_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"units_label",90,98,23,0)

tde4.addButtonWidget(req,"convert_btn","Convert",70,10)
tde4.setWidgetAttachModes(req,"convert_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"convert_btn",57,77,80,0)
tde4.setWidgetSensitiveFlag(req,"convert_btn",0)

tde4.addButtonWidget(req,"close_btn","Close",70,10)
tde4.setWidgetAttachModes(req,"close_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"close_btn",81,97,80,0)
tde4.setWidgetSensitiveFlag(req,"close_btn",0)

#callbacks...
tde4.setWidgetCallbackFunction(req,"close_btn","closeButton")
tde4.setWidgetCallbackFunction(req,"units_menu","optionMenuUpdate")
tde4.setWidgetCallbackFunction(req,"convert_btn","convertCallback")


tde4.postCustomRequesterAndContinue(req,window_title,520,120)