# 3DE4.script.name:	Lamb on/off
# 3DE4.script.version:	v1.0
# 3DE4.script.gui.button:	Lineup Controls::Lamb on/off, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::Lamb on/off, align-bottom-left, 70, 20
# 3DE4.script.comment:toggles lambertizer on/off.
# Patcha Saheb(patchasaheb@gmail.com)


from vl_sdv import *

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
mlist = tde4.get3DModelList(pg,1)
if len(mlist) > 0:
	for model in mlist:	
		per_vertex = tde4.get3DModelPerVertexColorsFlag(pg,model)
		if per_vertex == 1:
			tde4.set3DModelPerVertexColorsFlag(pg,model,0)
			tde4.set3DModelRenderingFlags(pg,model,0,1,0)
		else:
			tde4.set3DModelPerVertexColorsFlag(pg,model,1)
			tde4.set3DModelRenderingFlags(pg,model,0,0,1)
       
else:
	tde4.postQuestionRequester("Patcha Lamb on/off","Error, atleast one 3DModel must be selected.","Ok")









