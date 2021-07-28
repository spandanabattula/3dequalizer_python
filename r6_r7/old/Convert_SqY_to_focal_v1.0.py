#
# 3DE4.script.name:		Convert SqY to focal
#
# 3DE4.script.version:		v1.0
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment:
#
# Patcha Saheb(patchasaheb@gmail.com) / Michael Karp mckarp@aol.com

#pseudo code...

#pg = camera PGroup
#cam = camera
#frame =  current frame
#frameLength = last frame number
#(bake all non dynamic focal and distortion, to dynamic and linear Focus)
#SqX= list of SqX in curve
#SqY = list of SqY in curve
#zoom= list of focal lengths in curve
#yFirst = first frame of SqY
#delta = SqX/SqY list
#zoom = zoom * delta
#SqY = yFirst (static for all frames)

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
	focal_list = []
	sq_x_list = []
	sq_y_list = []
	delta_list = []
	new_focal_list = []

#filling lists...
	n	= tde4.getLDModelNoParameters(model)
	count = 0
#sqeeze_x data...
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
#sqeeze_y data...
		if count == 13:
			for f in range(1,frames+1):
				para	= tde4.getLDModelParameterName(model,i0)
				focal = tde4.getCameraFocalLength(cam,f) * 10.0
				focus = tde4.getCameraFocus(cam,f)
				if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
					v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
					sq_y_list.append(v)	
					#get first frame's sqeeze y value...					
					if f == 1:
						sqy	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
							
#focal data...
	for i in range(1,frames+1):
		focal = tde4.getCameraFocalLength(cam,i) * 10.0
		focal_list.append(focal)
		
#delta = sqx / sqy...
	for j in range(0,len(sq_x_list)):
		d =  sq_x_list[j] / sq_y_list[j]
		delta_list.append(d)
	
#new_focal  = old_focal(focal) * delta
	for k in range(0,len(focal_list)):
		n_f =  focal_list[k] * delta_list[k]
		new_focal_list.append(n_f)
		
#write back new focal values...
	for m in range(1,frames+1):
		tde4.setCameraFocalLength(cam,m,(new_focal_list[m-1]/10.0))
		tde4.filterPGroup(pg,cam)		

#make sqeeze y curve static...	
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
				tde4.createCurveKey(curve,[f,sqy])
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	




