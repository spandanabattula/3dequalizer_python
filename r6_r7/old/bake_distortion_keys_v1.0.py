#
# 3DE4.script.name:		Bake distortion keys into curves...
#
# 3DE4.script.version:		v1.0
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: Bakes distortion keyframes, taking into account any time remap of the Focus channel. Then the Focus channel is automatically reset to linear 1:1.	
#
# Patcha Saheb(patchasaheb@gmail.com)
#


from vl_sdv import*

class bake_keys():

	def main(self):
		self.GUI()

	def Bake_all_curves_allframes(self):
		# remember current state for undo...
		tde4.pushCurrentCurvesToUndoStack()
		cam	= tde4.getCurrentCamera()
		frames = tde4.getCameraNoFrames(cam)
		if cam!= None:
			f	= tde4.getCurrentFrame(cam)
			lens	= tde4.getCameraLens(cam)
		else:	lens	= None
		if lens!=None: 
			model = tde4.getLensLDModel(lens)
		else: model = None
		if model!=None:
		#Bakes all curves, every frame...
			focal	= tde4.getCameraFocalLength(cam,f)
			n	= tde4.getLDModelNoParameters(model)
			para_array = []
			for i0 in range(n):
				for frame in range(1,frames+1):
					tde4.setCurrentFrame(cam,frame)
					focus = tde4.getCameraFocus(cam,tde4.getCurrentFrame(cam))
					para	= tde4.getLDModelParameterName(model,i0)
					if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
						v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
						#print str(frame) + " " + str(v)
						para_array.append(v)
				#delete all curve keys...
				curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
				tde4.deleteAllCurveKeys(curve)	
			#creating new curve keys...
			new_paralist = para_array
			for i1 in range(n):
				i = 1
				for n in new_paralist:
					tde4.setCurrentFrame(cam,i)
					para1	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para1)
					tde4.createCurveKey(curve,[i,n])
					i = i + 1
					if i == frames + 1:
						del new_paralist[0:frames]
						break
					#put all keys mode to linear...
					para2	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para2)
					kl	= tde4.getCurveKeyList(curve,0)
					for k in kl:
						tde4.setCurveKeyMode(curve,k,"LINEAR")
			#reset focus curve...
			focus_curve = tde4.getCameraFocusCurve(cam)
			tde4.deleteAllCurveKeys(focus_curve)
			tde4.createCurveKey(focus_curve,[1,1])
			tde4.createCurveKey(focus_curve,[frames,frames])
			focus_kl = tde4.getCurveKeyList(focus_curve,0)
			for focus_k in focus_kl:
				tde4.setCurveKeyMode(focus_curve,focus_k,"LINEAR")
				
	def Bake_all_curves_existing_frames(self):
		# remember current state for undo...
		tde4.pushCurrentCurvesToUndoStack()
		cam	= tde4.getCurrentCamera()
		frames = tde4.getCameraNoFrames(cam)
		if cam!=None:
			f	= tde4.getCurrentFrame(cam)
			lens	= tde4.getCameraLens(cam)
		else:	lens	= None
		if lens!=None: 
			model = tde4.getLensLDModel(lens)
		else: model = None
		if model!=None:
			focal	= tde4.getCameraFocalLength(cam,f)
			n	= tde4.getLDModelNoParameters(model)
			for i0 in range(n):
				para = tde4.getLDModelParameterName(model,i0)
				curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
				kl = tde4.getCurveKeyList(curve)
				for k in kl:
					key = tde4.getCurveKeyPosition(curve,k)
					tde4.setCurrentFrame(cam,int(key[0]))
					focus = tde4.getCameraFocus(cam,tde4.getCurrentFrame(cam))
					v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
					tde4.deleteCurveKey(curve,k)
					new_key = tde4.createCurveKey(curve,[key[0],v])
					tde4.setCurveKeyMode(curve,new_key,"LINEAR")
			focus_curve = tde4.getCameraFocusCurve(cam)
			tde4.deleteAllCurveKeys(focus_curve)
			tde4.createCurveKey(focus_curve,[1,1])
			tde4.createCurveKey(focus_curve,[frames,frames])
			focus_kl = tde4.getCurveKeyList(focus_curve,0)
			for focus_k in focus_kl:
				tde4.setCurveKeyMode(focus_curve,focus_k,"LINEAR")
		else:
			tde4.postQuestionRequester(self.window_title,"Proper Lens Model not found.","OK","Cancel")
			
	def Bake_selected_curve_allframes(self):
		# remember current state for undo...
		tde4.pushCurrentCurvesToUndoStack()
		cam	= tde4.getCurrentCamera()
		frames = tde4.getCameraNoFrames(cam)
		if cam!= None:
			f	= tde4.getCurrentFrame(cam)
			lens	= tde4.getCameraLens(cam)
		else:	lens	= None
		if lens!= None: 
			model = tde4.getLensLDModel(lens)
		else: model = None
		if model!= None:
			n = tde4.getLDModelNoParameters(model)
			curve = tde4.getFirstCurrentCurve()	
			para_array = []
			for i0 in range(n):
				para	= tde4.getLDModelParameterName(model,i0)
				para_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
				if para_curve == curve:
					for frame in range(1,frames+1):
						tde4.setCurrentFrame(cam,frame)
						focal = tde4.getCameraFocalLength(cam,f)
						if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
							focus = tde4.getCameraFocus(cam,tde4.getCurrentFrame(cam))
							v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
							para_array.append(v)
					tde4.deleteAllCurveKeys(curve)
					curve = tde4.getNextCurrentCurve(curve)
			new_paralist = para_array
			#creating new curve keys...
			curve = tde4.getFirstCurrentCurve()
			for i0 in range(n):
				i = 1
				para	= tde4.getLDModelParameterName(model,i0)
				para_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
				if para_curve == curve:
					for n in new_paralist:
						tde4.setCurrentFrame(cam,i)
						key = tde4.createCurveKey(curve,[i,n])
						tde4.setCurveKeyMode(curve,key,"LINEAR")
						i = i + 1
						if i == frames + 1:
							del new_paralist[0:frames]
							break
					curve = tde4.getNextCurrentCurve(curve)
			focus_curve = tde4.getCameraFocusCurve(cam)
			tde4.deleteAllCurveKeys(focus_curve)
			tde4.createCurveKey(focus_curve,[1,1])
			tde4.createCurveKey(focus_curve,[frames,frames])
			focus_kl = tde4.getCurveKeyList(focus_curve,0)
			for focus_k in focus_kl:
				tde4.setCurveKeyMode(focus_curve,focus_k,"LINEAR")
				
	def Bake_selected_curve_existing_frames(self):
		# remember current state for undo...
		tde4.pushCurrentCurvesToUndoStack()
		cam	= tde4.getCurrentCamera()
		frames = tde4.getCameraNoFrames(cam)
		if cam!= None:
			f	= tde4.getCurrentFrame(cam)
			lens	= tde4.getCameraLens(cam)
		else:	lens	= None
		if lens!= None: 
			model = tde4.getLensLDModel(lens)
		else: model = None
		if model!= None:
			n = tde4.getLDModelNoParameters(model)
			focal = tde4.getCameraFocalLength(cam,f)
			curve = tde4.getFirstCurrentCurve()	
			para_array = []
			for i0 in range(n):
				para	= tde4.getLDModelParameterName(model,i0)
				para_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
				if para_curve == curve:
					kl = tde4.getCurveKeyList(curve)
					for k in kl:
						key = tde4.getCurveKeyPosition(curve,k)
						tde4.setCurrentFrame(cam,int(key[0]))
						focus = tde4.getCameraFocus(cam,tde4.getCurrentFrame(cam))
						v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
						tde4.deleteCurveKey(curve,k)
						new_key = tde4.createCurveKey(curve,[key[0],v])
						tde4.setCurveKeyMode(curve,new_key,"LINEAR")
					curve = tde4.getNextCurrentCurve(curve)				
			focus_curve = tde4.getCameraFocusCurve(cam)
			tde4.deleteAllCurveKeys(focus_curve)
			tde4.createCurveKey(focus_curve,[1,1])
			tde4.createCurveKey(focus_curve,[frames,frames])
			focus_kl = tde4.getCurveKeyList(focus_curve,0)
			for focus_k in focus_kl:
				tde4.setCurveKeyMode(focus_curve,focus_k,"LINEAR")
				
	def Bake_selected_cvs(self):
		# remember current state for undo...
		tde4.pushCurrentCurvesToUndoStack()
		cam	= tde4.getCurrentCamera()
		frames = tde4.getCameraNoFrames(cam)
		if cam!= None:
			f	= tde4.getCurrentFrame(cam)
			lens	= tde4.getCameraLens(cam)
		else:	lens	= None
		if lens!= None: 
			model = tde4.getLensLDModel(lens)
		else: model = None
		if model!= None:
			n = tde4.getLDModelNoParameters(model)
			focal = tde4.getCameraFocalLength(cam,f)
			curve = tde4.getFirstCurrentCurve()	
			para_array = []
			for i0 in range(n):
				para	= tde4.getLDModelParameterName(model,i0)
				para_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
				if para_curve == curve:
					kl = tde4.getCurveKeyList(curve)
					for k in kl:	
						key_selection = tde4.getCurveKeySelectionFlag(curve,k)
						if key_selection  == 1:
							key = tde4.getCurveKeyPosition(curve,k)
							tde4.setCurrentFrame(cam,int(key[0]))
							focus = tde4.getCameraFocus(cam,tde4.getCurrentFrame(cam))
							v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
							tde4.deleteCurveKey(curve,k)
							new_key = tde4.createCurveKey(curve,[key[0],v])
							tde4.setCurveKeyMode(curve,new_key,"LINEAR")
					curve = tde4.getNextCurrentCurve(curve)							
			focus_curve = tde4.getCameraFocusCurve(cam)
			tde4.deleteAllCurveKeys(focus_curve)
			tde4.createCurveKey(focus_curve,[1,1])
			tde4.createCurveKey(focus_curve,[frames,frames])
			focus_kl = tde4.getCurveKeyList(focus_curve,0)
			for focus_k in focus_kl:
				tde4.setCurveKeyMode(focus_curve,focus_k,"LINEAR")		
				
	def HelpText(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		print "************************************************************************************************************************************"
		print " "
		print "The distortion curves in 3DE can be time remapped by the Focus channel. Use this tool if you wish to bake the non linear Focus time channel LUT into the distortion curves."
		print "The non-linear Focus curve will be automatically returned to the default linear 1:1 frames curve."
		print " "
		print "************************************************************************************************************************************"

	def doit(self,requester,widget,action):
		if tde4.getWidgetValue(self.req,"operation") == 1:
			self.Bake_all_curves_existing_frames()	
		if tde4.getWidgetValue(self.req,"operation") == 2:
			self.Bake_all_curves_allframes()
		if tde4.getWidgetValue(self.req,"operation") == 3:
			self.Bake_selected_curve_allframes()
		if tde4.getWidgetValue(self.req,"operation") == 4:
			self.Bake_selected_curve_existing_frames()
		if tde4.getWidgetValue(self.req,"operation") == 5:
			self.Bake_selected_cvs()					
				
	def GUI(self):
		self.window_title = "bake distortion keys into curves v1.0"
		self.req	= tde4.createCustomRequester()	
		tde4.addOptionMenuWidget(self.req,"operation","Operation","Bake all curves, only existing keys","Bake all curves, every frame","Bake selected curve, every frame","Bake selected curve, only existing keys","Bake Selected Cvs")
		tde4.setWidgetAttachModes(self.req,"operation","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"operation",25,98,10,0)    	
		tde4.addButtonWidget(self.req,"bake_keys","Bake distortion keys",160,50)
		tde4.setWidgetAttachModes(self.req,"bake_keys","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_POSITION")
		tde4.setWidgetOffsets(self.req,"bake_keys",40,85,95,10)
		tde4.postCustomRequesterAndContinue(self.req,self.window_title,450,150)
		tde4.addButtonWidget(self.req,"help","Help",160,50)
		tde4.setWidgetAttachModes(self.req,"help","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_POSITION")
		tde4.setWidgetOffsets(self.req,"help",10,20,105,15)
		tde4.postCustomRequesterAndContinue(self.req,self.window_title,450,150)		
#callbacks...
		tde4.setWidgetCallbackFunction(bake.req,"bake_keys","bake.doit")
		tde4.setWidgetCallbackFunction(bake.req,"help","bake.HelpText")

bake = bake_keys()
bake.main()				










