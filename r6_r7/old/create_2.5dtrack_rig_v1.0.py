# 3DE4.script.name: Create 2.5D Track Rig...
# 3DE4.script.version: v1.0		
# 3DE4.script.gui.button:	Lineup Controls::2.5D Rig, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::2.5D Rig, align-bottom-left, 80, 20
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
				surve_mode = tde4.getPointSurveyMode(pg,pl[0])
				if surve_mode == "SURVEY_EXACT":
					point_name = tde4.getPointName(pg,pl[0])
					tde4.setWidgetValue(req,"point_name",str(point_name))
				else:
					tde4.postQuestionRequester(window_title,"Error, selected point must be Exactly Surveyed.","Ok")
			else:
				tde4.postQuestionRequester(window_title,"Error, exactly one point must be selected.","Ok")
		if widget == "create_rig_btn":
			for i_pg in tde4.getPGroupList():
				if tde4.getPGroupType(i_pg) == "CAMERA":				
					id_cpg = i_pg
					break
			id_opg = pg	
			#current base frame rotation...
			rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
			#need to subtract p3d from objPG position to bring back objPG...
			p3d	= tde4.getPointCalcPosition3D(id_opg,pl[0])

			fback_w	= tde4.getLensFBackWidth(lens)
			fback_h	= tde4.getLensFBackHeight(lens)
			xa,xb,ya,yb	= tde4.getCameraFOV(cam)
			factor	= 50.0
			for point in pl:
				for frame in range(1,frames+1):
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
						pos_opg_global = (pos_cpg+((pos_cpg - point_on_image_plane)*-factor)) - p3d

						scale = tde4.getPGroupScale3D(pg)
						rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
						tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
						tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
						tde4.setPGroupScale3D(id_opg,scale)	
				pf_mode = tde4.getPGroupPostfilterMode(id_opg)									
				tde4.setPGroupPostfilterMode(id_opg,"POSTFILTER_OFF")
				tde4.filterPGroup(id_opg,cam)
				tde4.setPGroupPostfilterMode(id_opg,pf_mode)
	else:
		tde4.postQuestionRequester(window_title,"Error, objectPGroup must be selected.","Ok")


























window_title = "Patcha Create 2.5D Track Rig to objPG v1.0"
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

#callbacks...
tde4.setWidgetCallbackFunction(req,"objpg_get_btn","Rig_Main_Callback")
tde4.setWidgetCallbackFunction(req,"point_get_btn","Rig_Main_Callback")
tde4.setWidgetCallbackFunction(req,"create_rig_btn","Rig_Main_Callback")





tde4.postCustomRequesterAndContinue(req,window_title,450,105)
