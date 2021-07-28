#
# 3DE4.script.name:		Convert SqX to focal
#
# 3DE4.script.version:		v1.2
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: Takes animated anamorphic SqX, sets it to a static value of 1 and then bakes animated focal and SqY to compensate.
#
# Patcha Saheb(patchasaheb@gmail.com) / Michael Karp (mckarp@aol.com)

#pseudo code...

#Convert sqx to focal
#Take reciprocal of SqX
#Multiply reciprocal of SqX  * (SqY)
#Multiply reciprocal of SqX  * (SqX) [sets to 1]
#Multiply reciprocal of SqX  * (Focal)


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
	new_sq_y_list = []
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
					#reciprocal of sqeeze y
					sq_x_list.append(1/v)
#sqeeze_y data...
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
		
#multiply reciprocal of sqeeze y with sqx and focal...
	for j in range(0,len(sq_y_list)):
		new_sq_y = sq_x_list[j] * sq_y_list[j]
		new_focal = sq_x_list[j] * focal_list[j]
		new_sq_y_list.append(new_sq_y)
		new_focal_list.append(new_focal)
		
#write back new focal values...
	for m in range(1,frames+1):
		tde4.setCameraFocalLengthMode(cam,"FOCAL_DYNAMIC")
		tde4.setCameraFocalLength(cam,m,(new_focal_list[m-1]/10.0))
		#tde4.filterPGroup(pg,cam)	
			
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
tde4.updateGUI()


