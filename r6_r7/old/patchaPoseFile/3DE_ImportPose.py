#
#
# 3DE4.script.name:	3DE Import Pose...
#
# 3DE4.script.version:	v1.0
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
#
# 3DE4.script.comment:	Imports Pose by reading .pose file...
#
# Written for 3DE4 by Patcha Saheb (patchasaheb@gmail.com)
#20-02-2014

from vl_sdv import *

pg	= tde4.getCurrentPGroup()
cam     = tde4.getCurrentCamera()
frame   = tde4.getCurrentFrame(cam)


if pg!=None and cam !=None and tde4.getPGroupType(pg)=="CAMERA" or tde4.getCameraType(cam) =="REF_FRAME" or tde4.getPGroupType(pg)=="OBJECT" or tde4.getPGroupType(pg) != "MOCAP":
	
	req	= tde4.createCustomRequester()
	tde4.addFileWidget(req,"file_browser","Filename...","*.pose")
	ret	= tde4.postCustomRequester(req,"3DE Import Pose...",500,120,"Ok","Cancel")
	if ret==1:
		path	= tde4.getWidgetValue(req,"file_browser")
		if path!=None:
			
			f	= open(path,"r")
			if not f.closed:
				string	= f.readline()
				a	= string.split()
				if len(a) == 6:
					
					# read values from .pose file..
					pos_x	= float(a[0])
					pos_y	= float(a[1])
					pos_z	= float(a[2])
					rot_x	= float(a[3])
					rot_y	= float(a[4])
					rot_z	= float(a[5])
					
					# matrix 3D...
					rot_x	= (rot_x*3.141592654)/180.0
					rot_y	= (rot_y*3.141592654)/180.0
					rot_z	= (rot_z*3.141592654)/180.0
					r3d	= mat3d(rot3d(rot_x,rot_y,rot_z,VL_APPLY_ZXY))
					r3d0	= [[r3d[0][0],r3d[0][1],r3d[0][2]],[r3d[1][0],r3d[1][1],r3d[1][2]],[r3d[2][0],r3d[2][1],r3d[2][2]]]
					
					# setting point group position and rotation...
					tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,pos_y,pos_z])
					tde4.setPGroupRotation3D(pg,cam,frame,r3d0)
					tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
					tde4.filterPGroup(pg,cam)
					tde4.setPGroupScale3D(pg,1.0)
				else: 
					tde4.postQuestionRequester("3DE Import Pose...","invalid .pose file","ok")
else:
	tde4.postQuestionRequester("3DE Import Pose...","Error...Camera or Object PGroup not found.", "ok")			

