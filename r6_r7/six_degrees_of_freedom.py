# Patcha Saheb(patchasaheb@gmail.com)
# April 24 2017.
# Bangalore - India.

from vl_sdv import*

def convertToAngles(r3d):
	rot = rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
	rx = (rot[0]*180.0)/3.141592654
	ry = (rot[1]*180.0)/3.141592654
	rz = (rot[2]*180.0)/3.141592654
	return(rx,ry,rz)

def Get_PGroup(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	pg_name = tde4.getPGroupName(pg)
	tde4.setWidgetValue(req,"pgroup",str(pg_name))
	Update_Every_Frame(req)

def Update_Every_Frame(req):
	v = tde4.getWidgetValue(req,"pgroup")	
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pg_list = tde4.getPGroupList(0)
	for pg in pg_list:
		pg_name = tde4.getPGroupName(pg)
		if str(v) == str(pg_name):
			break

	p3d = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
	r3d = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))

	tde4.setWidgetValue(req,"pos_x",str(p3d[0]))
	tde4.setWidgetValue(req,"pos_y",str(p3d[1]))
	tde4.setWidgetValue(req,"pos_z",str(p3d[2]))	

	tde4.setWidgetValue(req,"rot_x",str(convertToAngles(r3d)[0]))
	tde4.setWidgetValue(req,"rot_y",str(convertToAngles(r3d)[1]))
	tde4.setWidgetValue(req,"rot_z",str(convertToAngles(r3d)[2]))

def Set_Pose(req,widget,action):
	v = tde4.getWidgetValue(req,"pgroup")	
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pg_list = tde4.getPGroupList(0)
	for pg in pg_list:
		pg_name = tde4.getPGroupName(pg)
		if str(v) == str(pg_name):
			break
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)

	pos_x = float(tde4.getWidgetValue(req,"pos_x"))
	pos_y = float(tde4.getWidgetValue(req,"pos_y"))
	pos_z = float(tde4.getWidgetValue(req,"pos_z"))
	rot_x = float(tde4.getWidgetValue(req,"rot_x"))
	rot_y = float(tde4.getWidgetValue(req,"rot_y"))
	rot_z = float(tde4.getWidgetValue(req,"rot_z"))

	rot_x = (rot_x*3.141592654)/180.0
	rot_y = (rot_y*3.141592654)/180.0
	rot_z = (rot_z*3.141592654)/180.0
	r3d = mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))

	postfilter_mode = tde4.getPGroupPostfilterMode(pg)
	pg_scale = tde4.getPGroupScale3D(pg)	

	pg_type = tde4.getPGroupType(pg)
	if pg_type == "CAMERA":
		tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,pos_y,pos_z])
		tde4.setPGroupRotation3D(pg,cam,frame,r3d.list())
	if pg_type == "OBJECT":
		local_values = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,r3d.list(),[pos_x,pos_y,pos_z],1.0,0)
		tde4.setPGroupPosition3D(pg,cam,frame,local_values[1])
		tde4.setPGroupRotation3D(pg,cam,frame,local_values[0])
	tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
	tde4.filterPGroup(pg,cam)
	tde4.setPGroupScale3D(pg,pg_scale)
	tde4.setPGroupPostfilterMode(pg,postfilter_mode)
	tde4.updateGUI()

window_title = "Patcha Unlocked Camera/Object Channelbox v1.0"
req = tde4.createCustomRequester()

#pgroup text field widget...
tde4.addTextFieldWidget(req,"pgroup","PGroup")
tde4.setWidgetAttachModes(req,"pgroup","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pgroup",17,75,10,0)
tde4.setWidgetSensitiveFlag(req,"pgroup",0)

#get pgroup button widget...
tde4.addButtonWidget(req,"get","Get",70,10)
tde4.setWidgetAttachModes(req,"get","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"get",80,96,10,0)

#pos x widget...
tde4.addTextFieldWidget(req,"pos_x","Pos")
tde4.setWidgetAttachModes(req,"pos_x","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pos_x",17,42,50,0)

#pos y widget...
tde4.addTextFieldWidget(req,"pos_y","")
tde4.setWidgetAttachModes(req,"pos_y","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pos_y",45,70,50,0)

#pos z widget...
tde4.addTextFieldWidget(req,"pos_z","")
tde4.setWidgetAttachModes(req,"pos_z","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pos_z",73,98,50,0)

#rot x widget...
tde4.addTextFieldWidget(req,"rot_x","Rot")
tde4.setWidgetAttachModes(req,"rot_x","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rot_x",17,42,90,0)

#rot y widget...
tde4.addTextFieldWidget(req,"rot_y","")
tde4.setWidgetAttachModes(req,"rot_y","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rot_y",45,70,90,0)

#rot z widget...
tde4.addTextFieldWidget(req,"rot_z","")
tde4.setWidgetAttachModes(req,"rot_z","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rot_z",73,98,90,0)


pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
pg_name = tde4.getPGroupName(pg)
tde4.setWidgetValue(req,"pgroup",str(pg_name))

#Callbacks...
tde4.setWidgetCallbackFunction(req,"get","Get_PGroup")
tde4.setWidgetCallbackFunction(req,"pos_x","Set_Pose")
tde4.setWidgetCallbackFunction(req,"pos_y","Set_Pose")
tde4.setWidgetCallbackFunction(req,"pos_z","Set_Pose")
tde4.setWidgetCallbackFunction(req,"rot_x","Set_Pose")
tde4.setWidgetCallbackFunction(req,"rot_y","Set_Pose")
tde4.setWidgetCallbackFunction(req,"rot_z","Set_Pose")




tde4.postCustomRequesterAndContinue(req,window_title,400,130,"Update_Every_Frame")
