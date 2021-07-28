# 3DE4.script.name: Zero out Camera PG rotations...
# 3DE4.script.version: v1.0
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.gui:	Orientation Controls::Edit
# 3DE4.script.gui.button: Lineup Controls::Zero CamRot, align-bottom-left,80,20
# 3DE4.script.gui.button: Orientation Controls::Zero CamRot, align-bottom-left,70,20
# 3DE4.script.comment:	Temporarily bakes the current camera rotations to look down the Z axis, to avoid rotation channel "cross talk", when using LSF object tracks

# Patcha Saheb(patchasaheb@gmail.com)
# 15 August 2018(Montreal)

from vl_sdv import*

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

def storeMainCallback(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	pg_list = tde4.getPGroupList(0)
	pg_type = tde4.getPGroupType(pg)
	cam_list = tde4.getCameraList(0)

	#set camera, pg names and set status
	if widget == "pg_get_btn":
		if pg_type == "CAMERA":
			camera_name = tde4.getCameraName(cam)
			pg_name = tde4.getPGroupName(pg)
			tde4.setWidgetValue(req,"pg_name_txt",str(camera_name + "|" + pg_name))
			try:
				for temp_pg in pg_list:
					if tde4.getPGroupName(temp_pg) == str("store_" + camera_name):
						tde4.setWidgetValue(req,"status_txt","Stored")
						tde4.setWidgetFGColor(req,"status_txt",0.0,1.0,0.0)
					else:
						tde4.setWidgetValue(req,"status_txt","Not stored")
						tde4.setWidgetFGColor(req,"status_txt",1.0,0.0,0.0)
			except:
				pass
		else:
			tde4.postQuestionRequester(window_title,"Error, please select camera pgroup","Ok")
			tde4.setWidgetValue(req,"pg_name_txt","")
			tde4.setWidgetValue(req,"status_txt","")
			tde4.setWidgetFGColor(req,"status_txt",1.0,1.0,1.0)

	if widget == "store_btn" or widget == "restore_btn":
		#get camera and pg names
		name_v = tde4.getWidgetValue(req,"pg_name_txt")
		if name_v != None:
			name_v = name_v.split("|")
			cam_name, pg_name = name_v

			#get pg id
			for cpg_id in pg_list:
				p_name = tde4.getPGroupName(cpg_id)
				if p_name == pg_name:
					break

			#get camera id
			for cam_id in cam_list:
				c_name = tde4.getCameraName(cam_id)
				if c_name == cam_name:
					break

			#get camera no of frames
			frames = tde4.getCameraNoFrames(cam_id)

			if widget == "store_btn":
				#if objpg exists then delete it
				try:
					for temp_pg in pg_list:
						if tde4.getPGroupName(temp_pg) == str("store_" + cam_name):
							tde4.deletePGroup(temp_pg)
				except:
					pass

				#create new objpg and disable it
				obj_pg_id = tde4.createPGroup("OBJECT")
				obj_pg_name = tde4.setPGroupName(obj_pg_id,str("store_" + cam_name))
				tde4.setPGroupEnabledFlag(obj_pg_id,0)

				#set status as stored
				tde4.setWidgetValue(req,"status_txt","Stored")
				tde4.setWidgetFGColor(req,"status_txt",0.0,1.0,0.0)

				#bake buffer curves
				bakeBufferCurves(cpg_id)

				#copy cpg pos and rot values to a list
				pos3d_list = []
				rot3d_list = []
				for frame in range(1,frames+1):
					#get cpg pos and rot values
					pos3d = vec3d(tde4.getPGroupPosition3D(cpg_id,cam_id,frame))
					rot3d = mat3d(tde4.getPGroupRotation3D(cpg_id,cam_id,frame))
					pos3d_list.append(pos3d)
					rot3d_list.append(rot3d)

				#zero out camera rotations
				for frame in range(1,frames+1):
					x_axis = [1.0,0.0,0.0]
					y_axis = [0.0,1.0,0.0]
					z_axis = [0.0,0.0,1.0]
					zero_matrix = mat3d(x_axis,y_axis,z_axis)
					tde4.setPGroupRotation3D(cpg_id,cam_id,frame,zero_matrix.list())
				tde4.copyPGroupEditCurvesToFilteredCurves(cpg_id,cam_id)

				#make all objpgs consistent to camera
				pg_list = tde4.getPGroupList(0)
				cam = tde4.getCurrentCamera()
				for temp_obj_pg in pg_list:
					if tde4.getPGroupType(temp_obj_pg) == "OBJECT":
						tde4.setPGroupScale3D(temp_obj_pg,float(tde4.getPGroupScale3D(temp_obj_pg)))
						tde4.makePGroupChildSpaceCurvesConsistentToGlobalSpaceCurves(temp_obj_pg)
						tde4.copyPGroupEditCurvesToFilteredCurves(temp_obj_pg,cam)

				#set cpg pos and rot values to objpg
				for frame in range(len(rot3d_list)):
					world_to_3de = tde4.convertObjectPGroupTransformationWorldTo3DE(cam_id,frame+1,rot3d_list[frame].list(),pos3d_list[frame].list(),1.0,1)
					new_pos3d = world_to_3de[1]
					new_rot3d = world_to_3de[0]
					tde4.setPGroupPosition3D(obj_pg_id,cam_id,frame+1,new_pos3d)
					tde4.setPGroupRotation3D(obj_pg_id,cam_id,frame+1,new_rot3d)
				tde4.copyPGroupEditCurvesToFilteredCurves(obj_pg_id,cam_id)

			#restore camera rotations
			if widget == "restore_btn":
				pg_list = tde4.getPGroupList(0)

				#check if objpg exists
				null = 0
				for temp_obj_pg in pg_list:
					if tde4.getPGroupType(temp_obj_pg) == "OBJECT":
						name = tde4.getPGroupName(temp_obj_pg)
						if name == str("store_" + cam_name):
							null = 1
							break

				#restore camera rotations from objpg
				if null == 1:
					for frame in range(1,frames+1):
						pos3d = vec3d(tde4.getPGroupPosition3D(temp_obj_pg,cam_id,frame))
						rot3d = mat3d(tde4.getPGroupRotation3D(temp_obj_pg,cam_id,frame))
						tde4.setPGroupPosition3D(cpg_id,cam_id,frame,pos3d.list())
						tde4.setPGroupRotation3D(cpg_id,cam_id,frame,rot3d.list())
					tde4.copyPGroupEditCurvesToFilteredCurves(cpg_id,cam_id)

					#delete objpg
					tde4.deletePGroup(temp_obj_pg)
					tde4.setWidgetValue(req,"pg_name_txt","")
					tde4.setWidgetValue(req,"status_txt","")
					tde4.setWidgetFGColor(req,"status_txt",1.0,1.0,1.0)

					#make all objpgs consistent to camera
					pg_list = tde4.getPGroupList(0)
					cam = tde4.getCurrentCamera()
					for temp_obj_pg in pg_list:
						if tde4.getPGroupType(temp_obj_pg) == "OBJECT":
							tde4.setPGroupScale3D(temp_obj_pg,float(tde4.getPGroupScale3D(temp_obj_pg)))
							tde4.makePGroupChildSpaceCurvesConsistentToGlobalSpaceCurves(temp_obj_pg)
							tde4.copyPGroupEditCurvesToFilteredCurves(temp_obj_pg,cam)
				else:
					tde4.postQuestionRequester(window_title,"Error, no stored data found.","Ok")
		else:
			tde4.postQuestionRequester(window_title,"Error, please get cameraPGroup first.","Ok")


window_title = "Patcha Zero out CameraPG rotations v1.0"

req = tde4.createCustomRequester()

#camera pg name textfield widget...
tde4.addTextFieldWidget(req,"pg_name_txt","Camera | PGroup","")
tde4.setWidgetAttachModes(req,"pg_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pg_name_txt",25,85,17,0)
tde4.setWidgetSensitiveFlag(req,"pg_name_txt",0)

#camera pg get button widget...
tde4.addButtonWidget(req,"pg_get_btn","Get",70,10)
tde4.setWidgetAttachModes(req,"pg_get_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pg_get_btn",87,98,17,0)

#status widget...
tde4.addTextFieldWidget(req,"status_txt","Current status","")
tde4.setWidgetAttachModes(req,"status_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"status_txt",25,85,50,0)
tde4.setWidgetSensitiveFlag(req,"status_txt",0)

#store camera rotations button widget...
tde4.addButtonWidget(req,"store_btn","Zero out Camera rotations",70,10)
tde4.setWidgetAttachModes(req,"store_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"store_btn",5,45,85,0)

#restore camera rotations button widget...
tde4.addButtonWidget(req,"restore_btn","Restore Camera rotations",70,10)
tde4.setWidgetAttachModes(req,"restore_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"restore_btn",55,95,85,0)

#callbacks
tde4.setWidgetCallbackFunction(req,"pg_get_btn","storeMainCallback")
tde4.setWidgetCallbackFunction(req,"store_btn","storeMainCallback")
tde4.setWidgetCallbackFunction(req,"restore_btn","storeMainCallback")

tde4.postCustomRequesterAndContinue(req,window_title,500,120)