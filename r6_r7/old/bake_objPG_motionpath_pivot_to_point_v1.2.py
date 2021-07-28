# 3DE4.script.name:Bake objectPG motionpath pivot to new point...
# 3DE4.script.version:	 v1.2
# 3DE4.script.gui.config_menus: true
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.comment: Bake objectPGroup motion path pivot to selected 3dpoint. Motion is unchanged, only pivot is modified.
# Patcha Saheb (patchasaheb@gmail.com)
# 6 Nov 2016.

from vl_sdv import *
import math

#bake buffer curves...
def Bake_Buffer_Curves():
	pg = tde4.getCurrentPGroup()
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
			focal = tde4.getCameraFocalLength(cam,frame)
			tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
			tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
			tde4.setPGroupScale3D(pg,scale)
			tde4.setCameraFocalLength(cam,frame,focal)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
	if pg_type == "OBJECT":
		pg = tde4.getCurrentPGroup()
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
	#only change from public, returns to parked frame
	tde4.setCurrentFrame(cam,currentFrame)

def Update(req):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	if tde4.getPGroupType(pg) == "OBJECT":
		tde4.setWidgetValue(req,"object_name",str(tde4.getPGroupName(pg)))
	else:
		tde4.setWidgetValue(req,"object_name"," ")
		tde4.setWidgetValue(req,"point_name_txt"," ")

def Pick_Point(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pl = tde4.getPointList(pg,1)
	if tde4.getPGroupType(pg) == "OBJECT":
		if len(pl) == 1:
			tde4.setWidgetValue(req,"point_name_txt",str(tde4.getPointName(pg,pl[0])))
		else:
			tde4.postQuestionRequester(window_title, "Error, exactly one 3d point must be selected.", "ok")
	else:
		tde4.postQuestionRequester(window_title, "Error, objectPGroup must be selected.", "ok")

def Move_motionPath(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	pl = tde4.getPointList(pg,0)
	mlist = tde4.get3DModelList(pg,0)		
	if tde4.getPGroupType(pg) == "OBJECT":		
		for i_pg in tde4.getPGroupList():
			if tde4.getPGroupType(i_pg) == "CAMERA":
				id_cpg = i_pg
				break
		id_opg = pg

		point_name_given = str(tde4.getWidgetValue(req,"point_name_txt"))		
		if point_name_given != " ":
			Bake_Buffer_Curves()		
			pos_point_global_list = []			
			for frame in range(1,frames+1):	
				rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
				pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
				rot_pos_base = igl3d(rot_cpg,pos_cpg)
				rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
				pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))

				point = tde4.findPointByName(pg,point_name_given)
				point_pos = vec3d(tde4.getPointCalcPosition3D(pg,point))
				#convert point position local to global...
				pos_point_global = (rot_opg_global * point_pos) + pos_opg_global
				#delta vector in global...
				delta_vector = pos_point_global - pos_opg_global
				pos_point_global_list.append(delta_vector)

			for frame in range(1,frames+1):	
				rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
				pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
				rot_pos_base = igl3d(rot_cpg,pos_cpg)
				rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
				pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))				
				#objectPGroup new position...
				pos_opg_new_global = pos_opg_global + pos_point_global_list[frame-1]
				rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_new_global).invert() * rot_pos_base
				tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
				tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
				pf_mode  = tde4.getPGroupPostfilterMode(pg)
				tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
				tde4.filterPGroup(pg,cam)
				tde4.setPGroupPostfilterMode(pg,pf_mode)		
			#update objectPGroup pos & rot values...
			rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
			pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))
			#subtract delta vector from new point position to bring points back...
			for point in pl:
				pos_point_global = vec3d(tde4.getPointCalcPosition3D(pg,point))
				#convert point position local to global...
				pos_point_global = vec3d((rot_opg_global * pos_point_global) + pos_opg_global)			
				pos_point_new_global = pos_point_global - pos_point_global_list[frame-1]
				#convert point global position to local...
				pos_point_new_local = vec3d((rot_opg_global).invert() * (pos_point_new_global - pos_opg_global))
				tde4.setPointSurveyMode(pg,point,"SURVEY_EXACT")
				tde4.setPointSurveyPosition3D(pg,point,pos_point_new_local.list())
			#handling 3d model position...
			for model in mlist:
				pos_model = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
				#convert 3dmodel position local to global...
				pos_model_global = vec3d((rot_opg_global * pos_model) + pos_opg_global)
				#subtract delta vector from 3dmodel new position to bring 3dmodel back...
				pos_model_new_global = pos_model_global - pos_point_global_list[frame-1]
				#convert 3dmodel global position to local...
				pos_model_local = vec3d((rot_opg_global).invert() * (pos_model_new_global - pos_opg_global))
				tde4.set3DModelSurveyFlag(pg,model,0)
				tde4.set3DModelPosition3D(pg,model,pos_model_local.list())
		else:
			tde4.postQuestionRequester(window_title, "Error, please pick 3d point.", "ok")
	else:
		tde4.postQuestionRequester(window_title, "Error, objectPGroup must be selected.", "ok")	

#GUI...
window_title = "Patcha Bake objectPG motionpath pivot to new point v1.2"
req = tde4.createCustomRequester()
object_name = tde4.addTextFieldWidget(req,"object_name","objectPG Name"," ")
tde4.setWidgetAttachModes(req,"object_name","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"object_name",25,97,15,0)
tde4.setWidgetSensitiveFlag(req,"object_name",0)

tde4.addTextFieldWidget(req,"point_name_txt","Point Name"," ")
tde4.setWidgetAttachModes(req,"point_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"point_name_txt",20,68,45,0)
tde4.setWidgetSensitiveFlag(req,"point_name_txt",0)

tde4.addButtonWidget(req,"pick_point_btn","Pick 3d point",70,10)
tde4.setWidgetAttachModes(req,"pick_point_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pick_point_btn",70,97,45,0)

tde4.addButtonWidget(req,"move_path_btn","Bake objectPG motionpath pivot to new point",70,10)
tde4.setWidgetAttachModes(req,"move_path_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"move_path_btn",15,85,75,0)

tde4.setWidgetCallbackFunction(req,"pick_point_btn","Pick_Point")
tde4.setWidgetCallbackFunction(req,"move_path_btn","Move_motionPath")

tde4.postCustomRequesterAndContinue(req,window_title,550,105,"Update")
