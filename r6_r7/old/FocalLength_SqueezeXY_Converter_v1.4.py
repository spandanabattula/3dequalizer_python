#
# 3DE4.script.name:		FocalLength-SqueezeX/Y Converter...
#
# 3DE4.script.version:		v1.4
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: 
#
# Patcha Saheb(patchasaheb@gmail.com) / Michael Karp (mckarp@aol.com)

# Pre bakes all distortion curves, returns focus to 1:1, works correctly

#pseudo code...

#reciprocal of x is 1/x

#Convert sqx to focal
#Pre bake sqx & sy and set focus curve to 1:1
#Take reciprocal of SqX
#Multiply reciprocal of SqX  * (SqY)
#Multiply reciprocal of SqX  * (SqX) [sets to 1]
#Multiply reciprocal of SqX  * (Focal)

#Convert sqy to focal
#Pre bake sqx & sy and set focus curve to 1:1
#Take reciprocal of SqY
#Multiply reciprocal of SqY  * (SqX)
#Multiply reciprocal of SqY  * (SqY) [sets to 1]
#Multiply reciprocal of SqY  * (Focal)

#Convert focal to sqx&sqy
#Pre bake sqx & sy and set focus curve to 1:1
#Take reciprocal of Focal
#Multiply reciprocal of Focal  * (SqX)
#Multiply reciprocal of Focal  * (SqY)
#Multiply reciprocal of Focal  * (Focal) [sets to 1]
#Multiply new sqx * (first frame's Focal value)
#Multiply new sqy * (first frame's Focal value)
#make focal curve static to first frame's focal value

from vl_sdv import*
import os,sys
import math

def Convert(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(cam)

	if cam!=None:
		frame	= tde4.getCurrentFrame(cam)
		lens	= tde4.getCameraLens(cam)
	else:	lens	= None
	if lens!=None: model = tde4.getLensLDModel(lens)
	else: model = None

	if model!=None:	
	#create emphty lists...
		sq_x_list = []
		sq_y_list = []
		focal_list = []
		new_sq_x_list = []
		new_sq_y_list = []
		
		# remember current state for undo...
		tde4.pushCurrentCurvesToUndoStack()
		#filling lists...
		n	= tde4.getLDModelNoParameters(model)
		count = 0
		#squeeze_x data...
		for i0 in range(n):
			count = count + 1
			if count == 12:
				for f in range(1,frames+1):
					para	= tde4.getLDModelParameterName(model,i0)
					focal = tde4.getCameraFocalLength(cam,f) * 10.0
					focus = tde4.getCameraFocus(cam,f)
					if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
						v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
						sq_x_list.append(v)
		#squeeze_y data...
			if count == 13:
				for f in range(1,frames+1):
					para	= tde4.getLDModelParameterName(model,i0)
					focal = tde4.getCameraFocalLength(cam,f) * 10.0
					focus = tde4.getCameraFocus(cam,f)
					if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
						v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
						sq_y_list.append(v)
		#focal data...
		for i in range(1,frames+1):
			focal = tde4.getCameraFocalLength(cam,i) * 10.0
			focal_list.append(focal)						

		#Function to pre bake all distortion curves and  reset focus curve to 1:1
		def Pre_Bake():
			# remember current state for undo...
			tde4.pushCurrentCurvesToUndoStack()
			cam	= tde4.getCurrentCamera()
			current_frame = tde4.getCurrentFrame(cam)
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
				n	= tde4.getLDModelNoParameters(model)
				para_array = []
				for i0 in range(n):
					for frame in range(1,frames+1):
						tde4.setCurrentFrame(cam,frame)
						focal	= tde4.getCameraFocalLength(cam,tde4.getCurrentFrame(cam))
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
				tde4.setCurrentFrame(cam,current_frame)
	
		
		for j in range(0,len(sq_y_list)):
			#multiply reciprocal of sqx with sqy...
			new_sq_y = (1.0/float(sq_x_list[j])) * sq_y_list[j]
			new_sq_y_list.append(new_sq_y)
			#multiply reciprocal of sqy with sqx...
			new_sq_x = (1.0/float(sq_y_list[j])) * sq_x_list[j]
			new_sq_x_list.append(new_sq_x)
			
		if widget == "sqx_to_focal":
			Pre_Bake()
			#put new focal values...
			for m in range(1,frames+1):
				new_focal = (1.0/float(sq_x_list[m-1])) * focal_list[m-1]
				tde4.setCameraFocalLengthMode(cam,"FOCAL_DYNAMIC")
				tde4.setCameraFocalLength(cam,m,(new_focal/10.0))			
			#put new sqx and sqy values...
			count1 = 0
			for i1 in range(n):
				count1 = count1 + 1
				if count1 == 13:
					para	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					kl = tde4.getCurveKeyList(curve,0)
					for key in kl:
						tde4.deleteCurveKey(curve,key)
					for f in range(1,frames+1):
						para	= tde4.getLDModelParameterName(model,i1)
						curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
						k = tde4.createCurveKey(curve,[f,new_sq_y_list[f-1]])
						tde4.setCurveKeyMode(curve,k,"LINEAR")
				if count1 == 12:
					para	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					kl = tde4.getCurveKeyList(curve,0)
					for key in kl:
						tde4.deleteCurveKey(curve,key)
					for f in range(1,frames+1):
						para	= tde4.getLDModelParameterName(model,i1)
						curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
						k = tde4.createCurveKey(curve,[f,1])	
						tde4.setCurveKeyMode(curve,k,"LINEAR")
						
		if widget == "sqy_to_focal":
			Pre_Bake()
			#put new focal values...
			for m in range(1,frames+1):
				new_focal = (1.0/float(sq_y_list[m-1])) * focal_list[m-1]
				tde4.setCameraFocalLengthMode(cam,"FOCAL_DYNAMIC")
				tde4.setCameraFocalLength(cam,m,(new_focal/10.0))			
			#put new sqx and sqy values...
			count1 = 0
			for i1 in range(n):
				count1 = count1 + 1
				if count1 == 12:
					para	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					kl = tde4.getCurveKeyList(curve,0)
					for key in kl:
						tde4.deleteCurveKey(curve,key)
					for f in range(1,frames+1):
						para	= tde4.getLDModelParameterName(model,i1)
						curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
						k = tde4.createCurveKey(curve,[f,new_sq_x_list[f-1]])
						tde4.setCurveKeyMode(curve,k,"LINEAR")
				if count1 == 13:
					para	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					kl = tde4.getCurveKeyList(curve,0)
					for key in kl:
						tde4.deleteCurveKey(curve,key)
					for f in range(1,frames+1):
						para	= tde4.getLDModelParameterName(model,i1)
						curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
						k = tde4.createCurveKey(curve,[f,1])	
						tde4.setCurveKeyMode(curve,k,"LINEAR")	

		if widget == "focal_to_sqxy":
			Pre_Bake()
			#get reciprocal of focal data...
			focal_list = []
			new_sq_x_list = []
			new_sq_y_list = []
			for i in range(1,frames+1):
				focal = tde4.getCameraFocalLength(cam,i) * 10.0
				focal_list.append(1/focal)	
					
			#get first frame's focal value
			focal = tde4.getCameraFocalLength(cam,1) * 10.0
			
			
			for j in range(0,len(focal_list)):
				#Multiply reciprocal of Focal  * sqx
				new_sq_x = focal_list[j] * sq_x_list[j]
				#Multiply new sqx * (first frame's Focal value)
				new_sq_x = new_sq_x * focal
				new_sq_x_list.append(new_sq_x)
				#Multiply reciprocal of Focal  * sqy
				new_sq_y = focal_list[j] * sq_y_list[j]
				#Multiply new sqy * (first frame's Focal value)
				new_sq_y = new_sq_y * focal
				new_sq_y_list.append(new_sq_y)
			
			#put new focal values...
			for m in range(1,frames+1):
				tde4.setCameraFocalLengthMode(cam,"FOCAL_DYNAMIC")
				tde4.setCameraFocalLength(cam,m,(focal/10.0))
							
			#put new sqx and sqy values...
			count1 = 0
			for i1 in range(n):
				count1 = count1 + 1
				if count1 == 12:
					para	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					kl = tde4.getCurveKeyList(curve,0)
					for key in kl:
						tde4.deleteCurveKey(curve,key)
					for f in range(1,frames+1):
						para	= tde4.getLDModelParameterName(model,i1)
						curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
						k = tde4.createCurveKey(curve,[f,float(new_sq_x_list[f-1])])
						tde4.setCurveKeyMode(curve,k,"LINEAR")
				if count1 == 13:
					para	= tde4.getLDModelParameterName(model,i1)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					kl = tde4.getCurveKeyList(curve,0)
					for key in kl:
						tde4.deleteCurveKey(curve,key)
					for f in range(1,frames+1):
						para	= tde4.getLDModelParameterName(model,i1)
						curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
						k = tde4.createCurveKey(curve,[f,new_sq_y_list[f-1]])
						tde4.setCurveKeyMode(curve,k,"LINEAR")

		if widget == "factor_slider":		
			factor_slider = tde4.getWidgetValue(req,"factor_slider")
			tde4.setWidgetValue(req,"factor_text",str(factor_slider))
			
		if widget == "factor_text":				
			factor_text = tde4.getWidgetValue(req,"factor_text")
			factor_slider = tde4.getWidgetValue(req,"factor_slider")
			if float(factor_text) >= 0.001:
				if float(factor_text) > 2.0:
					tde4.setWidgetSensitiveFlag(req,"factor_slider",0)
				else:
					tde4.setWidgetValue(req,"factor_slider",str(factor_text))
					tde4.setWidgetSensitiveFlag(req,"factor_slider",1)
			else:
				tde4.setWidgetValue(req,"factor_text","1.1")
				tde4.setWidgetValue(req,"factor_slider","1.1")
				tde4.postQuestionRequester(window_title,"Error, minimum value is 0.001","OK")
				
		v = tde4.getWidgetValue(req,"factor_text")		
		if widget == "apply":
			#multiply factor value with focal curve...
			for f in range(0,frames):
				tde4.setCameraFocalLengthMode(cam,"FOCAL_DYNAMIC")
				focal = (focal_list[f] / 10) * float(v)
				tde4.setCameraFocalLength(cam,f+1,focal)
			n	= tde4.getLDModelNoParameters(model)
			count = 0
			for i0 in range(n):
				count = count + 1
				#multiply raw sqx keys with factor value...
				if count == 12:
					para	= tde4.getLDModelParameterName(model,i0)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
						kl = tde4.getCurveKeyList(curve,0)
						for key in kl:
							pos = tde4.getCurveKeyPosition(curve,key)
							f = float(pos[1]) * float(v)
							tde4.setCurveKeyPosition(curve,key,[pos[0],f])
				#multiply raw sqy keys with factor value...
				if count == 13:
					para	= tde4.getLDModelParameterName(model,i0)
					curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
					if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
						kl = tde4.getCurveKeyList(curve,0)
						for key in kl:
							pos = tde4.getCurveKeyPosition(curve,key)
							f = float(pos[1]) * float(v)
							tde4.setCurveKeyPosition(curve,key,[pos[0],f])


#build GUI...
window_title = "Patcha Focal-SqueezeX/Y Converter v1.4"
req	= tde4.createCustomRequester()

#add convert sqx to focal button...
tde4.addButtonWidget(req,"sqx_to_focal","Convert SqueezeX to FocalLength & SqueezeY",70,10)
tde4.setWidgetAttachModes(req,"sqx_to_focal","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sqx_to_focal",7,93,10,0)
#add convert sqy to focal button...
tde4.addButtonWidget(req,"sqy_to_focal","Convert SqueezeY to FocalLength & SqueezeX",70,10)
tde4.setWidgetAttachModes(req,"sqy_to_focal","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sqy_to_focal",7,93,40,0)
#add convert focal to sqx & sqy button...
tde4.addButtonWidget(req,"focal_to_sqxy","Convert FocalLength to SqueezeX & SqueezeY",70,10)
tde4.setWidgetAttachModes(req,"focal_to_sqxy","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"focal_to_sqxy",7,93,70,0)
#add separator...
tde4.addSeparatorWidget(req,"sep1")
tde4.setWidgetAttachModes(req,"sep1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sep1",2,98,90,0)
#add apply button widget...
tde4.addButtonWidget(req,"apply","Transform SqX/Y and Focal curves",70,10)
tde4.setWidgetAttachModes(req,"apply","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"apply",15,85,140,0)
#add factor slider widget...
tde4.addScaleWidget(req,"factor_slider","factor","DOUBLE",0.001,2.0,1.1)
tde4.setWidgetAttachModes(req,"factor_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"factor_slider",15,80,110,0)
#add factor text fiels widget...
tde4.addTextFieldWidget(req,"factor_text"," ","1.1")
tde4.setWidgetAttachModes(req,"factor_text","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"factor_text",82,98,110,0)
#callbacks...
tde4.setWidgetCallbackFunction(req,"sqx_to_focal","Convert")
tde4.setWidgetCallbackFunction(req,"sqy_to_focal","Convert")
tde4.setWidgetCallbackFunction(req,"focal_to_sqxy","Convert")
tde4.setWidgetCallbackFunction(req,"factor_slider","Convert")
tde4.setWidgetCallbackFunction(req,"factor_text","Convert")
tde4.setWidgetCallbackFunction(req,"apply","Convert")
tde4.postCustomRequesterAndContinue(req,window_title,410,170)
				
				
				
				
				
