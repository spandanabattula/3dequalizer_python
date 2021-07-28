# 3DE4.script.name: PGroup Constraint...
# 3DE4.script.version: v1.0.5
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui.button: Lineup Controls::PG Constraint, align-bottom-left,80,20
# 3DE4.script.gui.button: Orientation Controls::PG Constraint, align-bottom-left,70,20

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
			frame = i
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
			frame = i
			rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
			pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
			rot_pos_base = igl3d(rot_cpg,pos_cpg)
			rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
			pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)
			rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
			tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
			tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
			#tde4.setPGroupScale3D(pg,scale)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)


def convertToAngles(r3d):
	rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
	rx	= (rot[0])
	ry	= (rot[1])
	rz	= (rot[2])
	return(rx,ry,rz)

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

	#menu widget update
	if widget == "constraints_menu":
		menu_value = tde4.getWidgetValue(req,"constraints_menu")
		if menu_value == 1:
			tde4.setWidgetValue(req,"tx_toggle","1")
			tde4.setWidgetValue(req,"ty_toggle","1")
			tde4.setWidgetValue(req,"tz_toggle","1")
			tde4.setWidgetSensitiveFlag(req,"tx_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"ty_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"tz_toggle",1)
			tde4.setWidgetValue(req,"rx_toggle","0")
			tde4.setWidgetValue(req,"ry_toggle","0")
			tde4.setWidgetValue(req,"rz_toggle","0")
			tde4.setWidgetSensitiveFlag(req,"rx_toggle",0)
			tde4.setWidgetSensitiveFlag(req,"ry_toggle",0)
			tde4.setWidgetSensitiveFlag(req,"rz_toggle",0)

		if menu_value == 2:
			tde4.setWidgetValue(req,"tx_toggle","0")
			tde4.setWidgetValue(req,"ty_toggle","0")
			tde4.setWidgetValue(req,"tz_toggle","0")
			tde4.setWidgetSensitiveFlag(req,"tx_toggle",0)
			tde4.setWidgetSensitiveFlag(req,"ty_toggle",0)
			tde4.setWidgetSensitiveFlag(req,"tz_toggle",0)
			tde4.setWidgetValue(req,"rx_toggle","1")
			tde4.setWidgetValue(req,"ry_toggle","1")
			tde4.setWidgetValue(req,"rz_toggle","1")
			tde4.setWidgetSensitiveFlag(req,"rx_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"ry_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"rz_toggle",1)

		if menu_value == 3:
			tde4.setWidgetValue(req,"tx_toggle","1")
			tde4.setWidgetValue(req,"ty_toggle","1")
			tde4.setWidgetValue(req,"tz_toggle","1")
			tde4.setWidgetSensitiveFlag(req,"tx_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"ty_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"tz_toggle",1)
			tde4.setWidgetValue(req,"rx_toggle","1")
			tde4.setWidgetValue(req,"ry_toggle","1")
			tde4.setWidgetValue(req,"rz_toggle","1")
			tde4.setWidgetSensitiveFlag(req,"rx_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"ry_toggle",1)
			tde4.setWidgetSensitiveFlag(req,"rz_toggle",1)



	if widget == "constraint_btn":
		#get parent and child pg ids
		parent_pg_name_v = tde4.getWidgetValue(req,"parent_name_txt")	
		child_pg_name_v = tde4.getWidgetValue(req,"child_name_txt")
		#make sure both pgs picked
		if parent_pg_name_v != None and child_pg_name_v != None:
			for temp_pg in pg_list:
				if tde4.getPGroupName(temp_pg) == parent_pg_name_v:
					parent_pg = temp_pg
				if tde4.getPGroupName(temp_pg) == child_pg_name_v:
					child_pg = temp_pg	

			#bake buffered curves
			bakeBufferCurves(parent_pg)
			bakeBufferCurves(child_pg)

			#get calc enabled frame range
			start_frame = 1
			end_frame = frames
			if tde4.getCameraFrameRangeCalculationFlag(cam):
				start_frame, end_frame = tde4.getCameraCalculationRange(cam)
			offset_v = tde4.getWidgetValue(req,"offset_toggle")
			menu_value = tde4.getWidgetValue(req,"constraints_menu")

			if menu_value == 1 or (menu_value == 3 and offset_v == 0 and tde4.getWidgetValue(req,"rx_toggle")==0 and tde4.getWidgetValue(req,"ry_toggle")==0 and tde4.getWidgetValue(req,"rz_toggle")==0):
				#calc position delta on current frame
				current_frame = tde4.getCurrentFrame(cam)
				parent_pos3d = vec3d(tde4.getPGroupPosition3D(parent_pg,cam,current_frame))
				parent_rot3d = mat3d(tde4.getPGroupRotation3D(parent_pg,cam,current_frame))
				child_pos3d = vec3d(tde4.getPGroupPosition3D(child_pg,cam,current_frame))
				child_rot3d = mat3d(tde4.getPGroupRotation3D(child_pg,cam,current_frame))
				delta_pos3d = parent_pos3d - child_pos3d

				for frame in range(start_frame, end_frame+1):
					parent_pos3d = vec3d(tde4.getPGroupPosition3D(parent_pg,cam,frame))
					parent_rot3d = mat3d(tde4.getPGroupRotation3D(parent_pg,cam,frame))
					child_pos3d = vec3d(tde4.getPGroupPosition3D(child_pg,cam,frame))
					child_rot3d = mat3d(tde4.getPGroupRotation3D(child_pg,cam,frame))

					if offset_v == 0:
						new_pos3d = parent_pos3d

					if offset_v == 1:
						new_pos3d = parent_pos3d - delta_pos3d

					if tde4.getWidgetValue(req,"tx_toggle") == 0:
						new_pos3d[0] = child_pos3d[0]
					if tde4.getWidgetValue(req,"ty_toggle") == 0:
						new_pos3d[1] = child_pos3d[1]
					if tde4.getWidgetValue(req,"tz_toggle") == 0:
						new_pos3d[2] = child_pos3d[2]

					if tde4.getPGroupType(child_pg) == "OBJECT":
						pg_scale = float(tde4.getPGroupScale3D(child_pg))
						world_to_3de = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,child_rot3d.list(),list(new_pos3d),1.0,1)
						new_pos3d = world_to_3de[1]
						new_rot3d = world_to_3de[0]
					if tde4.getPGroupType(child_pg) == "CAMERA":
						new_pos3d = new_pos3d
						new_rot3d = child_rot3d.list()
					tde4.setPGroupPosition3D(child_pg,cam,frame,list(new_pos3d))
					tde4.setPGroupRotation3D(child_pg,cam,frame,new_rot3d)
					tde4.setPGroupScale3D(child_pg,tde4.getPGroupScale3D(child_pg))
				tde4.copyPGroupEditCurvesToFilteredCurves(child_pg,cam)



			if menu_value == 2:
				for frame in range(start_frame, end_frame+1):
					parent_pos3d = vec3d(tde4.getPGroupPosition3D(parent_pg,cam,frame))
					parent_rot3d = mat3d(tde4.getPGroupRotation3D(parent_pg,cam,frame))
					child_pos3d = vec3d(tde4.getPGroupPosition3D(child_pg,cam,frame))
					child_rot3d = mat3d(tde4.getPGroupRotation3D(child_pg,cam,frame))

					parent_rot3d = list(convertToAngles(parent_rot3d))
					child_rot3d = list(convertToAngles(child_rot3d))					

					if offset_v == 0:
						new_rot3d = parent_rot3d

					if offset_v == 1:
						parent_rot3d_current_frame = mat3d(tde4.getPGroupRotation3D(parent_pg,cam,frame))
						if frame < frames:
							parent_rot3d_next_frame = mat3d(tde4.getPGroupRotation3D(parent_pg,cam,frame+1))
						child_rot3d_current_frame = mat3d(tde4.getPGroupRotation3D(child_pg,cam,frame))

						rotation_delta = parent_rot3d_next_frame * parent_rot3d_current_frame.invert()
						new_rot3d = rotation_delta * child_rot3d_current_frame
						new_rot3d = list(convertToAngles(new_rot3d))

					if tde4.getWidgetValue(req,"rx_toggle") == 0:
						new_rot3d[0] = child_rot3d[0]
					if tde4.getWidgetValue(req,"ry_toggle") == 0:
						new_rot3d[1] = child_rot3d[1]	
					if tde4.getWidgetValue(req,"rz_toggle") == 0:
						new_rot3d[2] = child_rot3d[2]

					#print frame, math.degrees(new_rot3d[0]), math.degrees(new_rot3d[1]), math.degrees(new_rot3d[2])
					print frame, math.degrees(child_rot3d[0]), math.degrees(child_rot3d[1]), math.degrees(child_rot3d[2])

					new_rot3d = mat3d(rot3d(new_rot3d[0], new_rot3d[1], new_rot3d[2],VL_APPLY_ZXY))

					"""if offset_v == 0:
						if tde4.getPGroupType(child_pg) == "OBJECT":
							child_pg_scale = float(tde4.getPGroupScale3D(child_pg))
							world_to_3de = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,new_rot3d.list(),child_pos3d.list(),child_pg_scale,1)
							new_pos3d = world_to_3de[1]
							new_rot3d = world_to_3de[0]
						if tde4.getPGroupType(child_pg) == "CAMERA":
							new_pos3d = child_pos3d
							new_rot3d = new_rot3d.list()
						tde4.setPGroupPosition3D(child_pg,cam,frame,list(new_pos3d))
						tde4.setPGroupRotation3D(child_pg,cam,frame,new_rot3d)
						tde4.setPGroupScale3D(child_pg,tde4.getPGroupScale3D(child_pg))

					if offset_v == 1:
						if frame < frames:
							if tde4.getPGroupType(child_pg) == "OBJECT":
								child_pg_scale = float(tde4.getPGroupScale3D(child_pg))
								world_to_3de = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame+1,new_rot3d.list(),child_pos3d.list(),child_pg_scale,1)
								new_pos3d = world_to_3de[1]
								new_rot3d = world_to_3de[0]
							if tde4.getPGroupType(child_pg) == "CAMERA":
								new_pos3d = child_pos3d
								new_rot3d = new_rot3d.list()
							tde4.setPGroupPosition3D(child_pg,cam,frame,list(new_pos3d))
							tde4.setPGroupRotation3D(child_pg,cam,frame+1,new_rot3d)
							tde4.setPGroupScale3D(child_pg,tde4.getPGroupScale3D(child_pg))"""
				#tde4.copyPGroupEditCurvesToFilteredCurves(child_pg,cam)














			"""#update all objpgs current transformations
			for pg in tde4.getPGroupList(0):
				if tde4.getPGroupType(pg) == "OBJECT":
					bakeBufferCurves(pg)"""


		else:
			tde4.postQuestionRequester(window_title,"Error, please get parent and child pgroups.","Ok")




























































window_title = "Patcha PGroup Constraint Tool v1.0.5"
req = tde4.createCustomRequester()

#parent name textfield widget...
tde4.addTextFieldWidget(req,"parent_name_txt","Parent PG","")
tde4.setWidgetAttachModes(req,"parent_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_name_txt",16,73,15,0)
tde4.setWidgetSensitiveFlag(req,"parent_name_txt",0)

#parent get button widget...
tde4.addButtonWidget(req,"parent_get_btn","Get",70,10)
tde4.setWidgetAttachModes(req,"parent_get_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_get_btn",75,86,15,0)

#parent clear button widget...
tde4.addButtonWidget(req,"parent_clear_btn","Clear",70,10)
tde4.setWidgetAttachModes(req,"parent_clear_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"parent_clear_btn",88,98,15,0)

#child name textfield widget...
tde4.addTextFieldWidget(req,"child_name_txt","Child PG","")
tde4.setWidgetAttachModes(req,"child_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_name_txt",16,73,45,0)
tde4.setWidgetSensitiveFlag(req,"child_name_txt",0)

#child get button widget...
tde4.addButtonWidget(req,"child_get_btn","Get",70,10)
tde4.setWidgetAttachModes(req,"child_get_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_get_btn",75,86,45,0)

#child clear button widget...
tde4.addButtonWidget(req,"child_clear_btn","Clear",70,10)
tde4.setWidgetAttachModes(req,"child_clear_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"child_clear_btn",88,98,45,0)

#add constraints menu widget...
tde4.addOptionMenuWidget(req,"constraints_menu","Constraints","Point Constraint","Orient Constraint","Parent Constraint")
tde4.setWidgetAttachModes(req,"constraints_menu","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"constraints_menu",19,53,80,0)
tde4.setWidgetValue(req,"constraints_menu","3")

#offset toggle widget...
tde4.addToggleWidget(req,"offset_toggle","Maintain offset",1)
tde4.setWidgetAttachModes(req,"offset_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"offset_toggle",83,87,80,0)

"""
#translation label widget...
tde4.addLabelWidget(req,"translate_label","Translation Axes:","ALIGN_LABEL_LEFT")
tde4.setWidgetAttachModes(req,"translate_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"translate_label",13,39,100,0)

#rotation label widget...
tde4.addLabelWidget(req,"rotate_label","Rotation Axes:","ALIGN_LABEL_LEFT")
tde4.setWidgetAttachModes(req,"rotate_label","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rotate_label",68,94,100,0)
"""

#tx toggle widget...
tde4.addToggleWidget(req,"tx_toggle","TX",1)
tde4.setWidgetAttachModes(req,"tx_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"tx_toggle",10,14,115,0)

#ty toggle widget...
tde4.addToggleWidget(req,"ty_toggle","TY",1)
tde4.setWidgetAttachModes(req,"ty_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"ty_toggle",23,27,115,0)

#tz toggle widget...
tde4.addToggleWidget(req,"tz_toggle","TZ",1)
tde4.setWidgetAttachModes(req,"tz_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"tz_toggle",36,40,115,0)

#rx toggle widget...
tde4.addToggleWidget(req,"rx_toggle","RX",1)
tde4.setWidgetAttachModes(req,"rx_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rx_toggle",64,68,115,0)

#ry toggle widget...
tde4.addToggleWidget(req,"ry_toggle","RY",1)
tde4.setWidgetAttachModes(req,"ry_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"ry_toggle",77,81,115,0)

#rz toggle widget...
tde4.addToggleWidget(req,"rz_toggle","RZ",1)
tde4.setWidgetAttachModes(req,"rz_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rz_toggle",90,94,115,0)


#do constraint button widget...
tde4.addButtonWidget(req,"constraint_btn","Make Constraint",70,10)
tde4.setWidgetAttachModes(req,"constraint_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"constraint_btn",30,70,145,0)

#callbacks...
tde4.setWidgetCallbackFunction(req,"parent_get_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"child_get_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"parent_clear_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"child_clear_btn","mainCallback")
tde4.setWidgetCallbackFunction(req,"constraints_menu","mainCallback")
tde4.setWidgetCallbackFunction(req,"constraint_btn","mainCallback")






tde4.postCustomRequesterAndContinue(req,window_title,520,175)