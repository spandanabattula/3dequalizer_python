# 3DE4.script.name: Camera/Object offset Curve Editor...
# 3DE4.script.version: v1.2
# 3DE4.script.gui: Lineup Controls::Edit
# 3DE4.script.gui: Orientation Controls::Edit
# 3DE4.script.gui.button: Lineup Controls::Offset Curves, align-bottom-left, 80,20
# 3DE4.script.gui.button: Orientation Controls::Offset Curves, align-bottom-left, 70,20
# 3DE4.script.comment:	This script works as Animation Layer in Maya.
# 3DE4.script.gui.config_menus: true
# Patcha Saheb(patchasaheb@gmail.com)
# 19 Nov 2016(India)
# updated 07 Feb 2018(Montreal)

from vl_sdv import*
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

def Cursor_Update(req):
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	tde4.setCurveAreaWidgetCursorPosition(req,"curves_area",frame,1)

def Curvearea_Callback(req,widget,action):
	cam = tde4.getCurrentCamera()
	if action==3 or action==2:
		f = tde4.getCurveAreaWidgetCursorPosition(req,"curves_area")
		n = tde4.getCameraNoFrames(cam)
		if f < 1: f = 1
		if f > n: f = 1
		tde4.setCurrentFrame(cam,int(f))

def Min_Max(keylist,curve):
	keylist = tde4.getCurveKeyList(curve,0)
	x = []
	y = []
	for key in keylist:
		pos_2d = tde4.getCurveKeyPosition(curve,key)
		x.append(pos_2d[0])
		y.append(pos_2d[1])
	return min(x),max(x),min(y),max(y)

def Editmenu_Callback(req,widget,action):
	if widget == "delete_cvs":
		curve_list = tde4.getCurveAreaWidgetCurveList(req,"curves_area")
		for curve in curve_list:
			keylist = tde4.getCurveKeyList(curve,1)
			for key in keylist:
				tde4.deleteCurveKey(curve,key)
			tde4.updateGUI(1)
	if widget == "set_linear" or widget == "set_smooth" or widget == "set_broken":
		mode = widget[4:10].upper()
		curve_list = tde4.getCurveAreaWidgetCurveList(req,"curves_area")		
		for curve in curve_list:
			keylist = tde4.getCurveKeyList(curve,1)
			for key in keylist:
				tde4.setCurveKeyMode(curve,key,mode)
				if mode!="LINEAR":
					k0 = tde4.getPrevCurveKey(curve,key)
					k1 = tde4.getNextCurveKey(curve,key)
					if k0 != None and k1 != None:
						v0 = tde4.getCurveKeyPosition(curve,k0)
						v1 = tde4.getCurveKeyPosition(curve,k1)
						tx = (v0[0]-v1[0])/50.0
						ty = (v0[1]-v1[1])/50.0
						tde4.setCurveKeyTangent1(curve,key,[tx,ty])
						tde4.setCurveKeyTangent2(curve,key,[-tx,-ty])
		tde4.updateGUI(1)
	if widget == "flatten":
		curve_list = tde4.getCurveAreaWidgetCurveList(req,"curves_area")		
		for curve in curve_list:
			keylist = tde4.getCurveKeyList(curve,1)
			for key in keylist:
				t = tde4.getCurveKeyTangent1(curve,key)
				t[1] = 0.0
				tde4.setCurveKeyTangent1(curve,key,t)
				t = tde4.getCurveKeyTangent2(curve,key)
				t[1] = 0.0
				tde4.setCurveKeyTangent2(curve,key,t)
		tde4.updateGUI(1)
	if widget == "fix_cvs" or widget == "unfix_cvs":
		if widget == "fix_cvs": flag = 1
		else: flag = 0
		curve_list = tde4.getCurveAreaWidgetCurveList(req,"curves_area")		
		for curve in curve_list:
			keylist = tde4.getCurveKeyList(curve,1)
			for key in keylist:
				tde4.setCurveKeyFixedXFlag(curve,key,flag)
		tde4.updateGUI(1)		

def Update_Base_Curves():
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	frame_offset = tde4.getCameraFrameOffset(cam)
	focal_mode = tde4.getCameraFocalLengthMode(cam)	
	for frame in range(1,frames+1):
		pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
		rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
		pos_x = pos_pg[0]
		pos_y = pos_pg[1] 
		pos_z = pos_pg[2]
		rot_x = convertToAngles(rot_pg)[0]
		rot_y = convertToAngles(rot_pg)[1]
		rot_z = convertToAngles(rot_pg)[2]
		pos_x_curve_key = tde4.createCurveKey(pos_x_curve,[frame,pos_x])
		tde4.setCurveKeyMode(pos_x_curve,pos_x_curve_key,"LINEAR")
		pos_y_curve_key = tde4.createCurveKey(pos_y_curve,[frame,pos_y])
		tde4.setCurveKeyMode(pos_y_curve,pos_y_curve_key,"LINEAR")
		pos_z_curve_key = tde4.createCurveKey(pos_z_curve,[frame,pos_z])
		tde4.setCurveKeyMode(pos_z_curve,pos_z_curve_key,"LINEAR")		
		rot_x_curve_key = tde4.createCurveKey(rot_x_curve,[frame,rot_x])
		tde4.setCurveKeyMode(rot_x_curve,rot_x_curve_key,"LINEAR")
		rot_y_curve_key = tde4.createCurveKey(rot_y_curve,[frame,rot_y])
		tde4.setCurveKeyMode(rot_y_curve,rot_y_curve_key,"LINEAR")
		rot_z_curve_key = tde4.createCurveKey(rot_z_curve,[frame,rot_z])
		tde4.setCurveKeyMode(rot_z_curve,rot_z_curve_key,"LINEAR")
	if focal_mode == "FOCAL_DYNAMIC":
		zoom_curve = tde4.getCameraZoomCurve(cam)
		kl = tde4.getCurveKeyList(zoom_curve)
		for key in kl:
			pos_2d = tde4.getCurveKeyPosition(zoom_curve,key)
			pos_2d[0] = pos_2d[0]
			pos_2d[1] = pos_2d[1] * 10.0
			focal_curve_key = tde4.createCurveKey(focal_curve,pos_2d)
			tde4.setCurveKeyMode(focal_curve,focal_curve_key,"LINEAR")
	tde4.setWidgetValue(req,"pg_name_txt",str(tde4.getPGroupName(pg)))


def Delete_Keys(req,widget,action):
	offset_curves_list = [pos_x_offset_curve, pos_y_offset_curve, pos_z_offset_curve, rot_x_offset_curve, rot_y_offset_curve, rot_z_offset_curve]
	frame = tde4.getCurrentFrame(tde4.getCurrentCamera())
	for offset_curve in offset_curves_list:
		kl = tde4.getCurveKeyList(offset_curve,0)
		for key in kl:
			pos_2d = tde4.getCurveKeyPosition(offset_curve,key)
			if pos_2d[0] == frame:
				tde4.deleteCurveKey(offset_curve,key)
				

def Create_Keys(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pg_type = tde4.getPGroupType(pg)

	offset_curves_list = [pos_x_offset_curve, pos_y_offset_curve, pos_z_offset_curve, rot_x_offset_curve, rot_y_offset_curve, rot_z_offset_curve]
	for offset_curve in offset_curves_list:
		if widget == "create_keys_btn":
			offset_curve_y = tde4.evaluateCurve(offset_curve,frame)
		if widget == "zero_keys_btn":
			offset_curve_y = 0.0
		key = tde4.createCurveKey(offset_curve,[frame,offset_curve_y])
		tde4.setCurveKeyFixedXFlag(offset_curve,key,1)
		tde4.setCurveKeyMode(offset_curve,key,"LINEAR")
	focal_curve_kl = tde4.getCurveKeyList(focal_curve)
	if len(focal_curve_kl) > 0:
		if widget == "create_keys_btn":		
			focal_offset_curve_y = tde4.evaluateCurve(focal_offset_curve,frame)
		if widget == "zero_keys_btn":
			focal_offset_curve_y = 0.0
		key = tde4.createCurveKey(focal_offset_curve,[frame,focal_offset_curve_y])
		tde4.setCurveKeyFixedXFlag(focal_offset_curve,key,1)
		tde4.setCurveKeyMode(focal_offset_curve,key,"LINEAR")
	if widget == "zero_keys_btn":
		pos_x = tde4.evaluateCurve(pos_x_curve,frame)
		pos_y = tde4.evaluateCurve(pos_y_curve,frame)
		pos_z = tde4.evaluateCurve(pos_z_curve,frame)
		new_rot_x = tde4.evaluateCurve(rot_x_curve,frame)
		new_rot_y = tde4.evaluateCurve(rot_y_curve,frame)
		new_rot_z = tde4.evaluateCurve(rot_z_curve,frame)
		new_rot_x = (new_rot_x*3.141592654)/180.0
		new_rot_y = (new_rot_y*3.141592654)/180.0
		new_rot_z = (new_rot_z*3.141592654)/180.0
		rot_3d = mat3d(rot3d(new_rot_x,new_rot_y,new_rot_z,VL_APPLY_ZXY))
		if pg_type == "CAMERA":
			tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,pos_y,pos_z])
			tde4.setPGroupRotation3D(pg,cam,frame,rot_3d.list())
		if pg_type == "OBJECT":
			for i_pg in tde4.getPGroupList():
				if tde4.getPGroupType(i_pg) == "CAMERA":
					id_cpg = i_pg
					break
			id_opg = pg
			rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
			pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
			rot_pos_base = igl3d(rot_cpg,pos_cpg)
			rot_opg_global = rot_3d
			pos_opg_global = vec3d(pos_x,pos_y,pos_z)
			rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
			tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
			tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())				
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
				

def Main_Callback(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	frames = tde4.getCameraNoFrames(cam)
	pg_type = tde4.getPGroupType(pg)
	if widget == "curves_list":
		tde4.detachCurveAreaWidgetAllCurves(req,"curves_area")		
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",0):
			curve = pos_x_curve
			keylist = tde4.getCurveKeyList(pos_x_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_x_curve,1.0,0.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_x_curve,1.0,0.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)						
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",1):
			curve = pos_y_curve
			keylist = tde4.getCurveKeyList(pos_y_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_y_curve,0.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_y_curve,0.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",2):
			curve = pos_z_curve
			keylist = tde4.getCurveKeyList(pos_z_curve,0)
			if len(keylist) >= 1:			
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_z_curve,0.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_z_curve,0.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",3):
			curve = rot_x_curve
			keylist = tde4.getCurveKeyList(rot_x_curve,0)
			if len(keylist) >= 1:			
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_x_curve,0.0,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_x_curve,0.0,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",4):
			curve = rot_y_curve
			keylist = tde4.getCurveKeyList(rot_y_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_y_curve,1.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_y_curve,1.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",5):
			curve = rot_z_curve
			keylist = tde4.getCurveKeyList(rot_z_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_z_curve,1.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_z_curve,1.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",6):
			curve = focal_curve
			keylist = tde4.getCurveKeyList(focal_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",focal_curve,1.0,0.3,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",focal_curve,1.0,0.3,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",7):
			curve = pos_x_offset_curve
			keylist = tde4.getCurveKeyList(pos_x_offset_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_x_offset_curve,1.0,0.4,0.4,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_x_offset_curve,1.0,0.4,0.4,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",8):
			curve = pos_y_offset_curve
			keylist = tde4.getCurveKeyList(pos_y_offset_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_y_offset_curve,0.4,1.0,0.4,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_y_offset_curve,0.4,1.0,0.4,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",9):
			curve = pos_z_offset_curve
			keylist = tde4.getCurveKeyList(pos_z_offset_curve,0)
			if len(keylist) >= 1:			
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_z_offset_curve,0.4,0.4,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_z_offset_curve,0.4,0.4,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",10):
			curve = rot_x_offset_curve
			keylist = tde4.getCurveKeyList(rot_x_offset_curve,0)
			if len(keylist) >= 1:			
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_x_offset_curve,0.5,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_x_offset_curve,0.5,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)	
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",11):
			curve = rot_y_offset_curve
			keylist = tde4.getCurveKeyList(rot_y_offset_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_y_offset_curve,1.0,0.4,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_y_offset_curve,1.0,0.4,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",12):
			curve = rot_z_offset_curve
			keylist = tde4.getCurveKeyList(rot_z_offset_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_z_offset_curve,1.0,1.0,0.4,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",rot_z_offset_curve,1.0,1.0,0.4,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",13):
			curve = focal_offset_curve
			keylist = tde4.getCurveKeyList(focal_offset_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",focal_offset_curve,1.0,0.5,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",focal_offset_curve,1.0,0.5,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
	if widget == "update_offset_curves_btn":
		zoom_curve = tde4.getCameraZoomCurve(cam)
		keylist = tde4.getCurveKeyList(pos_x_offset_curve,0)
		for key in keylist:
			pos_2d_offset_curve = tde4.getCurveKeyPosition(pos_x_offset_curve,key)
			pos_2d_base_curve = tde4.evaluateCurve(pos_x_curve,pos_2d_offset_curve[0])
			frame = int(pos_2d_offset_curve[0])
			pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
			rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
			pos_x = pos_pg[0]
			new_pos_x = pos_x - pos_2d_base_curve
			tde4.setCurveKeyPosition(pos_x_offset_curve,key,[frame,new_pos_x])
		keylist = tde4.getCurveKeyList(pos_y_offset_curve,0)
		for key in keylist:
			pos_2d_offset_curve = tde4.getCurveKeyPosition(pos_y_offset_curve,key)
			pos_2d_base_curve = tde4.evaluateCurve(pos_y_curve,pos_2d_offset_curve[0])
			frame = int(pos_2d_offset_curve[0])
			pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
			rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
			pos_y = pos_pg[1] 
			new_pos_y = pos_y - pos_2d_base_curve
			tde4.setCurveKeyPosition(pos_y_offset_curve,key,[frame,new_pos_y])
		keylist = tde4.getCurveKeyList(pos_z_offset_curve,0)
		for key in keylist:
			pos_2d_offset_curve = tde4.getCurveKeyPosition(pos_z_offset_curve,key)
			pos_2d_base_curve = tde4.evaluateCurve(pos_z_curve,pos_2d_offset_curve[0])
			frame = int(pos_2d_offset_curve[0])
			pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
			rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
			pos_z = pos_pg[2]
			new_pos_z = pos_z - pos_2d_base_curve
			tde4.setCurveKeyPosition(pos_z_offset_curve,key,[frame,new_pos_z])
		keylist = tde4.getCurveKeyList(rot_x_offset_curve,0)
		for key in keylist:
			pos_2d_offset_curve = tde4.getCurveKeyPosition(rot_x_offset_curve,key)
			pos_2d_base_curve = tde4.evaluateCurve(rot_x_curve,pos_2d_offset_curve[0])
			frame = int(pos_2d_offset_curve[0])
			pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
			rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
			rot_x = convertToAngles(rot_pg)[0]
			new_rot_x = rot_x - pos_2d_base_curve
			tde4.setCurveKeyPosition(rot_x_offset_curve,key,[frame,new_rot_x])
		keylist = tde4.getCurveKeyList(rot_y_offset_curve,0)
		for key in keylist:
			pos_2d_offset_curve = tde4.getCurveKeyPosition(rot_y_offset_curve,key)
			pos_2d_base_curve = tde4.evaluateCurve(rot_y_curve,pos_2d_offset_curve[0])
			frame = int(pos_2d_offset_curve[0])
			pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
			rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
			rot_y = convertToAngles(rot_pg)[1]
			new_rot_y = rot_y - pos_2d_base_curve
			tde4.setCurveKeyPosition(rot_y_offset_curve,key,[frame,new_rot_y])
		keylist = tde4.getCurveKeyList(rot_z_offset_curve,0)
		for key in keylist:
			pos_2d_offset_curve = tde4.getCurveKeyPosition(rot_z_offset_curve,key)
			pos_2d_base_curve = tde4.evaluateCurve(rot_z_curve,pos_2d_offset_curve[0])
			frame = int(pos_2d_offset_curve[0])
			pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
			rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
			rot_z = convertToAngles(rot_pg)[2]
			new_rot_z = rot_z - pos_2d_base_curve
			tde4.setCurveKeyPosition(rot_z_offset_curve,key,[frame,new_rot_z])
		keylist = tde4.getCurveKeyList(focal_offset_curve,0)
		#if len(keylist) > 0:
		for key in keylist:
			pos_2d_offset_curve = tde4.getCurveKeyPosition(focal_offset_curve,key)
			pos_2d_base_curve = tde4.evaluateCurve(focal_curve,pos_2d_offset_curve[0])
			frame = int(pos_2d_offset_curve[0])
			new_focal = tde4.evaluateCurve(zoom_curve,frame) * 10.0
			new_focal = new_focal - pos_2d_base_curve
			tde4.setCurveKeyPosition(focal_offset_curve,key,[frame,new_focal])
		for frame in range(1,frames+1):
			pos_pg = tde4.getPGroupPosition3D(pg,cam,frame)
			rot_pg = tde4.getPGroupRotation3D(pg,cam,frame)
			pos_x = pos_pg[0]
			pos_y = pos_pg[1] 
			pos_z = pos_pg[2]
			rot_x = convertToAngles(rot_pg)[0]
			rot_y = convertToAngles(rot_pg)[1]
			rot_z = convertToAngles(rot_pg)[2]						
			new_pos_x = Merge_Curves(pos_x_curve,pos_x_offset_curve,frame)
			new_pos_y = Merge_Curves(pos_y_curve,pos_y_offset_curve,frame)
			new_pos_z = Merge_Curves(pos_z_curve,pos_z_offset_curve,frame)
			new_rot_x = Merge_Curves(rot_x_curve,rot_x_offset_curve,frame)
			new_rot_y = Merge_Curves(rot_y_curve,rot_y_offset_curve,frame)
			new_rot_z = Merge_Curves(rot_z_curve,rot_z_offset_curve,frame)
			new_rot_x = (new_rot_x*3.141592654)/180.0
			new_rot_y = (new_rot_y*3.141592654)/180.0
			new_rot_z = (new_rot_z*3.141592654)/180.0
			rot_3d = mat3d(rot3d(new_rot_x,new_rot_y,new_rot_z,VL_APPLY_ZXY))
			if pg_type == "CAMERA":
				tde4.setPGroupPosition3D(pg,cam,frame,[new_pos_x,new_pos_y,new_pos_z])
				tde4.setPGroupRotation3D(pg,cam,frame,rot_3d.list())
			if pg_type == "OBJECT":
				for i_pg in tde4.getPGroupList():
					if tde4.getPGroupType(i_pg) == "CAMERA":
						id_cpg = i_pg
						break
				id_opg = pg
				rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
				pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
				rot_pos_base = igl3d(rot_cpg,pos_cpg)
				rot_opg_global = rot_3d
				pos_opg_global = vec3d(new_pos_x,new_pos_y,new_pos_z)
				rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
				tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
				tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())				
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
		zoom_curve = tde4.getCameraZoomCurve(cam)		
		keylist = tde4.getCurveKeyList(zoom_curve,0)
		for key in keylist:
			frame = tde4.getCurveKeyPosition(zoom_curve,key)
			frame = frame[0]
			new_focal = Merge_Curves(focal_curve,focal_offset_curve,frame)
			tde4.setCurveKeyPosition(zoom_curve,key,[frame,new_focal/10.0])
		if tde4.widgetExists(req,"update_objpg_toggle"):
			toggle_v = int(tde4.getWidgetValue(req,"update_objpg_toggle"))			
			if toggle_v == 1:
				pgl = tde4.getPGroupList()
				for pgroup in pgl:
					pg_type = tde4.getPGroupType(pgroup)
					if pg_type == "OBJECT":
						tde4.setPGroupScale3D(pgroup,tde4.getPGroupScale3D(pgroup))	

	if widget == "merge_offset_curves_widget":
		for frame in range(1,frames+1):		
			new_pos_x = Merge_Curves(pos_x_curve,pos_x_offset_curve,frame)
			new_pos_y = Merge_Curves(pos_y_curve,pos_y_offset_curve,frame)
			new_pos_z = Merge_Curves(pos_z_curve,pos_z_offset_curve,frame)
			new_rot_x = Merge_Curves(rot_x_curve,rot_x_offset_curve,frame)
			new_rot_y = Merge_Curves(rot_y_curve,rot_y_offset_curve,frame)
			new_rot_z = Merge_Curves(rot_z_curve,rot_z_offset_curve,frame)
			tde4.createCurveKey(pos_x_curve,[frame,new_pos_x])
			tde4.createCurveKey(pos_y_curve,[frame,new_pos_y])			
			tde4.createCurveKey(pos_z_curve,[frame,new_pos_z])
			tde4.createCurveKey(rot_x_curve,[frame,new_rot_x])
			tde4.createCurveKey(rot_y_curve,[frame,new_rot_y])
			tde4.createCurveKey(rot_z_curve,[frame,new_rot_z])
		new_focal_values = []
		zoom_curve = tde4.getCameraZoomCurve(cam)
		keylist = tde4.getCurveKeyList(zoom_curve,0)
		for key in keylist:
			pos_2d = tde4.getCurveKeyPosition(zoom_curve,key)
			new_focal_values.append(pos_2d[1])
		keylist = tde4.getCurveKeyList(focal_curve,0)
		for i in range(len(keylist)):
			pos_2d = tde4.getCurveKeyPosition(focal_curve,keylist[i])
			tde4.setCurveKeyPosition(focal_curve,keylist[i],[pos_2d[0],new_focal_values[i]])					
		tde4.deleteAllCurveKeys(pos_x_offset_curve)
		tde4.deleteAllCurveKeys(pos_y_offset_curve)
		tde4.deleteAllCurveKeys(pos_z_offset_curve)
		tde4.deleteAllCurveKeys(rot_x_offset_curve)
		tde4.deleteAllCurveKeys(rot_y_offset_curve)
		tde4.deleteAllCurveKeys(rot_z_offset_curve)
		tde4.deleteAllCurveKeys(focal_offset_curve)	
	if widget == "key-" or widget == "key+" or widget == "jump_previous_key" or widget == "jump_next_key":
		curve_list = tde4.getCurveAreaWidgetCurveList(req,"curves_area")
		curve =  curve_list[0]
		if widget == "key+" or widget == "jump_next_key":
			keylist = tde4.getCurveKeyList(curve,0)
			f = 1000000
			for key in keylist:
				pos = tde4.getCurveKeyPosition(curve,key)
				if int(pos[0])>frame and int(pos[0])<f:
					f = int(pos[0])
					break
			if f != 1000000:
				tde4.setCurrentFrame(cam,f)
				tde4.setCurveAreaWidgetCursorPosition(req,"curves_area",tde4.getCurrentFrame(cam))
		if widget == "key-" or widget == "jump_previous_key":
			keylist = tde4.getCurveKeyList(curve,0)	
			keylist.reverse()
			f = -1
			for key in keylist:
				pos =  tde4.getCurveKeyPosition(curve,key)
				if int(pos[0])<frame and int(pos[0])>f:
					f = int(pos[0])
					break
			if f!= -1:
				tde4.setCurrentFrame(cam,f)
				tde4.setCurveAreaWidgetCursorPosition(req,"curves_area",tde4.getCurrentFrame(cam))

	"""if widget == "delete_frame_all_menu_widget":
		current_frame = tde4.getCurrentFrame(cam)"""












	if widget == "delete_all_menu_widget":
		tde4.deleteAllCurveKeys(pos_x_offset_curve)
		tde4.deleteAllCurveKeys(pos_y_offset_curve)
		tde4.deleteAllCurveKeys(pos_z_offset_curve)
		tde4.deleteAllCurveKeys(rot_x_offset_curve)
		tde4.deleteAllCurveKeys(rot_y_offset_curve)
		tde4.deleteAllCurveKeys(rot_z_offset_curve)
		tde4.deleteAllCurveKeys(focal_offset_curve)
	if widget == "view_all" or widget == "view_all_menu_widget":
		y = []
		curves_list = tde4.getCurveAreaWidgetCurveList(req,"curves_area")
		for curve in curves_list:
			keylist = tde4.getCurveKeyList(curve,0)
			for key in keylist:
				pos_2d = tde4.getCurveKeyPosition(curve,key)
				y.append(pos_2d[1])
		if len(y) >= 1:
			tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,min(y)-0.1,max(y)+0.1)
		else:
			tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)

def Merge_Curves(curve,offset_curve,frame):
	curve_pos_y = tde4.evaluateCurve(curve,frame)
	offset_curve_pos_y = tde4.evaluateCurve(offset_curve,frame)
	new_pos_y = curve_pos_y + offset_curve_pos_y
	return new_pos_y

def convertToAngles(r3d):
	rot = rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
	rx = (rot[0]*180.0)/3.141592654
	ry = (rot[1]*180.0)/3.141592654
	rz = (rot[2]*180.0)/3.141592654
	return rx,ry,rz

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
frames = tde4.getCameraNoFrames(cam)
frame_offset = tde4.getCameraFrameOffset(cam)

window_title = "Patcha Camera/Object offset Curve Editor v1.2"
req = tde4.createCustomRequester()

#add menu bar widget...
tde4.addMenuBarWidget(req,"menu_bar")
tde4.setWidgetAttachModes(req,"menu_bar","ATTACH_WINDOW","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetOffsets(req,"menu_bar",2,20,2,0)

""""#add file menu...
tde4.addMenuWidget(req,"file_menu","File","menu_bar",0)
tde4.addMenuButtonWidget(req,"import_offset_keys","Import offset curves keys","file_menu")
tde4.addMenuButtonWidget(req,"export_offset_keys","Export offset curves keys","file_menu")"""

#add edit menu...
tde4.addMenuWidget(req,"edit_menu","Edit","menu_bar",0)
tde4.addMenuButtonWidget(req,"delete_cvs","Delete CVs","edit_menu")
tde4.setWidgetShortcut(req,"delete_cvs",8)
tde4.addMenuSeparatorWidget(req,"sep1","edit_menu")
tde4.addMenuWidget(req,"set_cvs_menu","Set CVs To","edit_menu")
tde4.addMenuButtonWidget(req,"set_linear","Linear","set_cvs_menu")
tde4.setWidgetShortcut(req,"set_linear",108)
tde4.addMenuButtonWidget(req,"set_smooth","Smooth","set_cvs_menu")
tde4.setWidgetShortcut(req,"set_smooth",115)
tde4.addMenuButtonWidget(req,"set_broken","Broken","set_cvs_menu")
tde4.setWidgetShortcut(req,"set_broken",98)
tde4.addMenuButtonWidget(req,"flatten","Flatten Tangents","edit_menu")
tde4.addMenuButtonWidget(req,"fix_cvs","Fix CVs Vertically","edit_menu")
tde4.addMenuButtonWidget(req,"unfix_cvs","Unfix CVs Vertically","edit_menu")
tde4.addMenuButtonWidget(req,"jump_previous_key","Jump to Previous Key","edit_menu")
tde4.setWidgetShortcut(req,"jump_previous_key",3018)
tde4.addMenuButtonWidget(req,"jump_next_key","Jump to Next Key","edit_menu")
tde4.setWidgetShortcut(req,"jump_next_key",3019)

#add view menu...
tde4.addMenuWidget(req,"view_menu","View","menu_bar",0)
tde4.addMenuButtonWidget(req,"view_all_menu_widget","View All","view_menu")
tde4.setWidgetShortcut(req,"view_all_menu_widget",32)

#add delete menu...
tde4.addMenuWidget(req,"delete_menu","Delete","menu_bar",0)
tde4.addMenuButtonWidget(req,"delete_all_menu_widget","Delete all offset curves keys","delete_menu")
tde4.addMenuButtonWidget(req,"delete_frame_all_menu_widget","Delete current frame all offset curves keys","delete_menu")

#add merge menu...
tde4.addMenuWidget(req,"merge_menu","Merge","menu_bar",0)
tde4.addMenuButtonWidget(req,"merge_offset_curves_widget","Merge offset curves","merge_menu")

#add curve are widget...
tde4.addCurveAreaWidget(req,"curves_area","",100)
tde4.setWidgetAttachModes(req,"curves_area","ATTACH_WINDOW","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_WINDOW")
tde4.setWidgetOffsets(req,"curves_area",5,85,-1000,30)

#display selected PGroup text field widget...
tde4.addTextFieldWidget(req,"pg_name_txt","Selected PGroup","")
tde4.setWidgetSensitiveFlag(req,"pg_name_txt",0)
tde4.setWidgetAttachModes(req,"pg_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pg_name_txt",33,65,2,0)
tde4.setWidgetValue(req,"pg_name_txt",str(tde4.getPGroupName(tde4.getCurrentPGroup())))

if tde4.getPGroupType(tde4.getCurrentPGroup()) == "CAMERA":
	#add update objpg toggle button...
	tde4.addToggleWidget(req,"update_objpg_toggle","Update ObjectPGroup(s) along with Camera",1)
	tde4.setWidgetAttachModes(req,"update_objpg_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"update_objpg_toggle",93,95,2,0)

#add list widget...
tde4.addListWidget(req,"curves_list","",1,80)
tde4.setWidgetLinks(req,"curves_list","curves_area","","curves_area","curves_area")
tde4.setWidgetAttachModes(req,"curves_list","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_WINDOW")
tde4.setWidgetOffsets(req,"curves_list",5,5,0,5)

#insert list widget items...
tde4.insertListWidgetItem(req,"curves_list","Position X",0)
tde4.insertListWidgetItem(req,"curves_list","Position Y",1)
tde4.insertListWidgetItem(req,"curves_list","Position Z",2)
tde4.insertListWidgetItem(req,"curves_list","Rotation X",3)
tde4.insertListWidgetItem(req,"curves_list","Rotation Y",4)
tde4.insertListWidgetItem(req,"curves_list","Rotation Z",5)
tde4.insertListWidgetItem(req,"curves_list","Focal",6)
tde4.insertListWidgetItem(req,"curves_list","offset Position X",7)
tde4.insertListWidgetItem(req,"curves_list","offset Position Y",8)
tde4.insertListWidgetItem(req,"curves_list","offset Position Z",9)
tde4.insertListWidgetItem(req,"curves_list","offset Rotation X",10)
tde4.insertListWidgetItem(req,"curves_list","offset Rotation Y",11)
tde4.insertListWidgetItem(req,"curves_list","offset Rotation Z",12)
tde4.insertListWidgetItem(req,"curves_list","offset Focal",13)


#update offset curves button widget...
tde4.addButtonWidget(req,"update_offset_curves_btn","Update Offset Curves/Viewport",220,5)
tde4.setWidgetLinks(req,"update_offset_curves_btn","","","curves_area","")

"""
#bake offset curves button widget...
tde4.addButtonWidget(req,"bake_offset_curves_btn","Merge Offset Curves",160,5)
tde4.setWidgetLinks(req,"bake_offset_curves_btn","update_offset_curves_btn","","curves_area","")
tde4.setWidgetOffsets(req,"bake_offset_curves_btn",170,0,5,0)
"""

#add create keys button widget...
tde4.addButtonWidget(req,"create_keys_btn","Create Offset Keys",150,5)
tde4.setWidgetLinks(req,"create_keys_btn","update_offset_curves_btn","","curves_area","")
tde4.setWidgetOffsets(req,"create_keys_btn",240,0,5,0)

#add zero keys button widget...
tde4.addButtonWidget(req,"zero_keys_btn","Create Zero Offset Keys",160,5)
tde4.setWidgetLinks(req,"zero_keys_btn","create_keys_btn","","curves_area","")
tde4.setWidgetOffsets(req,"zero_keys_btn",410,0,5,0)

"""
#delete all offset curves keys button widget...
tde4.addButtonWidget(req,"delete_keys_btn","Delete All Offset Keys",170,5)
tde4.setWidgetLinks(req,"delete_keys_btn","bake_offset_curves_btn","","curves_area","")
tde4.setWidgetOffsets(req,"delete_keys_btn",483,0,5,0)
"""

#add key- button widget...
tde4.addButtonWidget(req,"key-","Previous Key",90,5)
tde4.setWidgetLinks(req,"key-","zero_keys_btn","","curves_area","")
tde4.setWidgetOffsets(req,"key-",720,0,5,0)

#add key+ button widget...
tde4.addButtonWidget(req,"key+","Next Key",75,5)
tde4.setWidgetLinks(req,"key+","key-","","curves_area","")
tde4.setWidgetOffsets(req,"key+",820,0,5,0)

#add view all button...
tde4.addButtonWidget(req,"view_all","View All",70,5)
tde4.setWidgetLinks(req,"view_all","key+","","curves_area","")
tde4.setWidgetOffsets(req,"view_all",915,0,5,0)

#create curves...
pos_x_curve = tde4.createCurve()
pos_y_curve = tde4.createCurve()
pos_z_curve = tde4.createCurve()
rot_x_curve = tde4.createCurve()
rot_y_curve = tde4.createCurve()
rot_z_curve = tde4.createCurve()
focal_curve = tde4.createCurve()
pos_x_offset_curve = tde4.createCurve()
pos_y_offset_curve = tde4.createCurve()
pos_z_offset_curve = tde4.createCurve()
rot_x_offset_curve = tde4.createCurve()
rot_y_offset_curve = tde4.createCurve()
rot_z_offset_curve = tde4.createCurve()
focal_offset_curve = tde4.createCurve()

Bake_Buffer_Curves()
Update_Base_Curves()

tde4.detachCurveAreaWidgetAllCurves(req,"curves_area")
tde4.attachCurveAreaWidgetCurve(req,"curves_area",pos_x_curve,1.0,0.4,0.4,1)
tde4.setCurveAreaWidgetXOffset(req,"curves_area",frame_offset-1)

tde4.setWidgetCallbackFunction(req,"curves_area","Curvearea_Callback")
tde4.setWidgetCallbackFunction(req,"curves_list","Main_Callback")
tde4.setWidgetCallbackFunction(req,"create_keys_btn","Create_Keys")
tde4.setWidgetCallbackFunction(req,"zero_keys_btn","Create_Keys")

tde4.setWidgetCallbackFunction(req,"delete_frame_all_menu_widget","Delete_Keys")
tde4.setWidgetCallbackFunction(req,"menu_bar","Editmenu_Callback")
tde4.setWidgetCallbackFunction(req,"merge_offset_curves_widget","Main_Callback")
tde4.setWidgetCallbackFunction(req,"update_offset_curves_btn","Main_Callback")
tde4.setWidgetCallbackFunction(req,"key-","Main_Callback")
tde4.setWidgetCallbackFunction(req,"key+","Main_Callback")
tde4.setWidgetCallbackFunction(req,"jump_previous_key","Main_Callback")
tde4.setWidgetCallbackFunction(req,"jump_next_key","Main_Callback")
tde4.setWidgetCallbackFunction(req,"delete_all_menu_widget","Main_Callback")
tde4.setWidgetCallbackFunction(req,"view_all","Main_Callback")
tde4.setWidgetCallbackFunction(req,"view_all_menu_widget","Main_Callback")

tde4.postCustomRequesterAndContinue(req,window_title,1200,800,"Cursor_Update")
tde4.updateGUI()
tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
