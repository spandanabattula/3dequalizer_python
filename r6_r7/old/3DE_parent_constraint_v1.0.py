# 3DE4.script.name: Parent Constraint...
# 3DE4.script.version: v1.0
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui.button: Lineup Controls::Parent, align-bottom-left,80,20
# 3DE4.script.gui.button: Orientation Controls::Parent, align-bottom-left,70,20

# Patcha Saheb(patchasaheb@gmail.com)
# 12 June 2018(Montreal)

from vl_sdv import *
import math

def bakeBufferCurves(pg):
	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(cam)
	pg_type = tde4.getPGroupType(pg)
	currentFrame = tde4.getCurrentFrame(cam)
	if pg_type == "CAMERA":
		for i in range(1,frames+1):
			tde4.setCurrentFrame(cam,i)
			frame = tde4.getCurrentFrame(cam)	
			pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
			rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)
			#focal = tde4.getCameraFocalLength(cam,frame)
			tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
			tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
			tde4.setPGroupScale3D(pg,scale)
			#tde4.setCameraFocalLength(cam,frame,focal)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
	if pg_type == "OBJECT":
		for i_pg in tde4.getPGroupList():
			if tde4.getPGroupType(i_pg) == "CAMERA":
				id_cpg = i_pg
				break
		id_opg = pg		
		for i in range(1,frames+1):
			tde4.setCurrentFrame(cam,i)
			frame = tde4.getCurrentFrame(cam)
			rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
			pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
			rot_pos_base = igl3d(rot_cpg,pos_cpg)

			rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
			pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)

			rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
			tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
			tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
			tde4.setPGroupScale3D(pg,scale)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
	#return to parked frame
	tde4.setCurrentFrame(cam,currentFrame)


def convertToAngles(r3d):
	rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
	rx	= (rot[0])
	ry	= (rot[1])
	rz	= (rot[2])
	return(rx,ry,rz)


def closeReq(req,widget,action):
	tde4.unpostCustomRequester(req)


def mainCallback(req,widget,action):

	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(cam)
	pg_list = tde4.getPGroupList(0)



	#set parent pg name
	if widget == "parent_get_btn":
		#make sure parent and child are not same
		child_pg_name_v = tde4.getWidgetValue(req,"child_name_txt")
		parent_pg = tde4.getCurrentPGroup()
		parent_pg_name = tde4.getPGroupName(parent_pg)
		if parent_pg_name != child_pg_name_v:
			tde4.setWidgetValue(req,"parent_name_txt",str(parent_pg_name))
		else:
			tde4.postQuestionRequester(window_title,"      Error, Parent and Child can't be same.      ","Ok")
			#tde4.setWidgetValue(req,"parent_name_txt","")

	#set child pg name
	if widget == "child_get_btn":
		#make sure parent and child are not same
		parent_pg_name_v = tde4.getWidgetValue(req,"parent_name_txt")		
		child_pg = tde4.getCurrentPGroup()
		child_pg_name = tde4.getPGroupName(child_pg)
		if parent_pg_name_v != child_pg_name:
			tde4.setWidgetValue(req,"child_name_txt",str(child_pg_name))
		else:
			tde4.postQuestionRequester(window_title,"      Error, Parent and Child can't be same.      ","Ok")
			#tde4.setWidgetValue(req,"child_name_txt","")

	#clearing pg's name
	if widget == "parent_clear_btn":
		tde4.setWidgetValue(req,"parent_name_txt","")
	if widget == "child_clear_btn":
		tde4.setWidgetValue(req,"child_name_txt","")

	


	#if maintain offset is turned off
	if widget == "constraint_btn":



		#get parent and child pg ids
		parent_pg_name_v = tde4.getWidgetValue(req,"parent_name_txt")	
		child_pg_name_v = tde4.getWidgetValue(req,"child_name_txt")
		for temp_pg in pg_list:
			if tde4.getPGroupName(temp_pg) == parent_pg_name_v:
				parent_pg = temp_pg
			if tde4.getPGroupName(temp_pg) == child_pg_name_v:
				child_pg = temp_pg	

		bakeBufferCurves(parent_pg)
		bakeBufferCurves(child_pg)


		offset_v = tde4.getWidgetValue(req,"offset_toggle")
		if offset_v == 0:
			for frame in range(1,frames+1):
				parent_pos3d = tde4.getPGroupPosition3D(parent_pg,cam,frame)
				parent_rot3d = tde4.getPGroupRotation3D(parent_pg,cam,frame)
				child_pos3d = tde4.getPGroupPosition3D(child_pg,cam,frame)
				child_rot3d = tde4.getPGroupRotation3D(child_pg,cam,frame)

				if tde4.getWidgetValue(req,"tx_toggle") == 0:
					parent_pos3d[0] = child_pos3d[0]
				if tde4.getWidgetValue(req,"ty_toggle") == 0:
					parent_pos3d[1] = child_pos3d[1]
				if tde4.getWidgetValue(req,"tz_toggle") == 0:
					parent_pos3d[2] = child_pos3d[2]

				parent_rot3d = list(convertToAngles(parent_rot3d))
				child_rot3d = list(convertToAngles(child_rot3d))

				if tde4.getWidgetValue(req,"rx_toggle") == 0:
					parent_rot3d[0] = child_rot3d[0]

				if tde4.getWidgetValue(req,"ry_toggle") == 0:
					parent_rot3d[1] = child_rot3d[1]

				if tde4.getWidgetValue(req,"rz_toggle") == 0:
					parent_rot3d[2] = child_rot3d[2]

				parent_rot3d = mat3d(rot3d(parent_rot3d[0],parent_rot3d[1],parent_rot3d[2],VL_APPLY_ZXY))

				if tde4.getPGroupType(child_pg) == "OBJECT":
					world_to_3de = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,parent_rot3d.list(),parent_pos3d,1.0,1)
					parent_pos3d = world_to_3de[1]
					parent_rot3d = world_to_3de[0]
				if tde4.getPGroupType(child_pg) == "CAMERA":
					parent_pos3d = parent_pos3d
					parent_rot3d = parent_rot3d
				tde4.setPGroupPosition3D(child_pg,cam,frame,parent_pos3d)
				tde4.setPGroupRotation3D(child_pg,cam,frame,parent_rot3d)
				tde4.setPGroupScale3D(child_pg,tde4.getPGroupScale3D(child_pg))
				tde4.copyPGroupEditCurvesToFilteredCurves(child_pg,cam)
			tde4.updateGUI()				

	#if maintain offset is turned on
		if offset_v == 1:

			bakeBufferCurves(parent_pg)
			bakeBufferCurves(child_pg)

			#translations
			#calc delta on current frame
			parent_pos3d = vec3d(tde4.getPGroupPosition3D(parent_pg,cam,tde4.getCurrentFrame(cam)))
			parent_rot3d = tde4.getPGroupRotation3D(parent_pg,cam,tde4.getCurrentFrame(cam))
			child_pos3d = vec3d(tde4.getPGroupPosition3D(child_pg,cam,tde4.getCurrentFrame(cam)))
			child_rot3d = tde4.getPGroupRotation3D(child_pg,cam,tde4.getCurrentFrame(cam))
			delta_pos3d = parent_pos3d - child_pos3d

			#subtract delta from parent
			for frame in range(1,frames+1):
				parent_pos3d = vec3d(tde4.getPGroupPosition3D(parent_pg,cam,frame))
				parent_rot3d = tde4.getPGroupRotation3D(parent_pg,cam,frame)
				child_pos3d = vec3d(tde4.getPGroupPosition3D(child_pg,cam,frame))
				child_rot3d = tde4.getPGroupRotation3D(child_pg,cam,frame)

				parent_pos3d[0] = parent_pos3d[0] - delta_pos3d[0]
				parent_pos3d[1] = parent_pos3d[1] - delta_pos3d[1]
				parent_pos3d[2] = parent_pos3d[2] - delta_pos3d[2]

				if tde4.getWidgetValue(req,"tx_toggle") == 0:
					parent_pos3d[0] = child_pos3d[0]
				if tde4.getWidgetValue(req,"ty_toggle") == 0:
					parent_pos3d[1] = child_pos3d[1]
				if tde4.getWidgetValue(req,"tz_toggle") == 0:
					parent_pos3d[2] = child_pos3d[2]

				if tde4.getPGroupType(child_pg) == "OBJECT":
					world_to_3de = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,child_rot3d,list(parent_pos3d),1.0,1)
					parent_pos3d = world_to_3de[1]
					parent_rot3d = world_to_3de[0]
				if tde4.getPGroupType(child_pg) == "CAMERA":
					parent_pos3d = parent_pos3d
					parent_rot3d = child_rot3d
				tde4.setPGroupPosition3D(child_pg,cam,frame,list(parent_pos3d))
				tde4.setPGroupRotation3D(child_pg,cam,frame,parent_rot3d)
				tde4.setPGroupScale3D(child_pg,tde4.getPGroupScale3D(child_pg))
			tde4.copyPGroupEditCurvesToFilteredCurves(child_pg,cam)

			#rotations
			current_frame = tde4.getCurrentFrame(cam)
			for frame in range(1,frames+1):
				parent_pos3d = vec3d(tde4.getPGroupPosition3D(parent_pg,cam,frame))
				parent_rot3d = tde4.getPGroupRotation3D(parent_pg,cam,frame)
				child_pos3d = vec3d(tde4.getPGroupPosition3D(child_pg,cam,frame))
				child_rot3d = tde4.getPGroupRotation3D(child_pg,cam,frame)

				parent_rot3d_values = list(convertToAngles(parent_rot3d))
				#child_rot3d = list(convertToAngles(child_rot3d))

				rx = float(parent_rot3d_values[0])
				ry = float(parent_rot3d_values[1])
				rz = float(parent_rot3d_values[2])

				rx_axis = vec3d(1,0,0)
				ry_axis = vec3d(0,1,0)
				rz_axis = vec3d(0,0,1)

				pivot = parent_pos3d

				#child_pos3d = vec3d(tde4.getPGroupPosition3D(child_pg,cam,frame))
				new_pos3d = rot3d(rx,ry,rz,VL_APPLY_ZXY) * (child_pos3d - pivot) + pivot


				new_rot3d_x = mat3d(rot3d(rx_axis,math.radians(rx)))
				new_rot3d_y = mat3d(rot3d(ry_axis,math.radians(ry)))
				new_rot3d_z = mat3d(rot3d(rz_axis,math.radians(rz)))


				#child_rot3d = tde4.getPGroupRotation3D(child_pg,cam,frame)
				new_rot3d = new_rot3d_z * new_rot3d_y * new_rot3d_x * mat3d(parent_rot3d)

				if tde4.getPGroupType(child_pg) == "OBJECT":
					world_to_3de = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,new_rot3d.list(),list(new_pos3d),1.0,1)
					new_pos3d = world_to_3de[1]
					new_rot3d = world_to_3de[0]
				if tde4.getPGroupType(child_pg) == "CAMERA":
					new_pos3d = new_pos3d
					new_rot3d = new_rot3d
				tde4.setPGroupPosition3D(child_pg,cam,frame,list(new_pos3d))
				tde4.setPGroupRotation3D(child_pg,cam,frame,new_rot3d)
				tde4.setPGroupScale3D(child_pg,tde4.getPGroupScale3D(child_pg))
			tde4.copyPGroupEditCurvesToFilteredCurves(child_pg,cam)
			tde4.updateGUI()














































window_title = "Patcha Parent Constraint Tool v1.0"
req = tde4.createCustomRequester()

#offset toggle widget...
tde4.addToggleWidget(req,"offset_toggle","Maintain offset",1)
tde4.setWidgetAttachModes(req,"offset_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"offset_toggle",32,37,10,0)

#parent name textfield widget...
tde4.addTextFieldWidget(req,"parent_name_txt","Parent","")
tde4.setWidgetAttachModes(req,"parent_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_name_txt",12,73,40,0)
tde4.setWidgetSensitiveFlag(req,"parent_name_txt",0)

#parent get button widget...
tde4.addButtonWidget(req,"parent_get_btn","Get",70,10)
tde4.setWidgetAttachModes(req,"parent_get_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_get_btn",75,86,40,0)

#parent clear button widget...
tde4.addButtonWidget(req,"parent_clear_btn","Clear",70,10)
tde4.setWidgetAttachModes(req,"parent_clear_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_clear_btn",88,98,40,0)

#child name textfield widget...
tde4.addTextFieldWidget(req,"child_name_txt","Child","")
tde4.setWidgetAttachModes(req,"child_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_name_txt",12,73,70,0)
tde4.setWidgetSensitiveFlag(req,"child_name_txt",0)

#child get button widget...
tde4.addButtonWidget(req,"child_get_btn","Get",70,10)
tde4.setWidgetAttachModes(req,"child_get_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_get_btn",75,86,70,0)

#child clear button widget...
tde4.addButtonWidget(req,"child_clear_btn","Clear",70,10)
tde4.setWidgetAttachModes(req,"child_clear_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_clear_btn",88,98,70,0)

#translate label widget...
tde4.addLabelWidget(req,"translate_label","Translation Axes:","ALIGN_LABEL_LEFT")
tde4.setWidgetAttachModes(req,"translate_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"translate_label",14,40,100,0)

#point constraint label widget...
tde4.addLabelWidget(req,"point_constraint_label","(Point Constraint)","ALIGN_LABEL_LEFT")
tde4.setWidgetAttachModes(req,"point_constraint_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"point_constraint_label",13,40,120,0)

#rotate label widget...
tde4.addLabelWidget(req,"rotate_label","Rotation Axes:","ALIGN_LABEL_LEFT")
tde4.setWidgetAttachModes(req,"rotate_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rotate_label",69,95,100,0)

#orient constraint label widget...
tde4.addLabelWidget(req,"orient_constraint_label","(Orient Constraint)","ALIGN_LABEL_LEFT")
tde4.setWidgetAttachModes(req,"orient_constraint_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"orient_constraint_label",66,98,120,0)

#tx toggle widget...
tde4.addToggleWidget(req,"tx_toggle","TX",1)
tde4.setWidgetAttachModes(req,"tx_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"tx_toggle",10,15,145,0)

#ty toggle widget...
tde4.addToggleWidget(req,"ty_toggle","TY",1)
tde4.setWidgetAttachModes(req,"ty_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"ty_toggle",23,28,145,0)

#tz toggle widget...
tde4.addToggleWidget(req,"tz_toggle","TZ",1)
tde4.setWidgetAttachModes(req,"tz_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"tz_toggle",36,41,145,0)

#rx toggle widget...
tde4.addToggleWidget(req,"rx_toggle","RX",1)
tde4.setWidgetAttachModes(req,"rx_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rx_toggle",64,69,145,0)

#ry toggle widget...
tde4.addToggleWidget(req,"ry_toggle","RY",1)
tde4.setWidgetAttachModes(req,"ry_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"ry_toggle",77,82,145,0)

#rz toggle widget...
tde4.addToggleWidget(req,"rz_toggle","RZ",1)
tde4.setWidgetAttachModes(req,"rz_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rz_toggle",90,95,145,0)

#constraint button widget...
tde4.addButtonWidget(req,"constraint_btn","Parent Constraint",70,10)
tde4.setWidgetAttachModes(req,"constraint_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"constraint_btn",50,80,180,0)

#close button widget...
tde4.addButtonWidget(req,"close_btn","Close",70,10)
tde4.setWidgetAttachModes(req,"close_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"close_btn",83,98,180,0)


#callbacks...
tde4.setWidgetCallbackFunction(req,"close_btn","closeReq")
tde4.setWidgetCallbackFunction(req,"parent_get_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"child_get_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"parent_clear_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"child_clear_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"constraint_btn","mainCallback")






tde4.postCustomRequesterAndContinue(req,window_title,520,210)