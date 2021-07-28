# 3DE4.script.name:Copy FOV to camera...
# 3DE4.script.version:	v1.2
# 3DE4.script.comment:	Copies FOV values from one camera/proxy, to another
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.gui:	Orientation Controls::Edit
# 3DE4.script.gui:	Manual Tracking Controls::Edit
# 3DE4.script.hide: false
# 3DE4.script.startup: false
#Patcha Saheb/Michael Karp
class Copy_FOV():
	def main(self):
		self.GUI()
	def Set_Callback(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		cam = tde4.getCurrentCamera()
		try:
			left = float(tde4.getWidgetValue(self.req,"left"))
			right = float(tde4.getWidgetValue(self.req,"right"))
			top = float(tde4.getWidgetValue(self.req,"top"))
			bottom = float(tde4.getWidgetValue(self.req,"bottom"))
			tde4.setCameraFOV(cam,left,right,bottom,top)
		except:
			tde4.postQuestionRequester(self.copyTitle,"Error, please enter float values in set FOV fields.","Ok")
		
	def Copy_Callback(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		cam_list = []
		n = tde4.getCameraList(0)
		for cam in n:
			name = tde4.getCameraName(cam)
			cam_list.append(name)
		s_cam = tde4.getWidgetValue(self.req,"sourceCam")
		s_proxy = tde4.getWidgetValue(self.req,"sourceProxy")
		t_cam = tde4.getWidgetValue(self.req,"targetCam")
		t_proxy = tde4.getWidgetValue(self.req,"targetProxy")
		if widget == "copy":
			s_proxy_fov = tde4.setCameraProxyFootage(n[s_cam-1],s_proxy-1)
			s_fov = tde4.getCameraFOV(n[s_cam-1])
			tde4.setCameraProxyFootage(n[t_cam-1],t_proxy-1)
			tde4.setCameraFOV(n[t_cam-1],s_fov[0],s_fov[1],s_fov[2],s_fov[3])
			s_fov = str(str(s_fov[0]) + " " + str(s_fov[1]) + " " + str(s_fov[2]) + " " + str(s_fov[3]))
			t_fov = tde4.getCameraFOV(n[t_cam-1])
			tde4.setWidgetValue(self.req,"sourceFOV",str(s_fov))
			t_fov = str(str(t_fov[0]) + " " + str(t_fov[1]) + " " + str(t_fov[2]) + " " + str(t_fov[3]))
			tde4.setWidgetValue(self.req,"targetFOV",t_fov)
		if widget == "refresh":
			cam = tde4.getCurrentCamera()
			current_proxy = tde4.getCameraProxyFootage(cam)
			tde4.modifyOptionMenuWidget(self.req,"sourceCam","Source Camera",*cam_list)
			tde4.modifyOptionMenuWidget(self.req,"targetCam","Target Camera",*cam_list)
			s_proxy_fov = tde4.setCameraProxyFootage(n[s_cam-1],s_proxy-1)
			s_fov = tde4.getCameraFOV(n[s_cam-1])
			tde4.setCameraProxyFootage(n[t_cam-1],t_proxy-1)
			#tde4.setCameraFOV(n[t_cam-1],s_fov[0],s_fov[1],s_fov[2],s_fov[3])
			s_fov = str(str(s_fov[0]) + " " + str(s_fov[1]) + " " + str(s_fov[2]) + " " + str(s_fov[3]))
			t_fov = tde4.getCameraFOV(n[t_cam-1])
			tde4.setWidgetValue(self.req,"sourceFOV",str(s_fov))
			t_fov = str(str(t_fov[0]) + " " + str(t_fov[1]) + " " + str(t_fov[2]) + " " + str(t_fov[3]))
			tde4.setWidgetValue(self.req,"targetFOV",t_fov)
			tde4.setCameraProxyFootage(cam,current_proxy)
		if widget == "close":
			tde4.unpostCustomRequester(self.req)
	def GUI(self):
		self.req = tde4.createCustomRequester()
		self.copyTitle="Patcha Copy FOV to camera v1.2"
#camera list...
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		cam_list = []
		n = tde4.getCameraList(0)
		for cam in n:
			name = tde4.getCameraName(cam)
			cam_list.append(name)
#set fov widgets...
		tde4.addTextFieldWidget(self.req, "left", "Left","  ")
		tde4.setWidgetAttachModes(self.req,"left","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"left",8,18,10,0)
		tde4.addTextFieldWidget(self.req, "right", "Right","  ")
		tde4.setWidgetAttachModes(self.req,"right","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"right",28,38,10,0)
		tde4.addTextFieldWidget(self.req, "top", "Top","  ")
		tde4.setWidgetAttachModes(self.req,"top","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"top",48,58,10,0)
		tde4.addTextFieldWidget(self.req, "bottom", "Bottom","  ")
		tde4.setWidgetAttachModes(self.req,"bottom","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"bottom",73,83,10,0)
		tde4.addButtonWidget(self.req,"set_fov","Set FOV",70,10)
		tde4.setWidgetAttachModes(self.req,"set_fov","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"set_fov",86,96,10,0)		
		tde4.addSeparatorWidget(self.req,"sep0")
		tde4.setWidgetAttachModes(self.req,"sep0","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep0",2,98,30,0)	
#source widgets...
		tde4.addOptionMenuWidget(self.req,"sourceCam","Source Camera",*cam_list)
		tde4.setWidgetAttachModes(self.req,"sourceCam","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sourceCam",25,95,50,0)		
		tde4.addOptionMenuWidget(self.req,"sourceProxy","Source Proxy","Main","Alternate #1","Alternate #2","Alternate #3")
		tde4.setWidgetAttachModes(self.req,"sourceProxy","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sourceProxy",25,95,80,0)			
		tde4.addTextFieldWidget(self.req, "sourceFOV", "Source FOV", " ")
		tde4.setWidgetAttachModes(self.req,"sourceFOV","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sourceFOV",25,95,110,0)		
		tde4.addSeparatorWidget(self.req,"sep1")
		tde4.setWidgetAttachModes(self.req,"sep1","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep1",2,98,130,0)		
#target widgets...
		tde4.addOptionMenuWidget(self.req,"targetCam","Target Camera",*cam_list)
		tde4.setWidgetAttachModes(self.req,"targetCam","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"targetCam",25,95,150,0)			
		tde4.addOptionMenuWidget(self.req,"targetProxy","Target Proxy","Main","Alternate #1","Alternate #2","Alternate #3")
		tde4.setWidgetAttachModes(self.req,"targetProxy","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"targetProxy",25,95,180,0)		
		tde4.addTextFieldWidget(self.req, "targetFOV", "Target FOV", " ")
		tde4.setWidgetAttachModes(self.req,"targetFOV","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"targetFOV",25,95,210,0)			
#disable widgets...
		tde4.setWidgetSensitiveFlag(self.req,"sourceFOV",0)
		tde4.setWidgetSensitiveFlag(self.req,"targetFOV",0)
#copy button widget...
		tde4.addButtonWidget(self.req,"copy","Copy FOV",90,10)	
		tde4.setWidgetAttachModes(self.req,"copy","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"copy",46,62,240,0)
#refresh button widget...
		tde4.addButtonWidget(self.req,"refresh","Refresh",90,10)	
		tde4.setWidgetAttachModes(self.req,"refresh","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"refresh",64,80,240,0)
#close button widget...
		tde4.addButtonWidget(self.req,"close","Close",90,10)	
		tde4.setWidgetAttachModes(self.req,"close","ATTACH_POSITION", "ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"close",82,97,240,0)
#callback...
		tde4.setWidgetCallbackFunction(self.req,"copy","copy.Copy_Callback")
		tde4.setWidgetCallbackFunction(self.req,"refresh","copy.Copy_Callback")
		tde4.setWidgetCallbackFunction(self.req,"close","copy.Copy_Callback")
		tde4.setWidgetCallbackFunction(self.req,"set_fov","copy.Set_Callback")
		tde4.postCustomRequesterAndContinue(self.req,self.copyTitle,550,270)
		
copy = Copy_FOV()
copy.main()
