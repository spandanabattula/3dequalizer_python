# 3DE4.script.name:	Translate 3DModel Pivot...
#
# 3DE4.script.version:	v1.0
#
# 3DE4.script.gui:	Orientation Controls::3D Models
# 3DE4.script.gui.button:	Orientation Controls::Model Pivot, align-bottom-left, 70, 20
# 3DE4.script.gui.button:	Lineup Controls::Model Pivot, align-bottom-left, 80, 20
#15-May-2015
#Patcha Saheb(patchasaheb@gmail.com)

from vl_sdv import*

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
mlist = tde4.get3DModelList(pg,1)
window_title = "Patcha Translate 3DModel Pivot v1.0"

def update(req):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,1)
	if len(mlist) == 1:
		model = mlist[0]
		name = tde4.get3DModelName(pg,model)
		tde4.setWidgetValue(req,"name",str(name))
		
#update names...
def Names(req,widget,action):
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		mlist = tde4.get3DModelList(pg,1)
		if len(mlist) == 1:
			model = mlist[0]
			name = tde4.get3DModelName(pg,model)
			if widget == "parent_get":
				tde4.setWidgetValue(req,"parent",str(name))
				p_v = tde4.getWidgetValue(req,"parent")
				c_v = tde4.getWidgetValue(req,"child")
				if p_v == c_v:
					tde4.setWidgetValue(req,"parent"," ")
					tde4.postQuestionRequester(window_title,"Error, parent and child models are should not be same.","Ok")
			if widget == "child_get":
				tde4.setWidgetValue(req,"child",str(name))
				p_v = tde4.getWidgetValue(req,"parent")
				c_v = tde4.getWidgetValue(req,"child")				
				if p_v == c_v:
					tde4.setWidgetValue(req,"child"," ")
					tde4.postQuestionRequester(window_title,"Error, parent and child models are should not be same.","Ok")
		else:
			tde4.postQuestionRequester(window_title,"Error, Exactly one 3DModel must be selected or 3DModels should be under current PGroup","Ok")	

#match pivots function...
def Match_Pivot(req,widget,action):
	cam	= tde4.getCurrentCamera()
	pg	= tde4.getCurrentPGroup()
	frame = tde4.getCurrentFrame(cam)
	mlist = tde4.get3DModelList(pg,0)
	p_v = tde4.getWidgetValue(req,"parent")
	c_v = tde4.getWidgetValue(req,"child")	
	if c_v and p_v != " ":
		for model in mlist:
			name = tde4.get3DModelName(pg,model)
			if name == p_v:
				parent = model
		for model in mlist:
			name = tde4.get3DModelName(pg,model)
			if name == c_v:
				child = model	
		tde4.set3DModelSurveyFlag(pg,parent,0)
		tde4.set3DModelSurveyFlag(pg,child,0)
		parent_pos = tde4.get3DModelPosition3D(pg,parent,cam,frame)
		parent_rot = tde4.get3DModelRotationScale3D(pg,parent)
		tde4.set3DModelPosition3D(pg,child,parent_pos)
		tde4.set3DModelRotationScale3D(pg,child,parent_rot)		
		parent_list = []
		child_list = []
		n = tde4.get3DModelNoVertices(pg,parent)
		mrot = tde4.get3DModelRotationScale3D(pg,parent)
		mpos= tde4.get3DModelPosition3D(pg,parent,cam,frame)
		for i in range(0,n):
			v = tde4.get3DModelVertex(pg,parent,i,cam,frame)
			vector = mat3d(mrot).invert()*(vec3d(0,0,0)-vec3d(mpos))
			v[0] = v[0]-vector[0]
			v[1] = v[1]-vector[1]
			v[2] = v[2]-vector[2]
			v = mat3d(mrot)*vec3d(v)
			parent_list.append(v)
			break
		n = tde4.get3DModelNoVertices(pg,child)
		mrot = tde4.get3DModelRotationScale3D(pg,child)
		mpos= tde4.get3DModelPosition3D(pg,child,cam,frame)
		for i in range(0,n):
			v = tde4.get3DModelVertex(pg,child,i,cam,frame)
			vector = mat3d(mrot).invert()*(vec3d(0,0,0)-vec3d(mpos))
			v[0] = v[0]-vector[0]
			v[1] = v[1]-vector[1]
			v[2] = v[2]-vector[2]
			v = mat3d(mrot)*vec3d(v)
			child_list.append(v)
			break
		newpos = vec3d(child_list[0]) - vec3d(parent_list[0])
		newpos = vec3d(mpos) - vec3d(newpos)
		tde4.set3DModelPosition3D(pg,child,newpos.list())

#funcion for getting vector...		
def Vector(pg,model,cam,frame,p3d,vlist):
	mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
	mrot = tde4.get3DModelRotationScale3D(pg,model)
	vector = mat3d(mrot).invert() * (vec3d(p3d) - vec3d(mpos))
	l = []
	for i in range(0,vlist):
		v = tde4.get3DModelVertex(pg,model,i,cam,frame)
		v[0] = v[0] - vector[0]
		v[1] = v[1] - vector[1]
		v[2] = v[2] - vector[2]
		l.append(v)
	return l	
	
#function for getting center pivot position...
def Center_Pivot(pg,model,cam,frame,vlist):
	mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
	mrot = tde4.get3DModelRotationScale3D(pg,model)
	n = tde4.get3DModelNoVertices(pg,model)
	x_list = []
	y_list = []
	z_list = []
	for i in range(0,n):
		vpos = tde4.get3DModelVertex(pg,model,i,cam,frame)
		x_list.append(vpos[0])
		y_list.append(vpos[1])
		z_list.append(vpos[2])
	x = sum(x_list) / len(x_list)
	y = sum(y_list) / len(y_list)
	z = sum(z_list) / len(z_list)
	com_global = (mat3d(mrot)*vec3d(x,y,z)) + vec3d(mpos)
	return com_global
	
#delete pivot locator funciton...
def Delete(requester,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	if widget == "delete":
		model_list = tde4.get3DModelList(pg,0)
		for item in model_list:
			name = tde4.get3DModelName(pg,item)
			if name.startswith("Pivot_Locator") == True:
				tde4.delete3DModel(pg,item)
				
#clearr funciton...
def Clear(requester,widget,action):	
	if widget == "parent_clear":
		tde4.setWidgetValue(req,"parent"," ")
	if widget == "child_clear":
		tde4.setWidgetValue(req,"child"," ")	
					
	
#main...		
def Move_Pivot(requester,widget,action):
	pg = tde4.getCurrentPGroup()
	cam = tde4.getCurrentCamera()
	frame = tde4.getCurrentFrame(cam)
	pl = tde4.getPointList(pg,1)
	mlist = tde4.get3DModelList(pg,1)
	if len(mlist) == 1:
		model = mlist[0]
		tde4.set3DModelSurveyFlag(pg,model,0)
#origin...
		if widget == "origin":
			p3d = vec3d(0,0,0)
			vlist = tde4.get3DModelNoVertices(pg,model)
			v = Vector(pg,model,cam,frame,p3d,vlist)
			for i in range(0,vlist):
				tde4.set3DModelVertex(pg,model,i,v[i])
			tde4.set3DModelPosition3D(pg,model,p3d.list())
#point...
		if widget == "point":
			if len(pl) == 1 and len(mlist) == 1:
				p3d = tde4.getPointCalcPosition3D(pg,pl[0])	
				vlist = tde4.get3DModelNoVertices(pg,model)
				v = Vector(pg,model,cam,frame,p3d,vlist)
				for i in range(0,vlist):
					tde4.set3DModelVertex(pg,model,i,v[i])
				tde4.set3DModelPosition3D(pg,model,p3d)				
			else:
				tde4.postQuestionRequester(window_title,"Error, exactly one 3DModel and one Point must be selected","Ok")		
#locator...
		if widget == "locator":
			vlist = tde4.get3DModelNoVertices(pg,model)
			cp = Center_Pivot(pg,model,cam,frame,vlist)
			model_list = tde4.get3DModelList(pg,0)
			l = []
			for item in model_list:
				name = tde4.get3DModelName(pg,item)
				if name.startswith("Pivot_Locator") == True:
					l.append(item)
					break
			if len(l) > 0:
				p3d = vec3d(tde4.get3DModelPosition3D(pg,l[0],cam,frame))
				vlist = tde4.get3DModelNoVertices(pg,model)
				v = Vector(pg,model,cam,frame,p3d,vlist)
				for i in range(0,vlist):
					tde4.set3DModelVertex(pg,model,i,v[i])
				tde4.set3DModelPosition3D(pg,model,p3d.list())
			else:
				tde4.postQuestionRequester(window_title,"Error, first please create 'Pivot Locator'.","Ok")					
#center...
		if widget == "center":
			vlist = tde4.get3DModelNoVertices(pg,model)
			p3d = Center_Pivot(pg,model,cam,frame,vlist)	
			v = Vector(pg,model,cam,frame,p3d,vlist)			
			for i in range(0,vlist):
				tde4.set3DModelVertex(pg,model,i,v[i])
			tde4.set3DModelPosition3D(pg,model,p3d.list())					
#camera...
		if widget == "camera":
			if tde4.getPGroupType(pg) == "CAMERA":
				p3d = tde4.getPGroupPosition3D(pg,cam,frame)
				vlist = tde4.get3DModelNoVertices(pg,model)
				v = Vector(pg,model,cam,frame,p3d,vlist)
				for i in range(0,vlist):
					tde4.set3DModelVertex(pg,model,i,v[i])
				tde4.set3DModelPosition3D(pg,model,p3d)				
			else:
				tde4.postQuestionRequester(window_title,"Error, 3DModel should be under camera PGroup.","Ok")	
#pivot locator...
		if widget == "pivot_loc":
			model_list = tde4.get3DModelList(pg,0)
			for item in model_list:
				name = tde4.get3DModelName(pg,item)
				if name.startswith("Pivot_Locator") == True:
					tde4.delete3DModel(pg,item)	
			m = tde4.create3DModel(pg, 7)
			tde4.set3DModelName(pg, m, "Pivot_Locator")
			tde4.add3DModelVertex(pg, m, [0.0, 0.0, 0.0])
			tde4.add3DModelVertex(pg, m, [10.0, 0.0, 0.0])
			tde4.add3DModelVertex(pg, m, [-10.0, 0.0, 0.0])
			tde4.add3DModelVertex(pg, m, [0.0, 10.0, 0.0])
			tde4.add3DModelVertex(pg, m, [0.0, -10.0, 0.0])
			tde4.add3DModelVertex(pg, m, [0.0, 0.0, 10.0])
			tde4.add3DModelVertex(pg, m, [0.0, 0.0, -10.0])
			for i in range(7):
				tde4.add3DModelLine(pg, m, [0, i])
			tde4.set3DModelColor(pg,m,1.0,0.0,0.0,1.0)
			tde4.set3DModelSurveyFlag(pg, m, 0)
			vlist = tde4.get3DModelNoVertices(pg,model)
			cp = Center_Pivot(pg,model,cam,frame,vlist)			
			tde4.set3DModelPosition3D(pg, m, [cp[0],cp[1],cp[2]])
#freeze transformations...
		if widget == "freeze":
			mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
			mrot = tde4.get3DModelRotationScale3D(pg,model)		
			m = 	mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()	
			s  =  vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
			r  = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
			p3d = vec3d(0,0,0)
			vlist = tde4.get3DModelNoVertices(pg,model)
			vector = mat3d(mrot).invert() * (vec3d(p3d) - vec3d(mpos))
			for i in range(0,vlist):
				v = tde4.get3DModelVertex(pg,model,i,cam,frame)
				v[0] = v[0] - vector[0]
				v[1] = v[1] - vector[1]
				v[2] = v[2] - vector[2]	
				v = mat3d(mrot) * vec3d(v)
				tde4.set3DModelVertex(pg,model,i,v.list())
			tde4.set3DModelPosition3D(pg,model,[0,0,0])	
			scale_matrix = mat3d(1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0)
			rot_matrix = mat3d(1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0)
			f = rot_matrix * scale_matrix
			tde4.set3DModelRotationScale3D(pg,model,f.list())
#reload 3DModels...
		if widget == "reload":
			path	= tde4.get3DModelFilepath(pg,model)
			if path!="":
				tde4.importOBJ3DModel(pg,model,path)	
	else:
		tde4.postQuestionRequester(window_title,"Error, Exactly one 3DModel must be selected or 3DModels should be under current PGroup","Ok")	
				
#GUI...
try:
	req	= _pivot_requester
except (ValueError,NameError,TypeError):
	req	= tde4.createCustomRequester()
	_pivot_requester	= req
#add model name text field widget...
	tde4.addTextFieldWidget(req,"name","Selected 3D Model"," ")
	tde4.setWidgetAttachModes(req,"name","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"name",27,98,10,0)	
#set widget sensitive flag...
	tde4.setWidgetSensitiveFlag(req,"name",0)
#move pivot to origin...
	tde4.addButtonWidget(req,"origin","Move pivot to Origin",70,10)
	tde4.setWidgetAttachModes(req,"origin","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"origin",4,32,40,0)		
#move pivot to point...
	tde4.addButtonWidget(req,"point","Move pivot to Point",70,10)
	tde4.setWidgetAttachModes(req,"point","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"point",35,65,40,0)		
#move pivot to locator...
	tde4.addButtonWidget(req,"locator","Move pivot to Locator",70,10)
	tde4.setWidgetAttachModes(req,"locator","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"locator",68,96,40,0)	
#move pivot to center...
	tde4.addButtonWidget(req,"center","Move pivot to Center",70,10)
	tde4.setWidgetAttachModes(req,"center","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"center",4,32,70,0)	
#move pivot to camera...
	tde4.addButtonWidget(req,"camera","Move pivot to Camera",70,10)
	tde4.setWidgetAttachModes(req,"camera","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"camera",35,65,70,0)	
#freeze transformations...
	tde4.addButtonWidget(req,"freeze","Freeze Transformations",70,10)
	tde4.setWidgetAttachModes(req,"freeze","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"freeze",68,96,70,0)
#pivot locator widget...
	tde4.addButtonWidget(req,"pivot_loc","Create Pivot Locator",70,10)
	tde4.setWidgetAttachModes(req,"pivot_loc","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"pivot_loc",4,32,100,0)
#reload widget...
	tde4.addButtonWidget(req,"reload","Reload Model",70,10)
	tde4.setWidgetAttachModes(req,"reload","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"reload",35,65,100,0)
#delete pivot locator button widget...
	tde4.addButtonWidget(req,"delete","Delete Pivot Locator",70,10)
	tde4.setWidgetAttachModes(req,"delete","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"delete",68,96,100,0)	
#sep2 widget...
	tde4.addSeparatorWidget(req,"sep1")
	tde4.setWidgetAttachModes(req,"sep1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"sep1",2,98,120,0)
#parent model name widget...
	tde4.addTextFieldWidget(req,"parent","Parent Model"," ")
	tde4.setWidgetAttachModes(req,"parent","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"parent",20,75,140,0)
	tde4.setWidgetSensitiveFlag(req,"parent",0)
#parent model get widget...
	tde4.addButtonWidget(req,"parent_get","Get",70,10)
	tde4.setWidgetAttachModes(req,"parent_get","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"parent_get",77,87,140,0)
#parent model clear widget...
	tde4.addButtonWidget(req,"parent_clear","Clear",70,10)
	tde4.setWidgetAttachModes(req,"parent_clear","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"parent_clear",89,98,140,0)
#child model name widget...
	tde4.addTextFieldWidget(req,"child","Child Model"," ")
	tde4.setWidgetAttachModes(req,"child","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"child",20,75,170,0)
	tde4.setWidgetSensitiveFlag(req,"child",0)
#child model get widget...
	tde4.addButtonWidget(req,"child_get","Get",70,10)
	tde4.setWidgetAttachModes(req,"child_get","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"child_get",77,87,170,0)
#child model clear widget...
	tde4.addButtonWidget(req,"child_clear","Clear",70,10)
	tde4.setWidgetAttachModes(req,"child_clear","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"child_clear",89,98,170,0)
#match pivots button widget...
	tde4.addButtonWidget(req,"match_pivots","Match 3DModels transform, maintain pivots",70,10)
	tde4.setWidgetAttachModes(req,"match_pivots","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
	tde4.setWidgetOffsets(req,"match_pivots",20,80,200,0)
#widget callbacks...
	tde4.setWidgetCallbackFunction(req,"origin","Move_Pivot")	
	tde4.setWidgetCallbackFunction(req,"point","Move_Pivot")	
	tde4.setWidgetCallbackFunction(req,"locator","Move_Pivot")
	tde4.setWidgetCallbackFunction(req,"center","Move_Pivot")	
	tde4.setWidgetCallbackFunction(req,"camera","Move_Pivot")	
	tde4.setWidgetCallbackFunction(req,"freeze","Move_Pivot")	
	tde4.setWidgetCallbackFunction(req,"pivot_loc","Move_Pivot")
	tde4.setWidgetCallbackFunction(req,"reload","Move_Pivot")
	tde4.setWidgetCallbackFunction(req,"delete","Delete")
	tde4.setWidgetCallbackFunction(req,"parent_get","Names")
	tde4.setWidgetCallbackFunction(req,"child_get","Names")	
	tde4.setWidgetCallbackFunction(req,"parent_clear","Clear")
	tde4.setWidgetCallbackFunction(req,"child_clear","Clear")	
	tde4.setWidgetCallbackFunction(req,"match_pivots","Match_Pivot")		
tde4.postCustomRequesterAndContinue(req,window_title,530,230,"update")

