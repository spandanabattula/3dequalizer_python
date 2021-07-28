#
# 3DE4.script.name:	Nudge Curve Key...
#
# 3DE4.script.version:	v1.0b8
#
# 3DE4.script.gui:	Curve Editor::Edit
#
# 3DE4.script.comment:	Nudges/edits the key frame(s) in the Curve Editor
#
#change log
#create new refresh button
#
#Patcha Saheb(patchasaheb@gmail.com)

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)

class Nudge_Curve_Key():

	def main(self):
		self.GUI()
		
#update function...
	def Update(self,requester):
		self.req = requester
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		curve = tde4.getFirstCurrentCurve()
		if curve != None:
			cmode = tde4.getCurrentCurveMode()
			if cmode!="DISTORTION_CURVES":
				cam	= tde4.getCurrentCamera()
				offset	= tde4.getCameraFrameOffset(cam)-1
			else:
				offset	= 0.0	
			kl = tde4.getCurveKeyList(curve,1)
			if len(kl) > 0:
				k = kl[0]
				key = tde4.getCurveKeyPosition(curve,k)
				tde4.setWidgetValue(self.req,"x",str(key[0]+offset))
				tde4.setWidgetValue(self.req,"y",str(key[1]+offset))
				
	def Refresh(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		curve = tde4.getFirstCurrentCurve()
		if curve != None:
			cmode = tde4.getCurrentCurveMode()
			if cmode!="DISTORTION_CURVES":
				cam	= tde4.getCurrentCamera()
				offset	= tde4.getCameraFrameOffset(cam)-1
			else:
				offset	= 0.0	
			kl = tde4.getCurveKeyList(curve,1)
			if len(kl) > 0:
				k = kl[0]
				key = tde4.getCurveKeyPosition(curve,k)
				tde4.setWidgetValue(self.req,"x",str(key[0]+offset))
				tde4.setWidgetValue(self.req,"y",str(key[1]+offset))				
		
#slider widgets update function	...	
	def Slider_Inc(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		toggle = tde4.getWidgetValue(self.req,"toggle")			
		slider_v = tde4.getWidgetValue(self.req,"slider")
		slider_text_v = tde4.getWidgetValue(self.req,"slidertext")
		x_int_slider_v = tde4.getWidgetValue(self.req,"x_int_slider")
		x_slider_v = tde4.getWidgetValue(self.req,"x_slider")
		x_slider_text_v = tde4.getWidgetValue(self.req,"x_slidertext")
		if widget == "slider":
			tde4.setWidgetValue(self.req,"slidertext",str(slider_v))	
		if widget == "slidertext":
			if float(slider_text_v) <= 1.0:
				tde4.setWidgetSensitiveFlag(self.req,"slider",1)
				tde4.setWidgetValue(self.req,"slider",str(slider_text_v))
			else:
				tde4.setWidgetSensitiveFlag(self.req,"slider",0)
		if widget == "x_slider":
			tde4.setWidgetValue(self.req,"x_slidertext",str(x_slider_v))
		if widget == "x_slidertext":
			if toggle == 0:
				if float(x_slider_text_v) <= 10:
					tde4.setWidgetValue(self.req,"x_slider",str(x_slider_text_v))
			if toggle == 1:
				if float(x_slider_text_v) <= 10:
					tde4.setWidgetValue(self.req,"x_int_slider",str(x_slider_text_v))
					
#toggle button function...				
	def Toggle(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action	
		toggle = tde4.getWidgetValue(self.req,"toggle")	
		x_int_slider_v = tde4.getWidgetValue(self.req,"x_int_slider")
		x_slider_v = tde4.getWidgetValue(self.req,"x_slider")
		x_slider_text_v = tde4.getWidgetValue(self.req,"x_slidertext")						
		if toggle == 0:
			tde4.setWidgetSensitiveFlag(self.req,"x_slider",1)
			tde4.setWidgetSensitiveFlag(self.req,"x_int_slider",0)
			tde4.setWidgetValue(self.req,"x_slidertext",str(x_slider_v))
		else:
			tde4.setWidgetSensitiveFlag(self.req,"x_slider",0)
			tde4.setWidgetSensitiveFlag(self.req,"x_int_slider",1)
			tde4.setWidgetValue(self.req,"x_slidertext",str(x_int_slider_v))
			
#pickup button function...				
	def Pickup(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action	
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)			
		currentCurve= tde4.getFirstCurrentCurve()
		while currentCurve!=None:
			pu= tde4.evaluateCurve(currentCurve,frame)
			key = tde4.createCurveKey(currentCurve,[frame,pu])
			tde4.setCurveKeyMode(currentCurve,key,"LINEAR")
			tde4.setCurveKeyFixedXFlag(currentCurve,key,1)
			tde4.filterPGroup(tde4.getCurrentPGroup(),tde4.getCurrentCamera())
			currentCurve=tde4.getNextCurrentCurve(currentCurve)	
			
#jump keys function...				
	def Jump(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action	
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		curve = tde4.getFirstCurrentCurve()
		if widget == "nextkey":
			kl = tde4.getCurveKeyList(curve,0)
			f		= 1000000
			for k in kl:
				pos = tde4.getCurveKeyPosition(curve,k)
				if int(pos[0])>frame and int(pos[0])<f:
					f	= int(pos[0])
					break
			if f!= 1000000:
				tde4.setCurrentFrame(cam,f)
		if widget == "previouskey":
			kl = tde4.getCurveKeyList(curve,0)
			kl.reverse()
			f		= -1
			for k in kl:
				pos = tde4.getCurveKeyPosition(curve,k)
				if int(pos[0])<frame and int(pos[0])>f:
					f	= int(pos[0])
					break
			if f!= -1:
				tde4.setCurrentFrame(cam,f)	
							
#help...				
	def Help(self,requester,widget,action):
		self.help_req = requester
		self.widget = widget
		self.action = action	
		self.help_req = tde4.createCustomRequester()
		tde4.addTextAreaWidget(self.help_req,"textarea","",0,0)
		tde4.setWidgetAttachModes(self.help_req,"textarea","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW")
		tde4.setWidgetOffsets(self.help_req,"textarea",2,2,2,2)
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","The Nudge Curve Key will nudge or edit the x and y values of the key frames in a curve in the 3DE Curve Editor.\n\n")                
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","X is frame number, or focal length in certain distortion curve scenarios, and y is the value of the translate, rotate, focal or distortion, etc.\n\n") 
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","Select one or more keys with alt+LMD marquee, and then nudge. Keys from only one curve can be selected for nudging at a time.\n\n") 
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","The increment value for the +- nudge buttons can be adjust with the slider or the data fields.\n\n") 
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","Integer snap mode will round any fractional frame numbers down to round number integers, when the +- X nudge is clicked.\n\n") 
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","If the curves for a distortion curve are displaying in mm focal length, then it is best if Integer snap is turned off, since some distortion keys in focal length mode might increment in large and unwanted 10mm jumps.\n\n")
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","If multiple keys are selected and then a new value is entered in an x/y data field, this might be undesirable, since keys will clump together .\n\n")
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","Jump previous key and Jump next key will jump to the next key in the curve editor.\n\n") 
		tde4.appendTextAreaWidgetString(self.help_req,"textarea","Pickup key will add a keyframe to the selected curve, at the frame number from the timeline. The key will be at the pre-existing unkeyed y value\n\n") 
		tde4.postCustomRequesterAndContinue(self.help_req,"Help",800,520)									
				
#main nudge function...
	def Nudge2d(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		curve = tde4.getFirstCurrentCurve()
		toggle = tde4.getWidgetValue(self.req,"toggle")	
		x_v = tde4.getWidgetValue(self.req,"x_slidertext")
		v = tde4.getWidgetValue(self.req,"slidertext")
		x = tde4.getWidgetValue(self.req,"x")
		y = tde4.getWidgetValue(self.req,"y")
		while curve != None:
			cmode = tde4.getCurrentCurveMode()
			if cmode!="DISTORTION_CURVES":
				cam	= tde4.getCurrentCamera()
				offset	= tde4.getCameraFrameOffset(cam)-1
			else:
				offset	= 0.0			
			kl = tde4.getCurveKeyList(curve,1)
			for key in kl:
				vec2d = tde4.getCurveKeyPosition(curve,key)
#push current curves to undo stack...
				tde4.pushCurrentCurvesToUndoStack()
				if widget == "x+":
					if toggle == 0: i =vec2d[0] + float(x_v)
					else: i =int(float(vec2d[0])) + int(float(x_v))
					tde4.setCurveKeyPosition(curve,key,[float(i),vec2d[1]])
					tde4.setWidgetValue(self.req,"x",str(float(i)+offset))
				if widget == "x-":
					if toggle == 0: i =vec2d[0] - float(x_v)
					else: i =int(float(vec2d[0])) - int(float(x_v))
					tde4.setCurveKeyPosition(curve,key,[float(i),vec2d[1]])
					tde4.setWidgetValue(self.req,"x",str(float(i)+offset))
				if widget == "y+":
					i = vec2d[1] + float(v)
					tde4.setCurveKeyPosition(curve,key,[vec2d[0],i])
					tde4.setWidgetValue(self.req,"y",str(i))						
				if widget == "y-":
					i = vec2d[1] - float(v)
					tde4.setCurveKeyPosition(curve,key,[vec2d[0],i])
					tde4.setWidgetValue(self.req,"y",str(i))
				if widget == "x":
					x = float(x) + 0.0
					tde4.setCurveKeyPosition(curve,key,[int(x)-offset,vec2d[1]])
				if widget == "y":
					tde4.setCurveKeyPosition(curve,key,[vec2d[0],float(y)])	
			tde4.filterPGroup(pg,cam)
			curve = tde4.getNextCurrentCurve(curve)
		
	
#build GUI...			
	def GUI(self):
		self.window_title = "Patcha Nudge Curve Key v1.0b8"
		self.req = tde4.createCustomRequester()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		curve = tde4.getFirstCurrentCurve()
		if curve != None:
#menu bar widget...
			tde4.addMenuBarWidget(self.req,"menu_bar")
			tde4.setWidgetAttachModes(self.req,"menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"menu_bar",0,100,1,0)	
			tde4.addMenuWidget(self.req,"about","About","menu_bar")
			tde4.addMenuButtonWidget(self.req,"help","Help","about")				
#add x text field widget...
			tde4.addTextFieldWidget(self.req,"x","X"," ")
			tde4.setWidgetAttachModes(self.req,"x","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"x",20,50,30,0)				
#add x increment button widget...	
			tde4.addButtonWidget(self.req,"x-","X-",70,10)	
			tde4.setWidgetAttachModes(self.req,"x-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"x-",55,70,30,0)			
			tde4.addButtonWidget(self.req,"x+","X+",70,10)	
			tde4.setWidgetAttachModes(self.req,"x+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"x+",75,90,30,0)	
#add x float slider widget...
			tde4.addScaleWidget(self.req,"x_slider"," ","DOUBLE",1,10,1)
			tde4.setWidgetAttachModes(self.req,"x_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"x_slider",5,70,60,0)
			tde4.setWidgetSensitiveFlag(self.req,"x_slider",0)
#add x int slider widget...
			tde4.addScaleWidget(self.req,"x_int_slider"," ","INT",1,10,1)
			tde4.setWidgetAttachModes(self.req,"x_int_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"x_int_slider",31,70,90,0)				
#add x textfield widget...
			tde4.addTextFieldWidget(self.req,"x_slidertext"," ","1")		
			tde4.setWidgetAttachModes(self.req,"x_slidertext","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"x_slidertext",75,95,75,0)
#add toggle widget...
			tde4.addToggleWidget(self.req,"toggle","Integer Snap",1)		
			tde4.setWidgetAttachModes(self.req,"toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"toggle",25,30,90,0)						
#separator widget...
			tde4.addSeparatorWidget(self.req,"sep")		
			tde4.setWidgetAttachModes(self.req,"sep","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"sep",2,98,110,0)							
#add y text field widget...
			tde4.addTextFieldWidget(self.req,"y","Y"," ")
			tde4.setWidgetAttachModes(self.req,"y","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"y",20,50,130,0)
#add y increment button widget...	
			tde4.addButtonWidget(self.req,"y-","Y-",70,10)	
			tde4.setWidgetAttachModes(self.req,"y-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"y-",55,70,130,0)			
			tde4.addButtonWidget(self.req,"y+","Y+",70,10)	
			tde4.setWidgetAttachModes(self.req,"y+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"y+",75,90,130,0)	
#add y slider widget...
			tde4.addScaleWidget(self.req,"slider"," ","DOUBLE",0.01,1.0,0.1)		
			tde4.setWidgetAttachModes(self.req,"slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"slider",5,70,160,0)	
#add slider textfield widget...
			tde4.addTextFieldWidget(self.req,"slidertext"," ","0.1")		
			tde4.setWidgetAttachModes(self.req,"slidertext","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"slidertext",75,95,160,0)	
#jump previous key...
			tde4.addButtonWidget(self.req,"previouskey","Previous Key",70,10)
			tde4.setWidgetAttachModes(self.req,"previouskey","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"previouskey",2,25,190,0)	
#jump pickup key...
			tde4.addButtonWidget(self.req,"pickup","Pickup key",70,10)
			tde4.setWidgetAttachModes(self.req,"pickup","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"pickup",27,50,190,0)	
#jump next key...
			tde4.addButtonWidget(self.req,"nextkey","Next Key",70,10)
			tde4.setWidgetAttachModes(self.req,"nextkey","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"nextkey",52,75,190,0)	
#refresh button...
			tde4.addButtonWidget(self.req,"refresh","Refresh",70,10)
			tde4.setWidgetAttachModes(self.req,"refresh","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
			tde4.setWidgetOffsets(self.req,"refresh",77,98,190,0)														
#widgetcallbacks...
			tde4.setWidgetCallbackFunction(self.req,"slider","n.Slider_Inc")		
			tde4.setWidgetCallbackFunction(self.req,"slidertext","n.Slider_Inc")
			tde4.setWidgetCallbackFunction(self.req,"x_slider","n.Slider_Inc")	
			tde4.setWidgetCallbackFunction(self.req,"x_slidertext","n.Slider_Inc")
			tde4.setWidgetCallbackFunction(self.req,"x_int_slider","n.Toggle")				
			tde4.setWidgetCallbackFunction(self.req,"toggle","n.Toggle")												
			tde4.setWidgetCallbackFunction(self.req,"x+","n.Nudge2d")	
			tde4.setWidgetCallbackFunction(self.req,"x-","n.Nudge2d")		
			tde4.setWidgetCallbackFunction(self.req,"y+","n.Nudge2d")	
			tde4.setWidgetCallbackFunction(self.req,"y-","n.Nudge2d")	
			tde4.setWidgetCallbackFunction(self.req,"x","n.Nudge2d")	
			tde4.setWidgetCallbackFunction(self.req,"y","n.Nudge2d")	
			tde4.setWidgetCallbackFunction(self.req,"pickup","n.Pickup")	
			tde4.setWidgetCallbackFunction(self.req,"previouskey","n.Jump")
			tde4.setWidgetCallbackFunction(self.req,"nextkey","n.Jump")
			tde4.setWidgetCallbackFunction(self.req,"help","n.Help")	
			tde4.setWidgetCallbackFunction(self.req,"refresh","n.Refresh")
			tde4.postCustomRequesterAndContinue(self.req,self.window_title,440,220,"n.Update")
		else:
			tde4.postQuestionRequester(self.window_title,"There is no current curve.","Ok")		
n = Nudge_Curve_Key()
n.main()


