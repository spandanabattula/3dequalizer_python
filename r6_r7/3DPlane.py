
# 3DE4.script.name:	3D Plane
# 3DE4.script.version:	v1.0 		
# 3DE4.script.gui.button:	Lineup Controls::3D Plane, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::3D Plane, align-bottom-left, 70, 20
# 3DE4.script.comment:	
#23/01/2014
# Author : Patcha Saheb (patchasaheb@gmail.com)

from vl_sdv import *
import math

window_title = "3D Plane_v1.0"
def Create(req,widget,action):
	pg 	= tde4.getCurrentPGroup()
	c 	= tde4.getCurrentCamera()
	mlist 	= tde4.get3DModelList(pg,1)
	frame = tde4.getCurrentFrame(c)
	if  c!=None and pg != None:
		m	= tde4.create3DModel(pg,10)
		tde4.set3DModelName(pg,m,"3D plane")
		i0	= tde4.add3DModelVertex(pg,m,[100.0,0.0,100.0])
		i1	= tde4.add3DModelVertex(pg,m,[100.0,0.0,-100.0])
		i2	= tde4.add3DModelVertex(pg,m,[-100.0,0.0,-100.0])
		i3	= tde4.add3DModelVertex(pg,m,[-100.0,0.0,100.0])
		tde4.add3DModelLine(pg,m,[i0,i1,i2,i3,i0])
		tde4.add3DModelFace(pg,m,[i0,i1,i2,i3])
		tde4.set3DModelSelectionFlag(pg,m,1)
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")	

def Subdivision(req,widget,action):
	pg 	= tde4.getCurrentPGroup()
	c 	= tde4.getCurrentCamera()
	mlist 	= tde4.get3DModelList(pg,1)
	frame = tde4.getCurrentFrame(c)	
	if  c!=None and pg != None:
		if len(mlist) > 0:
			for m in mlist:
				name = tde4.get3DModelName(pg,m)
				mpos = tde4.get3DModelPosition3D(pg,m,c,frame)
				#extracting 3DModel position,scale,rotation...
				matrix = mat3d(tde4.get3DModelRotationScale3D(pg,m))
				s0 = vec3d(matrix[0][0],matrix[1][0],matrix[2][0]).norm2()
				s1 = vec3d(matrix[0][1],matrix[1][1],matrix[2][1]).norm2()
				s2 = vec3d(matrix[0][2],matrix[1][2],matrix[2][2]).norm2()
				scale_Matrix = mat3d(s0,0.0,0.0,0.0,s1,0.0,0.0,0.0,s2)
				rotation_Matrix = matrix * mat3d(1.0 / s0,0.0,0.0,0.0,1.0 / s1,0.0,0.0,0.0,1.0 / s2)
				final_Matrix = rotation_Matrix * scale_Matrix
				phi_x,phi_y,phi_z = rot3d(rotation_Matrix).angles(VL_APPLY_ZXY)
				phi_x = phi_x * 180.0 / math.pi
				phi_y = phi_y * 180.0 / math.pi
				phi_z = phi_z * 180.0 / math.pi
				tde4.delete3DModel(pg,m)
			m	= tde4.create3DModel(pg,10)
			tde4.set3DModelName(pg,m,name)
			i0	= tde4.add3DModelVertex(pg,m,[100.0,0.0,100.0])
			i1	= tde4.add3DModelVertex(pg,m,[100.0,0.0,-100.0])
			i2	= tde4.add3DModelVertex(pg,m,[-100.0,0.0,-100.0])
			i3	= tde4.add3DModelVertex(pg,m,[-100.0,0.0,100.0])
			tde4.add3DModelLine(pg,m,[i0,i1,i2,i3,i0])
			tde4.add3DModelFace(pg,m,[i0,i1,i2,i3])
			m1 = vec3d(tde4.get3DModelVertex(pg,m,i0))
			m2 = vec3d(tde4.get3DModelVertex(pg,m,i1))
			m3 = vec3d(tde4.get3DModelVertex(pg,m,i2))
			m4 = vec3d(tde4.get3DModelVertex(pg,m,i3))
			#d = (x2-x1)/n  dz = (z2-z1)/n
 			n = tde4.getWidgetValue(req,"subd_height") 
			n1 = tde4.getWidgetValue(req,"subd_width")
			dx = (m2[0] - m1[0]) / int(n)
			dz = (m2[2] - m1[2]) / int(n)
			d = vec3d(dx,0.0,dz)
			dx1 = (m1[0] - m4[0]) / int(n1)
			dz1 = (m1[2] - m1[2]) / int(n1)
			d1 = vec3d(dx1,0.0,dz1)
			i = vec3d(m1)
			j = vec3d(m4)
			k = vec3d(m3)
			l = vec3d(m4)
			for f0 in range(1,int(n)):
				i = i + d
				j = j + d
				v   = tde4.add3DModelVertex(pg,m,[i[0],i[1],i[2]])
				v1 = tde4.add3DModelVertex(pg,m,[j[0],j[1],j[2]])
				tde4.add3DModelLine(pg,m,[v,v1])
			for f1 in range(1,int(n1)):
				k = k + d1
				l = l + d1
				v2 = tde4.add3DModelVertex(pg,m,[k[0],k[1],k[2]])
				v3 = tde4.add3DModelVertex(pg,m,[l[0],l[1],l[2]])
				tde4.add3DModelLine(pg,m,[v2,v3])
			tde4.set3DModelPosition3D(pg,m,mpos)	
			tde4.set3DModelRotationScale3D(pg,m,final_Matrix.list())
			tde4.set3DModelSelectionFlag(pg,m,1)
		else:
			tde4.postQuestionRequester(window_title, "Error, atleast one 3DModel must be selected.", "OK")		
	else:
			tde4.postQuestionRequester(window_title, "Error, there is no point group or camera.", "OK")		
	
try:
	req	= _subd_requester
except (ValueError,NameError,TypeError):
	req	= tde4.createCustomRequester()
	_subd_requester	= req
	tde4.addTextFieldWidget(req, "subd_width", "Subdivision Width","1")	
	tde4.addTextFieldWidget(req, "subd_height", "Subdivision Height", "1")
	tde4.addButtonWidget(req,"create","Create",60,10)
	tde4.setWidgetCallbackFunction(req,"subd_width","Subdivision")
	tde4.setWidgetCallbackFunction(req,"subd_height","Subdivision")
	tde4.setWidgetCallbackFunction(req,"create","Create")
ret= tde4.postCustomRequesterAndContinue(req,window_title,500,120)