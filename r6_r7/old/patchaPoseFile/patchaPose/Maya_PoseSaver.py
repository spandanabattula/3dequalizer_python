#It exports and imports ".pose" files for selected object..
#it works only for rigid bodys not for rig...
#file extention should be ".pose" otherwise it won't work...
#it exports only translate & rotate values for selected objet...
#created by Patcha Saheb(patchasaheb@gmail.com)
#Date : 13-03-2014.
############################################################

import maya.cmds as cmds

# importPose Function...

def importPose():

# getting selection list...
	sel = cmds.ls(sl=True)
	if len(sel)!=0 and len(sel)<2:

#opening .pose file and reading values...
		path = cmds.fileDialog(dm="*.pose",m=0)
		f = open(path,"r")
		string = f.readline()
		values = string.split()

#reading & storing values...
		if len(values) == 6:
			posx	=	values[0]
			posy	=	values[1]
			posz	=	values[2]
			rotx	=	values[3]
			roty	=	values[4]
			rotz	=	values[5]
			cmds.setAttr("{0}.tx".format(sel[0]),lock=False)
			cmds.setAttr("{0}.ty".format(sel[0]),lock=False)
			cmds.setAttr("{0}.tz".format(sel[0]),lock=False)
			cmds.setAttr("{0}.rx".format(sel[0]),lock=False)
			cmds.setAttr("{0}.ry".format(sel[0]),lock=False)
			cmds.setAttr("{0}.rz".format(sel[0]),lock=False)			

#setting tx,ty,tx,rx,ry,rz attributes...
			cmds.setAttr("{0}.rotateOrder".format(sel[0]),2)
			cmds.setAttr("{0}.translateX".format(sel[0]),float(posx),lock=True)
			cmds.setAttr("{0}.translateY".format(sel[0]),float(posy),lock=True)
			cmds.setAttr("{0}.translateZ".format(sel[0]),float(posz),lock=True)
			cmds.setAttr("{0}.rotateX".format(sel[0]),float(rotx),lock=True)
			cmds.setAttr("{0}.rotateY".format(sel[0]),float(roty),lock=True)
			cmds.setAttr("{0}.rotateZ".format(sel[0]),float(rotz),lock=True)
		else:
			cmds.warning("selected file is not a valid file...")	
	else:
		cmds.warning("nothing is selected or selection was more than one object...")

#exportPose Function...
	 
def exportPose():
# getting selection list...
	sel = cmds.ls(sl=True)
	if len(sel)!=0 and len(sel)<2:
	
# creating locator and parenting...
		loc = cmds.spaceLocator(name="pose_loc")
		cmds.parentConstraint(sel[0],loc,mo=0)
		cmds.setAttr("pose_loc.rotateOrder",2)
	
# getting pos & rot values...
		p = cmds.xform("pose_loc",q=True,t=True)
		r = cmds.xform("pose_loc",q=True,rotation=True)
		posvalues = str(p[0])+" "+str(p[1])+" "+str(p[2])
		rotvalues = str(r[0])+" "+str(r[1])+" "+str(r[2])
		expvalues = str(posvalues)+" "+str(rotvalues)

#unlocking attributes...
		cmds.setAttr("{0}.tx".format(sel[0]),lock=False)
		cmds.setAttr("{0}.ty".format(sel[0]),lock=False)
		cmds.setAttr("{0}.tz".format(sel[0]),lock=False)
		cmds.setAttr("{0}.rx".format(sel[0]),lock=False)
		cmds.setAttr("{0}.ry".format(sel[0]),lock=False)
		cmds.setAttr("{0}.rz".format(sel[0]),lock=False)

# writing a file...
		path = cmds.fileDialog(dm="*.pose",m=1)
		if path!=None:
			cmds.delete(loc)
#locking attributes...
			cmds.setAttr("{0}.tx".format(sel[0]),lock=True)
			cmds.setAttr("{0}.ty".format(sel[0]),lock=True)
			cmds.setAttr("{0}.tz".format(sel[0]),lock=True)
			cmds.setAttr("{0}.rx".format(sel[0]),lock=True)
			cmds.setAttr("{0}.ry".format(sel[0]),lock=True)
			cmds.setAttr("{0}.rz".format(sel[0]),lock=True)
			f = open(path,"w")
			f.write(expvalues)
			f.close()
	else:
		cmds.warning("nothing is selected")
#building UI...

if cmds.window("win",ex=True):
	cmds.deleteUI("win")
win = cmds.window("win",t="Pose Saver/Loader v1.0",widthHeight=(200, 40))
cmds.columnLayout(adj=True)
cmds.frameLayout( label='Help', borderStyle='out',collapsable = True)
helpStr = """Directions:
1. select a object to import/export.
2. it works only for rigid bodies not for rig.
3. file extension should be ".pose"(eg:CameraAngle.pose). 
4.this script imports/exports only translate & rotate values of selected object from/to ".pose" file."""
cmds.scrollField( editable=False, wordWrap=True, text=helpStr )
loadbutton = cmds.button(l="Load Pose",c ="importPose()" )
cmds.columnLayout(adj=True)
savebutton = cmds.button(l="Save Pose",c="exportPose()")
cmds.showWindow("win")

######################################################################
