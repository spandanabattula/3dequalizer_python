# 3DE4.script.name:	Aim 3DModel to Camera
# 3DE4.script.version:	v1.0
# 3DE4.script.gui:	Orientation Controls::3D Models
# 3DE4.script.comment:Aims selected 3DModel to Camera
# Patcha Saheb(patchasaheb@gmail.com)


from vl_sdv import *
import math

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
pl = tde4.getPointList(pg,1)
mlist = tde4.get3DModelList(pg,1)
if len(mlist) == 1:
	model = mlist[0]
	p3d = tde4.getPGroupPosition3D(pg,cam,frame)
	mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
	mrot = tde4.get3DModelRotationScale3D(pg,model)

	#Extract scale & rotation matrices...
	m = mat3d(tde4.get3DModelRotationScale3D(pg,model))
	s0 = vec3d(m[0][0],m[1][0],m[2][0]).norm2()
	s1 = vec3d(m[0][1],m[1][1],m[2][1]).norm2()
	s2 = vec3d(m[0][2],m[1][2],m[2][2]).norm2()
	scale_Matrix = mat3d(s0,0.0,0.0,0.0,s1,0.0,0.0,0.0,s2)
	m_rot = m * mat3d(1.0/s0,0.0,0.0,0.0,1.0/s1,0.0,0.0,0.0,1.0/s2)
	rot_Matrix = mat3d(rot3d(m_rot),VL_APPLY_ZXY)

	z_dir = ((vec3d(p3d) - vec3d(mpos)).unit())
	x_dir = z_dir ^ vec3d(0,1,0)
	y_dir = -(z_dir ^ x_dir)
	rot = mat3d(x_dir,y_dir,-z_dir)
	rot = mat3d(rot).trans()
	#rot = rot_Matrix * rot
	#rot = rot = scale_Matrix
	tde4.set3DModelRotationScale3D(pg,model,rot.list())

	m = mat3d(tde4.get3DModelRotationScale3D(pg,model))
	m_rot = m * mat3d(1.0/s0,0.0,0.0,0.0,1.0/s1,0.0,0.0,0.0,1.0/s2)
	rot_Matrix = mat3d(rot3d(m_rot),VL_APPLY_ZXY)
	f = rot_Matrix * scale_Matrix
	tde4.set3DModelRotationScale3D(pg,model,f.list())
else:
	tde4.postQuestionRequester("Aim 3DModel to Camera","Error, please select exactly one 3DModel.","Ok")




