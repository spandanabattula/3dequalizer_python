#
#
# 3DE4.script.name:	Snap Model 2 Point
#
# 3DE4.script.version:	v1.0.
#
# 3DE4.script.gui:	Orientation Controls::3D Models
#
# 3DE4.script.comment:	Snap 3D Model to selected Point. The operation requieres one selected point and 3DModel.
#
#
# 21/01/2014 

# Author : Patcha Saheb (patchasaheb@gmail.com)

cam = tde4.getCurrentCamera()
pg  = tde4.getCurrentPGroup()
pl  = tde4.getPointList(pg,1)

if pg!=None and cam !=None and len(pl)>0:
	for p in pl:
		ps = tde4.isPointCalculated3D(pg,p) 
		p3d = tde4.getPointCalcPosition3D(pg,p)	
	if ps > 0:
		mlist = tde4.get3DModelList(pg,1)
		if len(mlist)<2 and len(mlist)>0 and len(pl)<2:
			m = mlist[0]				
			tde4.set3DModelPosition3D(pg,m,p3d)
		else :
			tde4.postQuestionRequester("Error", "there must be exactly one selected 3D point and one selected 3D model..!", "OK")
	else:
		tde4.postQuestionRequester("Error", "there must be exactly one selected 3D point and one selected 3D model..!", "OK")
else :
	tde4.postQuestionRequester("Error", "there must be exactly one selected 3D point and one selected 3D model..!", "OK")
		


