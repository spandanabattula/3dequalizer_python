# 3DE4.script.name: 3DModel Animation Curve Editor...
# 3DE4.script.version: v1.0
# 3DE4.script.gui: Lineup Controls::Edit
# 3DE4.script.gui: Orientation Controls::Edit
# 3DE4.script.gui.button: Lineup Controls::3DModel Anim, align-bottom-left, 80,20
# 3DE4.script.gui.button: Orientation Controls::3DModel Anim, align-bottom-left, 70,20
# 3DE4.script.comment:	This script allows user to animate 3DModels inside of 3DE.
# 3DE4.script.gui.config_menus: true
# Patcha Saheb(patchasaheb@gmail.com)
# 10 Oct 2017.

from vl_sdv import*
import math

pg = tde4.getCurrentPGroup()
pg_type = tde4.getPGroupType(pg)
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
frames = tde4.getCameraNoFrames(cam)
frame_offset = tde4.getCameraFrameOffset(cam)
mlist = tde4.get3DModelList(pg,1)
window_title = "Patcha 3DModel Animation Curve Editor v1.0"

def Realtime_Update(req):
	pg = tde4.getCurrentPGroup()
	mlist = tde4.get3DModelList(pg,0)
	model_name_txt = str(tde4.getWidgetValue(anim_req,"model_name_txt"))
	for model in mlist:
		if tde4.get3DModelName(pg,model) == model_name_txt:
			break

	#cursor update...
	frame = tde4.getCurrentFrame(tde4.getCurrentCamera())
	tde4.setCurveAreaWidgetCursorPosition(anim_req,"curves_area",frame,1)

	if tde4.getWidgetValue(anim_req,"live_update_toggle") == 1:
		#3DModel visibility live update to viewport...
		visibility_curve_y = tde4.evaluateCurve(visibility_curve,frame)
		if visibility_curve_y == 0:
			tde4.set3DModelVisibleFlag(pg,model,0)
		if visibility_curve_y == 1:
			tde4.set3DModelVisibleFlag(pg,model,1)
		tde4.updateGUI(1)

		#position curves live update to viewport...
		pos_x_curve_y = tde4.evaluateCurve(pos_x_curve,frame)	
		pos_y_curve_y = tde4.evaluateCurve(pos_y_curve,frame)	
		pos_z_curve_y = tde4.evaluateCurve(pos_z_curve,frame)
		tde4.set3DModelPosition3D(pg,model,[pos_x_curve_y,pos_y_curve_y,pos_z_curve_y])

		#rotation and scale curves live update to viewport...
		rot_x_curve_y = tde4.evaluateCurve(rot_x_curve,frame) * math.pi /180.0	
		rot_y_curve_y = tde4.evaluateCurve(rot_y_curve,frame) * math.pi /180.0	
		rot_z_curve_y = tde4.evaluateCurve(rot_z_curve,frame) * math.pi /180.0
		rot_Matrix = mat3d(rot3d(rot_x_curve_y,rot_y_curve_y,rot_z_curve_y,VL_APPLY_ZXY))
		m = mat3d(tde4.get3DModelRotationScale3D(pg,model))
		uniform_scale_curve_y = tde4.evaluateCurve(uniform_scale_curve,frame)
		scale_Matrix = mat3d(uniform_scale_curve_y,0.0,0.0,0.0,uniform_scale_curve_y,0.0,0.0,0.0,uniform_scale_curve_y)
		f = rot_Matrix * scale_Matrix					
		tde4.set3DModelRotationScale3D(pg,model,f.list())

def Curvearea_Callback(req,widget,action):
	cam = tde4.getCurrentCamera()
	if action==3 or action==2:
		f = tde4.getCurveAreaWidgetCursorPosition(anim_req,"curves_area")
		n = tde4.getCameraNoFrames(cam)
		if f < 1: f = 1
		if f > n: f = 1
		tde4.setCurrentFrame(cam,int(f))

def Editmenu_Callback(req,widget,action):
	if widget == "delete_cvs":
		curve_list = tde4.getCurveAreaWidgetCurveList(anim_req,"curves_area")
		for curve in curve_list:
			keylist = tde4.getCurveKeyList(curve,1)
			for key in keylist:
				tde4.deleteCurveKey(curve,key)
			tde4.updateGUI(1)

	if widget == "set_linear" or widget == "set_smooth" or widget == "set_broken":
		mode = widget[4:10].upper()
		curve_list = tde4.getCurveAreaWidgetCurveList(anim_req,"curves_area")		
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
		curve_list = tde4.getCurveAreaWidgetCurveList(anim_req,"curves_area")		
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
		curve_list = tde4.getCurveAreaWidgetCurveList(anim_req,"curves_area")		
		for curve in curve_list:
			keylist = tde4.getCurveKeyList(curve,1)
			for key in keylist:
				tde4.setCurveKeyFixedXFlag(curve,key,flag)
		tde4.updateGUI(1)

def Create_Update_Anim_Keys(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	model_name_txt = str(tde4.getWidgetValue(anim_req,"model_name_txt"))
	for model in mlist:
		if tde4.get3DModelName(pg,model) == model_name_txt:
			break

	#visibility curve update...
	vis_status = tde4.get3DModelVisibleFlag(pg,model)
	key = tde4.createCurveKey(visibility_curve,[frame,int(vis_status)])
	tde4.setCurveKeyFixedXFlag(visibility_curve,key,1)
	tde4.setCurveKeyMode(visibility_curve,key,"LINEAR")

	#position curves update...
	pos3d = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
	key = tde4.createCurveKey(pos_x_curve,[frame,float(pos3d[0])])
	tde4.setCurveKeyFixedXFlag(pos_x_curve,key,1)
	tde4.setCurveKeyMode(pos_x_curve,key,"LINEAR")
	key = tde4.createCurveKey(pos_y_curve,[frame,float(pos3d[1])])
	tde4.setCurveKeyFixedXFlag(pos_y_curve,key,1)
	tde4.setCurveKeyMode(pos_y_curve,key,"LINEAR")
	key = tde4.createCurveKey(pos_z_curve,[frame,float(pos3d[2])])
	tde4.setCurveKeyFixedXFlag(pos_z_curve,key,1)
	tde4.setCurveKeyMode(pos_z_curve,key,"LINEAR")

	#rotation curves update...
	r3d = mat3d(tde4.get3DModelRotationScale3D(pg,model))
	s0 = vec3d(r3d[0][0],r3d[1][0],r3d[2][0]).norm2()
	s1 = vec3d(r3d[0][1],r3d[1][1],r3d[2][1]).norm2()
	s2 = vec3d(r3d[0][2],r3d[1][2],r3d[2][2]).norm2()
	m_rot = r3d * mat3d(1.0/s0,0.0,0.0,0.0,1.0/s1,0.0,0.0,0.0,1.0/s2)
	phi_x,phi_y,phi_z = rot3d(m_rot).angles(VL_APPLY_ZXY)
	phi_x = phi_x * 180.0 / math.pi
	phi_y = phi_y * 180.0 / math.pi
	phi_z = phi_z * 180.0 / math.pi
	key = tde4.createCurveKey(rot_x_curve,[frame,float(phi_x)])
	tde4.setCurveKeyFixedXFlag(rot_x_curve,key,1)
	tde4.setCurveKeyMode(rot_x_curve,key,"LINEAR")
	key = tde4.createCurveKey(rot_y_curve,[frame,float(phi_y)])
	tde4.setCurveKeyFixedXFlag(rot_y_curve,key,1)
	tde4.setCurveKeyMode(rot_y_curve,key,"LINEAR")
	key = tde4.createCurveKey(rot_z_curve,[frame,float(phi_z)])
	tde4.setCurveKeyFixedXFlag(rot_z_curve,key,1)
	tde4.setCurveKeyMode(rot_z_curve,key,"LINEAR")

	#scale curve update..
	key = tde4.createCurveKey(uniform_scale_curve,[frame,float(s0)])
	tde4.setCurveKeyFixedXFlag(uniform_scale_curve,key,1)
	tde4.setCurveKeyMode(uniform_scale_curve,key,"LINEAR")

def Min_Max(keylist,curve):
	keylist = tde4.getCurveKeyList(curve,0)
	x = []
	y = []
	for key in keylist:
		pos_2d = tde4.getCurveKeyPosition(curve,key)
		x.append(pos_2d[0])
		y.append(pos_2d[1])
	return min(x),max(x),min(y),max(y)

def Anim_Main_Callback(req,widget,action):
	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(tde4.getCurrentCamera())	
	if widget == "curves_list":
		tde4.detachCurveAreaWidgetAllCurves(anim_req,"curves_area")		
		if tde4.getListWidgetItemSelectionFlag(anim_req,"curves_list",0):
			curve = pos_x_curve
			keylist = tde4.getCurveKeyList(pos_x_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",pos_x_curve,1.0,0.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",pos_x_curve,1.0,0.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",1):
			curve = pos_y_curve
			keylist = tde4.getCurveKeyList(pos_y_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",pos_y_curve,0.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",pos_y_curve,0.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(anim_req,"curves_list",2):
			curve = pos_z_curve
			keylist = tde4.getCurveKeyList(pos_z_curve,0)
			if len(keylist) >= 1:			
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",pos_z_curve,0.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",pos_z_curve,0.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(anim_req,"curves_list",3):
			curve = rot_x_curve
			keylist = tde4.getCurveKeyList(rot_x_curve,0)
			if len(keylist) >= 1:			
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",rot_x_curve,0.0,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",rot_x_curve,0.0,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(anim_req,"curves_list",4):
			curve = rot_y_curve
			keylist = tde4.getCurveKeyList(rot_y_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",rot_y_curve,1.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",rot_y_curve,1.0,0.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)				
		if tde4.getListWidgetItemSelectionFlag(anim_req,"curves_list",5):
			curve = rot_z_curve
			keylist = tde4.getCurveKeyList(rot_z_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",rot_z_curve,1.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",rot_z_curve,1.0,1.0,0.0,1)
				tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",6):
			curve = uniform_scale_curve
			keylist = tde4.getCurveKeyList(uniform_scale_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",uniform_scale_curve,1.0,0.3,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",uniform_scale_curve,1.0,0.3,0.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)
		if tde4.getListWidgetItemSelectionFlag(req,"curves_list",7):
			curve = visibility_curve
			keylist = tde4.getCurveKeyList(visibility_curve,0)
			if len(keylist) >= 1:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",visibility_curve,1.0,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1,frames,Min_Max(keylist,curve)[2]-0.1,Min_Max(keylist,curve)[3]+0.1)
			else:
				tde4.attachCurveAreaWidgetCurve(req,"curves_area",visibility_curve,1.0,1.0,1.0,1)
				tde4.setCurveAreaWidgetDimensions(req,"curves_area",1.0,frames,-0.2,1.0)

	if widget == "view_all" or widget == "view_all_menu_widget":
		y = []
		curves_list = tde4.getCurveAreaWidgetCurveList(anim_req,"curves_area")
		for curve in curves_list:
			keylist = tde4.getCurveKeyList(curve,0)
			for key in keylist:
				pos_2d = tde4.getCurveKeyPosition(curve,key)
				y.append(pos_2d[1])
		if len(y) > 0:
			tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,min(y)-0.1,max(y)+0.1)
		else:
			tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)

	if widget == "key-" or widget == "key+" or widget == "jump_previous_key" or widget == "jump_next_key":
		curve_list = tde4.getCurveAreaWidgetCurveList(anim_req,"curves_area")
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
				tde4.setCurveAreaWidgetCursorPosition(anim_req,"curves_area",tde4.getCurrentFrame(cam))
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
				tde4.setCurveAreaWidgetCursorPosition(anim_req,"curves_area",tde4.getCurrentFrame(cam))

	if widget == "delete_keys_btn":
		tde4.deleteAllCurveKeys(pos_x_curve)
		tde4.deleteAllCurveKeys(pos_y_curve)
		tde4.deleteAllCurveKeys(pos_z_curve)
		tde4.deleteAllCurveKeys(rot_x_curve)
		tde4.deleteAllCurveKeys(rot_y_curve)
		tde4.deleteAllCurveKeys(rot_z_curve)
		tde4.deleteAllCurveKeys(uniform_scale_curve)		
		tde4.deleteAllCurveKeys(visibility_curve)

if pg_type == "CAMERA":
	if len(mlist) == 1:
		anim_req = tde4.createCustomRequester()
		#add menu bar widget...
		tde4.addMenuBarWidget(anim_req,"menu_bar")
		tde4.setWidgetAttachModes(anim_req,"menu_bar","ATTACH_WINDOW","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
		tde4.setWidgetOffsets(anim_req,"menu_bar",2,20,2,0)

		#add edit menu...
		tde4.addMenuWidget(anim_req,"edit_menu","Edit","menu_bar",0)
		tde4.addMenuButtonWidget(anim_req,"delete_cvs","Delete CVs","edit_menu")
		tde4.setWidgetShortcut(anim_req,"delete_cvs",8)
		tde4.addMenuSeparatorWidget(anim_req,"sep1","edit_menu")
		tde4.addMenuWidget(anim_req,"set_cvs_menu","Set CVs To","edit_menu")
		tde4.addMenuButtonWidget(anim_req,"set_linear","Linear","set_cvs_menu")
		tde4.setWidgetShortcut(anim_req,"set_linear",108)
		tde4.addMenuButtonWidget(anim_req,"set_smooth","Smooth","set_cvs_menu")
		tde4.setWidgetShortcut(anim_req,"set_smooth",115)
		tde4.addMenuButtonWidget(anim_req,"set_broken","Broken","set_cvs_menu")
		tde4.setWidgetShortcut(anim_req,"set_broken",98)
		tde4.addMenuButtonWidget(anim_req,"flatten","Flatten Tangents","edit_menu")
		tde4.addMenuButtonWidget(anim_req,"fix_cvs","Fix CVs Vertically","edit_menu")
		tde4.addMenuButtonWidget(anim_req,"unfix_cvs","Unfix CVs Vertically","edit_menu")
		tde4.addMenuButtonWidget(anim_req,"jump_previous_key","Jump to Previous Key","edit_menu")
		tde4.setWidgetShortcut(anim_req,"jump_previous_key",3018)
		tde4.addMenuButtonWidget(anim_req,"jump_next_key","Jump to Next Key","edit_menu")
		tde4.setWidgetShortcut(anim_req,"jump_next_key",3019)

		#add view menu...
		tde4.addMenuWidget(anim_req,"view_menu","View","menu_bar",0)
		tde4.addMenuButtonWidget(anim_req,"view_all_menu_widget","View All","view_menu")
		tde4.setWidgetShortcut(anim_req,"view_all_menu_widget",32)

		#add curve are widget...
		tde4.addCurveAreaWidget(anim_req,"curves_area","",100)
		tde4.setWidgetAttachModes(anim_req,"curves_area","ATTACH_WINDOW","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_WINDOW")
		tde4.setWidgetOffsets(anim_req,"curves_area",5,85,-1000,30)

		#display selected 3DModel text field widget...
		tde4.addTextFieldWidget(anim_req,"model_name_txt","Selected 3DModel","")
		tde4.setWidgetSensitiveFlag(anim_req,"model_name_txt",0)
		tde4.setWidgetAttachModes(anim_req,"model_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(anim_req,"model_name_txt",35,65,2,0)
		tde4.setWidgetValue(anim_req,"model_name_txt",str(tde4.get3DModelName(pg,mlist[0])))
		tde4.set3DModelSelectionFlag(pg,mlist[0],0)
		

		#add live update toggle widget...
		live_toggle = tde4.addToggleWidget(anim_req,"live_update_toggle","Viewport Realtime live update",0)
		tde4.setWidgetAttachModes(anim_req,"live_update_toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(anim_req,"live_update_toggle",85,87,2,0)

		#add list widget...
		tde4.addListWidget(anim_req,"curves_list","",1,80)
		tde4.setWidgetLinks(anim_req,"curves_list","curves_area","","curves_area","curves_area")
		tde4.setWidgetAttachModes(anim_req,"curves_list","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_WINDOW")
		tde4.setWidgetOffsets(anim_req,"curves_list",5,5,0,5)

		#insert list widget items...
		tde4.insertListWidgetItem(anim_req,"curves_list","Position X",0)
		tde4.insertListWidgetItem(anim_req,"curves_list","Position Y",1)
		tde4.insertListWidgetItem(anim_req,"curves_list","Position Z",2)
		tde4.insertListWidgetItem(anim_req,"curves_list","Rotation X",3)
		tde4.insertListWidgetItem(anim_req,"curves_list","Rotation Y",4)
		tde4.insertListWidgetItem(anim_req,"curves_list","Rotation Z",5)
		tde4.insertListWidgetItem(anim_req,"curves_list","Uniform Scale",6)
		tde4.insertListWidgetItem(anim_req,"curves_list","Visibility",7)

		#create/update animation curves button widget...
		tde4.addButtonWidget(anim_req,"create_update_anim_curves_btn","Create/Update Anim Curves Keys",240,5)
		tde4.setWidgetLinks(anim_req,"create_update_anim_curves_btn","","","curves_area","")

		#delete all anim curves keys button widget...
		tde4.addButtonWidget(anim_req,"delete_keys_btn","Delete all Anim Curves Keys",210,5)
		tde4.setWidgetLinks(anim_req,"delete_keys_btn","create_update_anim_curves_btn","","curves_area","")
		tde4.setWidgetOffsets(anim_req,"delete_keys_btn",260,0,5,0)

		#add key- button widget...
		tde4.addButtonWidget(anim_req,"key-","Previous Key",90,5)
		tde4.setWidgetLinks(anim_req,"key-","create_update_anim_curves_btn","","curves_area","")
		tde4.setWidgetOffsets(anim_req,"key-",500,0,5,0)

		#add key+ button widget...
		tde4.addButtonWidget(anim_req,"key+","Next Key",75,5)
		tde4.setWidgetLinks(anim_req,"key+","key-","","curves_area","")
		tde4.setWidgetOffsets(anim_req,"key+",605,0,5,0)

		#add view all button...
		tde4.addButtonWidget(anim_req,"view_all","View All",70,5)
		tde4.setWidgetLinks(anim_req,"view_all","key+","","curves_area","")
		tde4.setWidgetOffsets(anim_req,"view_all",695,0,5,0)
		#create curves...
		pos_x_curve = tde4.createCurve()
		pos_y_curve = tde4.createCurve()
		pos_z_curve = tde4.createCurve()
		rot_x_curve = tde4.createCurve()
		rot_y_curve = tde4.createCurve()
		rot_z_curve = tde4.createCurve()
		uniform_scale_curve = tde4.createCurve()
		visibility_curve = tde4.createCurve()

		tde4.detachCurveAreaWidgetAllCurves(anim_req,"curves_area")
		tde4.attachCurveAreaWidgetCurve(anim_req,"curves_area",pos_x_curve,1.0,0.4,0.4,1)
		tde4.setCurveAreaWidgetXOffset(anim_req,"curves_area",frame_offset-1)

		tde4.setWidgetCallbackFunction(anim_req,"curves_list","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"create_update_anim_curves_btn","Create_Update_Anim_Keys")
		tde4.setWidgetCallbackFunction(anim_req,"view_all","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"view_all_menu_widget","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"curves_area","Curvearea_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"key-","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"key+","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"jump_previous_key","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"jump_next_key","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"delete_keys_btn","Anim_Main_Callback")
		tde4.setWidgetCallbackFunction(anim_req,"menu_bar","Editmenu_Callback")

		tde4.postCustomRequesterAndContinue(anim_req,window_title,1200,800,"Realtime_Update")
		tde4.updateGUI()
		tde4.setCurveAreaWidgetDimensions(anim_req,"curves_area",1.0,frames,-0.2,1.0)		

	else:
		tde4.postQuestionRequester(window_title,"Error, exactly one 3DModel must be selected.","Ok")
else:
	tde4.postQuestionRequester(window_title,"Error, only 'CAMERA PGroup' 3DModels can be animated.","Ok")