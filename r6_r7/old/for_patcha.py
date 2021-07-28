
from vl_sdv import*
import math

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
pl = tde4.getPointList(pg,0)

pivot = vec3d(tde4.getPointCalcPosition3D(pg,pl[0]))

# Specify the frame to be used in order to express rotation. For example,
# my test sequencehas 126 frames, I pick a frame in the middle...
my_frame = tde4.getCurrentFrame(cam)

# You said you'd like to rotate around the camera's local x-axis.
# So let us create a rotation matrix for 5 degree around the x-axis
rx = 10.0 * math.pi / 180.0
ry = 0
rz = 0

# We interpret this as a rotation in local coordinates.
delta_rot_local = mat3d(rot3d(rx,ry,rz,VL_APPLY_ZXY))

# Now the task is to express this matrix in *global* coordinates.
# In order to transform a rotation matrix like this one
# to another coordinate system, we have do apply the transformation
# from the left and the inverse one from the right, like a "sandwich".
# So let's do the sandwich technique; apply transform from left and
# inverse transform from the right.
# I think you want to use this transformation for *all* frames.
cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,my_frame))
delta_rot_global = cam_rot * delta_rot_local * (cam_rot).trans()

# Now, if your previous script worked for one particular frame,
# it should work for all frames now, since we apply the same
# transformation (generated from my_frame) to all cameras and points.

num_frames = tde4.getCameraNoFrames(cam)
for frame in range(1,num_frames + 1):
	cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
	cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))

# No, not here! We have already calculated the transformation matrix
# in globale space above, outside of this loop.
#	delta_rot_global = cam_rot * delta_rot_local * (cam_rot).trans()

	# Now apply this to the camera. Position:
	p3d = delta_rot_global * (cam_pos - pivot) + pivot
	tde4.setPGroupPosition3D(pg,cam,frame,p3d.list())

	# Rotation. Use the old rotation and apply our new global delta rotation.
	cam_rot_new = delta_rot_global * cam_rot
	tde4.setPGroupRotation3D(pg,cam,frame,cam_rot_new.list())


for point in pl:
	if tde4.isPointCalculated3D(pg,point):	
		survey_pos = tde4.getPointCalcPosition3D(pg,point)
		tde4.setPointSurveyPosition3D(pg,point,survey_pos)
		tde4.setPointSurveyMode(pg,point,"SURVEY_EXACT")
		p3d = vec3d(tde4.getPointSurveyPosition3D(pg,point))

# No, don't do this here! We have calculated the transformation matrix
# in globale space above, outside of the frame loop.
#		rx = 10.0 * math.pi / 180.0
#		ry = 0
#		rz = 0
#		delta_rot_local = mat3d(rot3d(rx,ry,rz,VL_APPLY_ZXY))
#		delta_rot_global = cam_rot * delta_rot_local * (cam_rot).trans()										

	p3d = delta_rot_global * (p3d - pivot) + pivot
	tde4.setPointSurveyPosition3D(pg,point,p3d.list())


# Finally! Do this after modifying *all* frames...
# Don't do this within the frame loop!
tde4.filterPGroup(pg,cam)

