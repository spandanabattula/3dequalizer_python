#Author : Patcha Saheb(patchasaheb@gmail.com)
# 3DE4.script.comment:	Creates test 2d points at the four corners of the frame, plus the center. For testing,

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)

point_1 = tde4.createPoint(pg)
tde4.setPointPosition2D(pg,point_1,cam,frame,[0.0,0.0])

point_2 = tde4.createPoint(pg)
tde4.setPointPosition2D(pg,point_2,cam,frame,[1.0,0.0])

point_3 = tde4.createPoint(pg)
tde4.setPointPosition2D(pg,point_3,cam,frame,[0.0,1.0])

point_4 = tde4.createPoint(pg)
tde4.setPointPosition2D(pg,point_4,cam,frame,[1.0,1.0])

point_1 = tde4.createPoint(pg)
tde4.setPointPosition2D(pg,point_1,cam,frame,[0.5,0.5])
