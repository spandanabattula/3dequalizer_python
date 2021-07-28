#
# 3DE4.script.name:		Convert SqX to focal
#
# 3DE4.script.version:		v1.5
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: Takes animated anamorphic SqX, sets it to a static value of 1 and then bakes animated focal and SqY to compensate.
#
# Patcha Saheb(patchasaheb@gmail.com) / Michael Karp (mckarp@aol.com)

#pseudo code...

#Convert sqx to focal
#Multiply reciprocal of raw SqX  * (raw SqY) ---> gives new SqY
#Multiply reciprocal of raw SqX  * (raw SqX) [sets to 1] ---> gived new SqX
#Multiply reciprocal of instantaneous SqX  * (Focal) ---> gives new Focal


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
	baked_sq_x_keys_list = []
	baked_sq_y_keys_list = []
	new_sq_y_list = []
	new_focal_list = []		
	
#filling lists...
	n	= tde4.getLDModelNoParameters(model)
	count = 0
	#get squeeze_x curve and get instantaneous sqx keys list...
	for i0 in range(n):
		count = count + 1
		if count == 12:
			para	= tde4.getLDModelParameterName(model,i0)
			sq_x_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
			for f in range(1,frames+1):	
				para	= tde4.getLDModelParameterName(model,i0)		
				focal = tde4.getCameraFocalLength(cam,f) * 10.0
				focus = tde4.getCameraFocus(cam,f)
				if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
					v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
					baked_sq_x_keys_list.append(v)


	#get squeeze_y curve and get instantaneous sqy keys list......
	count = 0	
	for i0 in range(n):
		count = count + 1
		if count == 13:
			para	= tde4.getLDModelParameterName(model,i0)
			sq_y_curve = tde4.getLensLDAdjustableParameterCurve(lens,para)
			for f in range(1,frames+1):	
				para	= tde4.getLDModelParameterName(model,i0)		
				focal = tde4.getCameraFocalLength(cam,f) * 10.0
				focus = tde4.getCameraFocus(cam,f)
				if tde4.getLDModelParameterType(model,para)=="LDP_DOUBLE_ADJUST":
					v	= tde4.getLensLDAdjustableParameter(lens,para,focal,focus)
					baked_sq_y_keys_list.append(v)	
							
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
	
	#get focal data...
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
	
	#sqx curve existing keys data...
	kl = tde4.getCurveKeyList(sq_x_curve,0)
	for k in kl:
		key = tde4.getCurveKeyPosition(sq_x_curve,k)
		raw_sq_x_ext_keys_x_list.append(key[0])
	#sqy curve existing keys data...
	kl = tde4.getCurveKeyList(sq_y_curve,0)
	for k in kl:
		key = tde4.getCurveKeyPosition(sq_y_curve,k)
		raw_sq_y_ext_keys_x_list.append(key[0])

	#integer pickups...
	tde4.postProgressRequesterAndContinue("test","Pickingup keys...Step 1/5",int(raw_sq_x_ext_keys_x_list[-1]),"Cancel")
	null = 0	
	count = 0	
	for i in range(len(raw_sq_x_ext_keys_x_list)):
		null = null + count
		count = count + 1
		if count != len(raw_sq_x_ext_keys_x_list):
			#k = count
			for j in range(int(raw_sq_x_ext_keys_x_list[i]),int(raw_sq_x_ext_keys_x_list[i+1])):
				y_pos = tde4.evaluateCurve(sq_x_curve,j)
				key = tde4.createCurveKey(sq_x_curve,[j,y_pos])
				tde4.setCurveKeyMode(sq_x_curve,key,"LINEAR")
				y_pos = tde4.evaluateCurve(sq_y_curve,j)
				key = tde4.createCurveKey(sq_y_curve,[j,y_pos])
				tde4.setCurveKeyMode(sq_y_curve,key,"LINEAR")
				null = null + 1
				if null % 10 == 0:
					tde4.updateProgressRequester(null,"Pickingup keys...Step 1/5")
	tde4.unpostProgressRequester()
					
	

	
	#if widget == "sqx_to_focal"			
	#multiply raw sqx with raw sqy...
	sq_x_keys_list = tde4.getCurveKeyList(sq_x_curve,0)
	sq_y_keys_list = tde4.getCurveKeyList(sq_y_curve,0)
	tde4.postProgressRequesterAndContinue("test","Calculating keys data...Step 2/5",len(sq_y_keys_list),"Cancel")
	null = 1 
	for i in sq_x_keys_list:
		if null % 10 == 0:
			tde4.updateProgressRequester(null,"Calculating keys data...Step 2/5")
		sq_x_key = tde4.getCurveKeyPosition(sq_x_curve,i)
		sq_y_key = tde4.evaluateCurve(sq_y_curve,sq_x_key[0])
		new_sq_y = (1/sq_x_key[1]) * sq_y_key
		new_sq_y_list.append(new_sq_y)
		null = null + 1
	tde4.unpostProgressRequester()	

	#write new sqy values...
	tde4.postProgressRequesterAndContinue("test","Writing new Squeeze Y keys...Step 3/5",len(sq_y_keys_list),"Cancel")
	count = 0
	null = 1
	for i in sq_y_keys_list:
		key = tde4.getCurveKeyPosition(sq_y_curve,i)
		tde4.setCurveKeyPosition(sq_y_curve,i,[key[0],new_sq_y_list[count]])
		count = count + 1
		if null % 10 == 0:
			tde4.updateProgressRequester(null,"Writing new Squeeze Y keys...Step 3/5")	
		null = null + 1		
	tde4.unpostProgressRequester()

	#set sqx to 1...
	tde4.postProgressRequesterAndContinue("test","Writing new Squeeze X keys...Step 4/5",len(sq_x_keys_list),"Cancel")
	null = 1
	for i in sq_x_keys_list:
		key = tde4.getCurveKeyPosition(sq_x_curve,i)
		tde4.setCurveKeyPosition(sq_x_curve,i,[key[0],1])
		if null % 10 == 0:
			tde4.updateProgressRequester(null,"Writing new Squeeze X keys...Step 4/5")
		null = null + 1
	tde4.unpostProgressRequester()

	#multiply instantaneous reciprocal of sqx with focal...
	tde4.postProgressRequesterAndContinue("test","Writing new Focal keys...Step 5/5",len(baked_sq_x_keys_list),"Cancel")
	null = 1
	for i in range(len(baked_sq_x_keys_list)):
		new_focal = (1/baked_sq_x_keys_list[i]) * focal_list[i]
		#new_focal_list.append(new_focal)
		tde4.setCameraFocalLengthMode(cam,"FOCAL_DYNAMIC")
		tde4.setCameraFocalLength(cam,i+1,(new_focal/10.0))
		if null % 10 == 0:
			tde4.updateProgressRequester(null,"Writing new Focal keys...Step 5/5")
		null = null + 1
	tde4.unpostProgressRequester()
