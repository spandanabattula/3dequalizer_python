# 3DE4.script.name:	3DModel Grid Creator...
# 3DE4.script.version:	v1.0b1
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.gui:	Orientation Controls::Edit
# 3DE4.script.gui.button:	Lineup Controls::Grid 3DModels, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::Grid 3DModels, align-bottom-left, 70, 20
# 3DE4.script.comment:create 3dmodels in row column layout.
#
#Patcha Saheb(patchasaheb@gmail.com)
#04-Jan-2016.
#
#import 3DModel
#give camera rotation y value
#calculate centroid of all 3DModels positions
#get distance vector from centroid to camera
#add distance vector to 3DModels positions

from vl_sdv import *

window_title = "Patcha 3DModel Grid Creator v1.0b1"

def Models_List():
	l = []
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	for model in mlist:
		name = tde4.get3DModelName(pg,model)
		if name.startswith("Grid_3DModel") == True:
			l.append(model)
	return l

def Toggle_Polygons(req,widget,action):
	pg	= tde4.getCurrentPGroup()
	v = tde4.getWidgetValue(req,"toggle")
	if v == 1:
		for model in Models_List():
			tde4.set3DModelRenderingFlags(pg,model,1,1,1)
	if v == 0:
		for model in Models_List():
			tde4.set3DModelRenderingFlags(pg,model,1,1,0)		


def Delete_temp():
	pg	= tde4.getCurrentPGroup()
	for model in Models_List():
		name = tde4.get3DModelName(pg,model)
		if name.startswith("Grid_3DModel") == True:
			tde4.delete3DModel(pg,model)

def Delete_All(req,widget,action):
	Delete_temp()

def Select_All(req,widget,action):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	for model in mlist:
		tde4.set3DModelSelectionFlag(pg,model,0)
	for model in Models_List():
		tde4.set3DModelSelectionFlag(pg,model,1)

def Deselect_All(req,widget,action):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	for model in mlist:
		tde4.set3DModelSelectionFlag(pg,model,0)

def Color(req,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	alp = tde4.getWidgetValue(req,"alpha_slider")
	for m in Models_List():
		if tde4.getWidgetValue(req,"red") == 1:
			tde4.set3DModelColor(pg,m,1.0,0.0,0.0,alp)
		if tde4.getWidgetValue(req,"green") == 1:
			tde4.set3DModelColor(pg,m,0.0,1.0,0.0,alp)		
		if tde4.getWidgetValue(req,"blue") == 1:
			tde4.set3DModelColor(pg,m,0.0,0.0,1.0,alp)				
		if tde4.getWidgetValue(req,"purple") == 1:
			tde4.set3DModelColor(pg,m,1.0,0.0,1.0,alp)
		if tde4.getWidgetValue(req,"yellow") == 1:
			tde4.set3DModelColor(pg,m,1.0,1.0,0.0,alp)
		if tde4.getWidgetValue(req,"black") == 1:
			tde4.set3DModelColor(pg,m,0.0,0.0,0.0,alp)	
		if tde4.getWidgetValue(req,"white") == 1:
			tde4.set3DModelColor(pg,m,1.0,1.0,1.0,alp)
		if tde4.getWidgetValue(req,"cyan") == 1:
			tde4.set3DModelColor(pg,m,0.22,0.45,0.65,alp)

def Create_3DModels(req,widget,action):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	path	= tde4.getWidgetValue(req,"file_browser")
	No_of_rows = int(tde4.getWidgetValue(req,"rows"))
	No_of_columns = int(tde4.getWidgetValue(req,"columns"))
	distance = float(tde4.getWidgetValue(req,"distance"))
	cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
	cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
	rot	= rot3d(mat3d(cam_rot)).angles(VL_APPLY_ZXY)
	rx	= (rot[0]*180.0)/3.141592654
	ry	= (rot[1]*180.0)/3.141592654
	rz	= (rot[2]*180.0)/3.141592654
	if path != None and No_of_rows != None and No_of_columns != None and distance != None:
		Delete_temp()
		for number_of_sphere in range(No_of_columns):
			count1 = 0
			count2 = 0
			for row in range(No_of_rows):
				for column in range(No_of_columns):
					if count1 == column and row == 0:						
						model = tde4.create3DModel(pg,10)
						tde4.set3DModelName(pg,model,"Grid_3DModel")
						tde4.importOBJ3DModel(pg,model,path)												
						tde4.set3DModelPosition3D(pg,model,[0.0,float(distance * number_of_sphere),0.0])
					else:
						if count1 == row and column == 0:
							model = tde4.create3DModel(pg,10)
							tde4.set3DModelName(pg,model,"Grid_3DModel")
							tde4.importOBJ3DModel(pg,model,path)							
							tde4.set3DModelPosition3D(pg,model,[(distance * column), (distance * number_of_sphere), (distance * count1)])
							count2 = count2 + 1
						else:
							model = tde4.create3DModel(pg,10)
							tde4.set3DModelName(pg,model,"Grid_3DModel")
							tde4.importOBJ3DModel(pg,model,path)							
							tde4.set3DModelPosition3D(pg,model,[(distance * column), (distance * number_of_sphere), (distance * count2)])
				count1 = count1 + 1
		#bring 3dmodels infront of the camera...
		l = []
		mlist = tde4.get3DModelList(pg,0)
		for m in mlist:
			name = tde4.get3DModelName(pg,m)
			if name.startswith("Grid_3DModel") == True:
				l.append(m)	
		x_list = []
		y_list = []
		z_list = []
		for model in l:
			pos = tde4.get3DModelPosition3D(pg,model,cam,frame)
			x_list.append(pos[0])
			y_list.append(pos[1])
			z_list.append(pos[2])
		x = sum(x_list) / len(x_list)
		y = sum(y_list) / len(y_list)
		z = sum(z_list) / len(z_list)
		centroid = vec3d(x,y,z)
		diff = cam_pos - centroid
		for model in l:
			pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
			new_pos = pos + diff
			tde4.set3DModelPosition3D(pg,model,new_pos.list())
		for model in l:	
			#Convert to Angles...
			rot_x = 0.0 *  math.pi /180.0
			rot_y = ry *  math.pi /180.0
			rot_z = 0.0 *  math.pi /180.0
			rot_Matrix = mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))
			m = mat3d(tde4.get3DModelRotationScale3D(pg,model))
			s0 = vec3d(m[0][0],m[1][0],m[2][0]).norm2()
			s1 = vec3d(m[0][1],m[1][1],m[2][1]).norm2()
			s2 = vec3d(m[0][2],m[1][2],m[2][2]).norm2()
			scale_Matrix = mat3d(1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0)
			f = rot_Matrix * scale_Matrix					
			tde4.set3DModelRotationScale3D(pg,model,f.list())
		#rotate all 3dmodels around camera to match camera y rotation orientation...
		"""pivot = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
		for model in l:
			model_pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
			rx = 0.0
			ry = pivot[1]
			rz = 0.0
			rx *= math.pi / 180.0
			ry *= math.pi / 180.0
			rz *= math.pi / 180.0
			new_pos = rot3d(rx,ry,rz,VL_APPLY_ZXY) * (model_pos - pivot) + pivot
			tde4.set3DModelPosition3D(pg,model,new_pos.list())"""
	else:
		tde4.postQuestionRequester(window_title,"Error, please enter proper values in all fields.","Ok")

def Translate(req,widget,action):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	x = float(tde4.getWidgetValue(req,"posx"))
	y = float(tde4.getWidgetValue(req,"posy"))
	z = float(tde4.getWidgetValue(req,"posz"))
	for model in Models_List():
		pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
		rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
		rot1 = mat3d(rot).trans()
		x_axis = vec3d(rot1[0]).unit()
		y_axis = vec3d(rot1[1]).unit()
		z_axis = vec3d(rot1[2]).unit()
		x_v = x_axis * float(x)
		y_v = y_axis * float(y)
		z_v = z_axis * float(z)	
		pos = vec3d(x_v) + vec3d(pos)
		tde4.set3DModelPosition3D(pg,model,pos.list())
		pos = vec3d(y_v) + vec3d(pos)
		tde4.set3DModelPosition3D(pg,model,pos.list())
		pos = vec3d(z_v) + vec3d(pos)
		tde4.set3DModelPosition3D(pg,model,pos.list())

def Rotate_Scale(req,widget,action):
	pg	= tde4.getCurrentPGroup()
	cam     = tde4.getCurrentCamera()
	frame   = tde4.getCurrentFrame(cam)
	rx = float(tde4.getWidgetValue(req,"rotx"))
	ry = float(tde4.getWidgetValue(req,"roty"))
	rz = float(tde4.getWidgetValue(req,"rotz"))
	s_v = float(tde4.getWidgetValue(req,"scale_factor"))
	rot_x = rx *  math.pi /180.0
	rot_y = ry *  math.pi /180.0
	rot_z = rz *  math.pi /180.0
	if widget == "scale_button":
		for model in Models_List():
			m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
			rot_Matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
			scale_Matrix = mat3d(s_v,0.0,0.0,0.0,s_v,0.0,0.0,0.0,s_v)
			f = rot_Matrix * scale_Matrix
			tde4.set3DModelRotationScale3D(pg,model,f.list())
	if widget == "rot":
		pivot = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
		for model in Models_List():
			model_pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
			rx = float(tde4.getWidgetValue(req,"rotx"))
			ry = float(tde4.getWidgetValue(req,"roty"))
			rz = float(tde4.getWidgetValue(req,"rotz"))
			rx *= math.pi / 180.0
			ry *= math.pi / 180.0
			rz *= math.pi / 180.0
			new_pos = rot3d(rx,ry,rz,VL_APPLY_ZXY) * (model_pos - pivot) + pivot
			tde4.set3DModelPosition3D(pg,model,new_pos.list())

#build GUI...
req = tde4.createCustomRequester()
tde4.addMenuBarWidget(req,"menu_bar")
tde4.setWidgetAttachModes(req,"menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"menu_bar",0,100,1,0)
#color menu
tde4.addMenuWidget(req,"color_menu","Color","menu_bar",1)
tde4.addMenuToggleWidget(req,"red","Red","color_menu",0)
tde4.addMenuToggleWidget(req,"green","Green","color_menu",0)
tde4.addMenuToggleWidget(req,"blue","Blue","color_menu",0)
tde4.addMenuToggleWidget(req,"purple","Purple","color_menu",0)
tde4.addMenuToggleWidget(req,"yellow","Yellow","color_menu",0)
tde4.addMenuToggleWidget(req,"black","Black","color_menu",0)
tde4.addMenuToggleWidget(req,"white","White","color_menu",0)
tde4.addMenuToggleWidget(req,"cyan","Cyan","color_menu",1)
#add file widget...
tde4.addFileWidget(req,"file_browser","Browse...","*.obj","/u/pbb/sphere.obj")
tde4.setWidgetAttachModes(req,"file_browser","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"file_browser",15,98,30,0)
#add sep widget...
tde4.addSeparatorWidget(req,"sep")
tde4.setWidgetAttachModes(req,"sep","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sep",2,98,50,0)
#rows widget...
tde4.addTextFieldWidget(req,"rows","No of Rows","3")
tde4.setWidgetAttachModes(req,"rows","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rows",16,26,70,0)	
#columns widget...
tde4.addTextFieldWidget(req,"columns","No of Columns","3")
tde4.setWidgetAttachModes(req,"columns","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"columns",47,57,70,0)
#distance b/w 3dmodels widget...
tde4.addTextFieldWidget(req,"distance","Distance b/w 3DModels","5")
tde4.setWidgetAttachModes(req,"distance","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"distance",88,98,70,0)
#create button widget...
tde4.addButtonWidget(req,"create","Create",70,10)
tde4.setWidgetAttachModes(req,"create","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"create",10,25,100,0)
#select all button widget...
tde4.addButtonWidget(req,"select_all","Select All",70,10)
tde4.setWidgetAttachModes(req,"select_all","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"select_all",30,45,100,0)
#deselect all button widget...
tde4.addButtonWidget(req,"deselect_all","Deselect All",70,10)
tde4.setWidgetAttachModes(req,"deselect_all","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"deselect_all",50,65,100,0)
#delete all button widget...
tde4.addButtonWidget(req,"delete_all","Delete All",70,10)
tde4.setWidgetAttachModes(req,"delete_all","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"delete_all",70,85,100,0)
#add sep1 widget...
tde4.addSeparatorWidget(req,"sep1")
tde4.setWidgetAttachModes(req,"sep1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sep1",2,98,120,0)
#add translate text boxes and button widgets...
tde4.addTextFieldWidget(req,"posx","X","0.0")
tde4.setWidgetAttachModes(req,"posx","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"posx",8,23,140,0)
tde4.addTextFieldWidget(req,"posy","Y","0.0")
tde4.setWidgetAttachModes(req,"posy","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"posy",30,46,140,0)
tde4.addTextFieldWidget(req,"posz","Z","0.0")
tde4.setWidgetAttachModes(req,"posz","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"posz",53,68,140,0)	
tde4.addButtonWidget(req,"pos","Translate",70,10,)
tde4.setWidgetAttachModes(req,"pos","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pos",73,95,140,0)
#add rotation text boxes and button widgets...
tde4.addTextFieldWidget(req,"rotx","X","0.0")
tde4.setWidgetAttachModes(req,"rotx","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rotx",8,23,170,0)
tde4.addTextFieldWidget(req,"roty","Y","0.0")
tde4.setWidgetAttachModes(req,"roty","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"roty",30,46,170,0)
tde4.addTextFieldWidget(req,"rotz","Z","0.0")
tde4.setWidgetAttachModes(req,"rotz","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rotz",53,68,170,0)	
tde4.addButtonWidget(req,"rot","Rotate Around Camera",70,10)
tde4.setWidgetAttachModes(req,"rot","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"rot",73,95,170,0)
#scale widget...
tde4.addTextFieldWidget(req,"scale_factor","Uniform Scale","0.6")
tde4.setWidgetAttachModes(req,"scale_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"scale_factor",53,68,200,0)
tde4.addButtonWidget(req,"scale_button","Uniform Scale",70,10,)
tde4.setWidgetAttachModes(req,"scale_button","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"scale_button",73,95,200,0)
#sep2 widget...
tde4.addSeparatorWidget(req,"sep2")
tde4.setWidgetAttachModes(req,"sep2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"sep2",2,98,220,0)
#alpha slider...
tde4.addScaleWidget(req,"alpha_slider","Alpha","DOUBLE",0.0,1.0,0.32)
tde4.setWidgetAttachModes(req,"alpha_slider","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"alpha_slider",10,95,240,0)
#show polygons toggle widget...
tde4.addToggleWidget(req,"toggle","Show Polygons",1)
tde4.setWidgetAttachModes(req,"toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"toggle",28,32,200,0)
#Callbacks...
tde4.setWidgetCallbackFunction(req,"create","Create_3DModels")
tde4.setWidgetCallbackFunction(req,"select_all","Select_All")
tde4.setWidgetCallbackFunction(req,"deselect_all","Deselect_All")
tde4.setWidgetCallbackFunction(req,"delete_all","Delete_All")
tde4.setWidgetCallbackFunction(req,"pos","Translate")
tde4.setWidgetCallbackFunction(req,"rot","Rotate_Scale")
tde4.setWidgetCallbackFunction(req,"scale_button","Rotate_Scale")
tde4.setWidgetCallbackFunction(req,"color_menu","Color")
tde4.setWidgetCallbackFunction(req,"alpha_slider","Color")
tde4.setWidgetCallbackFunction(req,"toggle","Toggle_Polygons")
tde4.postCustomRequesterAndContinue(req,window_title,600,275)


