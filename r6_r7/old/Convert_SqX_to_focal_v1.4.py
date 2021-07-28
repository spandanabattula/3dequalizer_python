#
# 3DE4.script.name:		Convert SqX to focal
#
# 3DE4.script.version:		v1.4
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: Takes animated anamorphic SqX, sets it to a static value of 1 and then bakes animated focal and SqY to compensate.
#
# Patcha Saheb(patchasaheb@gmail.com) / Michael Karp (mckarp@aol.com)

#pseudo code...

#Convert sqx to focal
#Take reciprocal of raw SqX
#Multiply reciprocal of raw SqX  * (raw SqY)
#Multiply reciprocal of raw SqX  * (raw SqX) [sets to 1]
#Multiply reciprocal of baked SqX  * (Focal)


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
	raw_sq_x_ext_keys_x_list = []
	raw_sq_y_ext_keys_x_list = []

#filling lists...
	n	= tde4.getLDModelNoParameters(model)
	count = 0
	#get squeeze_x curve...
	for i0 in range(n):
		count = count + 1
		if count == 12:
			para	= tde4.getLDModelParameterName(model,i0)
			sq_x_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
	#get squeeze_y cruve...
	count = 0	
	for i0 in range(n):
		count = count + 1
		if count == 13:
			para	= tde4.getLDModelParameterName(model,i0)
			sq_y_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
	#get raw sqx existing keys...		
	kl = tde4.getCurveKeyList(sq_x_curve,0)
	for k in kl:
		key = tde4.getCurveKeyPosition(sq_x_curve,k)
		raw_sq_x_ext_keys_x_list.append(key[0])
	#get raw sqy existing keys...		
	kl = tde4.getCurveKeyList(sq_y_curve,0)
	for k in kl:
		key = tde4.getCurveKeyPosition(sq_y_curve,k)
		raw_sq_y_ext_keys_x_list.append(key[0])
	
	#focal data...
	for i in range(1,frames+1):
		focal = tde4.getCameraFocalLength(cam,i) * 10.0
		focal_list.append(focal)

	#pickups on sqy curve...
	for j in raw_sq_x_ext_keys_x_list:
		k = tde4.evaluateCurve(sq_y_curve,j)
		tde4.createCurveKey(sq_y_curve,[j,k])
	#pickups on sqx curve...
	for j in raw_sq_y_ext_keys_x_list:
		k = tde4.evaluateCurve(sq_x_curve,j)
		tde4.createCurveKey(sq_x_curve,[j,k])
	
	#pickup in between integer keys on sqx & sqy curves...
	##update raw sqx & raw sqy keys data...
	###remove previous keys data to update new existing keys data...
	raw_sq_x_ext_keys_x_list = []
	raw_sq_y_ext_keys_x_list = []
	
	###sqx curve existing keys data...
	kl = tde4.getCurveKeyList(sq_x_curve,0)
	for k in kl:
		key = tde4.getCurveKeyPosition(sq_x_curve,k)
		raw_sq_x_ext_keys_x_list.append(key[0])
	#sqy curve existing keys data...
	kl = tde4.getCurveKeyList(sq_y_curve,0)
	for k in kl:
		key = tde4.getCurveKeyPosition(sq_y_curve,k)
		raw_sq_y_ext_keys_x_list.append(key[0])
	
	count = 0	
	for i in range(len(raw_sq_x_ext_keys_x_list)):
		count = count + 1
		if count != len(raw_sq_x_ext_keys_x_list):
			#print int(raw_sq_x_ext_keys_x_list[i])
			#print int(raw_sq_x_ext_keys_x_list[i+1])
			#print " "
			for j in range(int(raw_sq_x_ext_keys_x_list[i]),int(raw_sq_x_ext_keys_x_list[i+1])):
				y_pos = tde4.evaluateCurve(sq_x_curve,j)
				key = tde4.createCurveKey(sq_x_curve,[j,y_pos])
				tde4.setCurveKeyMode(sq_x_curve,key,"LINEAR")
				y_pos = tde4.evaluateCurve(sq_y_curve,j)
				key = tde4.createCurveKey(sq_y_curve,[j,y_pos])
				tde4.setCurveKeyMode(sq_y_curve,key,"LINEAR")



		
		
		
		
		
		
"""	#multiply reciprocal of sqeeze y with sqx and focal...
	for j in range(0,len(raw_sq_x_list)):
		new_sq_y = raw_sq_x_list[j] * raw_sq_y_list[j]
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
				tde4.setCurveKeyMode(curve,k,"LINEAR")"""				



