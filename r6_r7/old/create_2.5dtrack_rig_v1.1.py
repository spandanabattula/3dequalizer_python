# 3DE4.script.name: Create 2.5D Track Rig...
# 3DE4.script.version: v1.1		
# 3DE4.script.gui.button:	Lineup Controls::2.5D Rig, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::2.5D Rig, align-bottom-left, 80, 20
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.comment: Creates 2.5D Rig setup to objectPGroup.
# Patcha Saheb (patchasaheb@gmail.com)

from vl_sdv import*

def Rig_Main_Callback(req,widget,action):
	pg  = tde4.getCurrentPGroup()
	cam  = tde4.getCurrentCamera()
	frame  = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	pl	= tde4.getPointList(pg,1)	
	lens = tde4.getCameraLens(cam)
	pg_type = tde4.getPGroupType(pg)
	if pg_type == "OBJECT":
		if widget == "objpg_get_btn":
			pg_name = tde4.getPGroupName(pg)
			tde4.setWidgetValue(req,"objpg_name",str(pg_name))
		if widget == "point_get_btn":
			pl = tde4.getPointList(pg,1)
			if len(pl) == 1:
				point_name = tde4.getPointName(pg,pl[0])
				tde4.setWidgetValue(req,"point_name",str(point_name))
			else:
				tde4.postQuestionRequester(window_title,"Error, exactly one point must be selected.","Ok")

		#store camera pg id...
		for i_pg in tde4.getPGroupList():
			if tde4.getPGroupType(i_pg) == "CAMERA":				
				id_cpg = i_pg
				break

		#store object pg id...
		for i_pg in tde4.getPGroupList():
			if tde4.getPGroupName(i_pg) == tde4.getWidgetValue(req,"objpg_name"):
				id_opg = i_pg
				break

		#store 3DModels pos & rot,scale values...
		model_pos_list = []
		model_rot_scale_list = []
		mlist = tde4.get3DModelList(id_opg,0)
		id_opg_pos = tde4.getPGroupPosition3D(id_opg,cam,frame)
		id_opg_rot = tde4.getPGroupRotation3D(id_opg,cam,frame)			
		for model in mlist:
			model_pos = tde4.get3DModelPosition3D(id_opg,model,cam,frame)
			model_rot_scale = tde4.get3DModelRotationScale3D(id_opg,model)
			model_pos_global = (mat3d(id_opg_rot) * vec3d(model_pos)) + vec3d(id_opg_pos)
			model_rot_scale_global = mat3d(id_opg_rot) * mat3d(model_rot_scale)
			model_pos_list.append(model_pos_global)
			model_rot_scale_list.append(model_rot_scale_global)

		#store point id...
		pl = tde4.getPointList(id_opg,0)
		v = tde4.getWidgetValue(req,"point_name")
		for point in pl:
			if tde4.getPointName(id_opg,point) == v:
				break

		if widget == "create_rig_btn":

			#current base frame rotation...
			rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
			#need to subtract p3d from objPG position to bring back objPG...
			#p3d	= tde4.getPointCalcPosition3D(id_opg,pl[0])

			fback_w	= tde4.getLensFBackWidth(lens)
			fback_h	= tde4.getLensFBackHeight(lens)
			xa,xb,ya,yb	= tde4.getCameraFOV(cam)
			factor	= 50.0
			if tde4.getPointSurveyMode(id_opg,point) == "SURVEY_EXACT":
				survey_pos = tde4.getPointSurveyPosition3D(id_opg,point)
				survey_pos_global = (mat3d(id_opg_rot) * vec3d(survey_pos)) + vec3d(id_opg_pos)

			playback_range = tde4.getCameraPlaybackRange(cam)
			start_frame = playback_range[0]
			end_frame = playback_range[1]

			for frame in range(start_frame,end_frame+1):
				if tde4.isPointPos2DValid(pg,point,cam,frame) == 1:
					focal	= tde4.getCameraFocalLength(cam,frame)
					p2d	= tde4.getPointPosition2D(pg,point,cam,frame)
					p2d	= tde4.removeDistortion2D(cam,frame,p2d)						
					pg = tde4.getCurrentPGroup()

					pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
					rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))						
					rot_pos_base = igl3d(rot_cpg,pos_cpg)

					v0 = rot_cpg * vec3d(fback_w*(p2d[0]-0.5*(1.0/(xb-xa))),0.0,0.0) 
					v1 = rot_cpg * vec3d(0.0,fback_h*(p2d[1]-0.5*(1.0/(yb-ya))),0.0)
					v2 = rot_cpg * vec3d(0.0,0.0,-focal)

					point_on_image_plane = pos_cpg + v2 + v1 + v0
					pos_opg_global = (pos_cpg+((pos_cpg - point_on_image_plane)*-factor))
					scale = tde4.getPGroupScale3D(pg)
					rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
					tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
					tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
					tde4.setPGroupScale3D(id_opg,scale)
					tde4.setPointSurveyMode(id_opg,point,"SURVEY_EXACT")
					tde4.setPointSurveyPosition3D(id_opg,point,[0.0,0.0,0.0])	
			pf_mode = tde4.getPGroupPostfilterMode(id_opg)									
			tde4.setPGroupPostfilterMode(id_opg,"POSTFILTER_OFF")
			tde4.filterPGroup(id_opg,cam)
			tde4.setPGroupPostfilterMode(id_opg,pf_mode)

			#update frame, objpg pos,rot values...
			frame = tde4.getCurrentFrame(cam)
			id_opg_pos = tde4.getPGroupPosition3D(id_opg,cam,frame)
			id_opg_rot = tde4.getPGroupRotation3D(id_opg,cam,frame)

			#setting up back 3DModels pos & rot,scale values...
			null = 0
			for model in mlist:
				tde4.set3DModelSurveyFlag(id_opg,model,0)
				model_pos_local = mat3d(id_opg_rot).invert() * (vec3d(model_pos_list[null]) - vec3d(id_opg_pos))
				model_rot_scale_local = mat3d(id_opg_rot).invert() * model_rot_scale_list[null]
				tde4.set3DModelPosition3D(id_opg,model,model_pos_local.list())
				tde4.set3DModelRotationScale3D(id_opg,model,model_rot_scale_local.list())
				null = null + 1

		power = float(tde4.getWidgetValue(req,"slider_wdgt"))
		if widget == "screenz-" or widget == "screenz+":
			if widget == "screenz-": power = -float(power)
			for frame in range(1,frames+1):
				cam_pos = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
				cam_rot = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
				obj_pos = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))
				obj_rot = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))	
				scale = tde4.getPGroupScale3D(id_opg)
				p1 = cam_pos + ((obj_pos - cam_pos) * (1.0 + float(power)))
				local_values = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,obj_rot.list(),p1.list(),1.0,0)
				tde4.setPGroupPosition3D(id_opg,cam,frame,local_values[1])
				tde4.setPGroupScale3D(id_opg,scale)
			pf_mode = tde4.getPGroupPostfilterMode(id_opg)									
			tde4.setPGroupPostfilterMode(id_opg,"POSTFILTER_OFF")
			tde4.filterPGroup(id_opg,cam)
			tde4.setPGroupPostfilterMode(id_opg,pf_mode)

			#update frame, objpg pos,rot values...
			frame = tde4.getCurrentFrame(cam)
			id_opg_pos = tde4.getPGroupPosition3D(id_opg,cam,frame)
			id_opg_rot = tde4.getPGroupRotation3D(id_opg,cam,frame)

			#setting up back 3DModels pos & rot,scale values...
			null = 0
			for model in mlist:
				tde4.set3DModelSurveyFlag(id_opg,model,0)
				model_pos_local = mat3d(id_opg_rot).invert() * (vec3d(model_pos_list[null]) - vec3d(id_opg_pos))
				model_rot_scale_local = mat3d(id_opg_rot).invert() * model_rot_scale_list[null]
				tde4.set3DModelPosition3D(id_opg,model,model_pos_local.list())
				tde4.set3DModelRotationScale3D(id_opg,model,model_rot_scale_local.list())
				null = null + 1










	else:
		tde4.postQuestionRequester(window_title,"Error, objectPGroup must be selected.","Ok")


























window_title = "Patcha Create 2.5D Track Rig to objPG v1.1"
req = tde4.createCustomRequester()

#objPG name textfield widget...
tde4.addTextFieldWidget(req,"objpg_name","ObjectPGroup"," ")
tde4.setWidgetAttachModes(req,"objpg_name","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"objpg_name",25,83,10,0)
tde4.setWidgetSensitiveFlag(req,"objpg_name",0)

#objPG get button widget...
tde4.addButtonWidget(req,"objpg_get_btn","Get",70,10)
tde4.setWidgetAttachModes(req,"objpg_get_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"objpg_get_btn",86,98,10,0)

#point name textfield widget...
tde4.addTextFieldWidget(req,"point_name","Point"," ")
tde4.setWidgetAttachModes(req,"point_name","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"point_name",25,83,40,0)
tde4.setWidgetSensitiveFlag(req,"point_name",0)

#point get button widget...
tde4.addButtonWidget(req,"point_get_btn","Get",70,10)
tde4.setWidgetAttachModes(req,"point_get_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"point_get_btn",86,98,40,0)

#create 2.5d track rig button widget...
tde4.addButtonWidget(req,"create_rig_btn","Create 2.5D Track Rig to ObjectPGroup",70,10)
tde4.setWidgetAttachModes(req,"create_rig_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"create_rig_btn",15,85,75,0)

#slider widget...
tde4.addScaleWidget(req,"slider_wdgt","ScreenZ Nudge","DOUBLE",0.001,0.1,0.05)
tde4.setWidgetAttachModes(req,"slider_wdgt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"slider_wdgt",24,98,105,0)

#screen Z- button widget...
tde4.addButtonWidget(req,"screenz-","Screen Z -",70,10)
tde4.setWidgetAttachModes(req,"screenz-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"screenz-",10,45,135,0)

#screen Z+ button widget...
tde4.addButtonWidget(req,"screenz+","Screen Z +",70,10)
tde4.setWidgetAttachModes(req,"screenz+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"screenz+",55,90,135,0)













#callbacks...
tde4.setWidgetCallbackFunction(req,"objpg_get_btn","Rig_Main_Callback")
tde4.setWidgetCallbackFunction(req,"point_get_btn","Rig_Main_Callback")
tde4.setWidgetCallbackFunction(req,"create_rig_btn","Rig_Main_Callback")
tde4.setWidgetCallbackFunction(req,"screenz-","Rig_Main_Callback")
tde4.setWidgetCallbackFunction(req,"screenz+","Rig_Main_Callback")




tde4.postCustomRequesterAndContinue(req,window_title,480,165)
