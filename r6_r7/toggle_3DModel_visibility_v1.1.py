#
#
# 3DE4.script.name:	Toggle Model Visibility
#
# 3DE4.script.version:	v1.1
#
# 3DE4.script.gui.button:	Lineup Controls::Model on/off, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::Model on/off, align-bottom-left, 70, 20
#
# 3DE4.script.comment:	Toggles selected 3D Model visibility.
#
#23/01/2014
#
# Author : Patcha Saheb (patchasaheb@gmail.com)

import tde4


pg_list = tde4.getPGroupList()
pg = tde4.getCurrentPGroup()

for p_group in pg_list:
	tde4.setCurrentPGroup(p_group)
	mlist = tde4.get3DModelList(p_group,1)
	for m in mlist :
		v = tde4.get3DModelVisibleFlag(p_group,m)
		tde4.set3DModelVisibleFlag(p_group,m,1-v)
tde4.setCurrentPGroup(pg)

	
