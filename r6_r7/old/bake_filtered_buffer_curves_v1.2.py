#
# 3DE4.script.name:		Bake post filtered buffer curves
#
# 3DE4.script.version:		v1.2
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: Bakes translation and rotation keyframes, so that any Post Filter smoothing, etc. is baked from the Filtered Curves, to the Raw curves. After bake, automatically sets Post Filter to Off. May then need Euler Flipping Filter applied.
#
#
# Patcha Saheb(patchasaheb@gmail.com)
#


from vl_sdv import*

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
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
if pg_type == "OBJECT":
	for i in range(1,frames+1):
		tde4.setCurrentFrame(cam,i)
		frame = tde4.getCurrentFrame(cam)
		obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
		obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
		scale = tde4.getPGroupScale3D(pg)
		focal = tde4.getCameraFocalLength(cam,frame)
		new_values = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), obj_pos.list(), 1.0, 0)
		tde4.setPGroupPosition3D(pg,cam,frame,new_values[1])
		tde4.setPGroupRotation3D(pg,cam,frame,new_values[0])
		tde4.setPGroupScale3D(pg,scale)
		tde4.setCameraFocalLength(cam,frame,focal)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
#only change from public, returns to parked frame
tde4.setCurrentFrame(cam,currentFrame)


"""req = tde4.createCustomRequester()
window_title = "Patcha Bake post filtered buffer curves"
tde4.addButtonWidget(req,"bake_all","Bake post filtered buffer curves all keyframes",70,10)
tde4.setWidgetAttachModes(req,"bake_all","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"bake_all",2,98,15,0)
tde4.addButtonWidget(req,"bake_ext","Bake post filtered buffer curves existing keyframes",70,10)
tde4.setWidgetAttachModes(req,"bake_ext","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"bake_ext",2,98,55,0)


tde4.postCustomRequesterAndContinue(req,window_title,420,65)"""















