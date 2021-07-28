
# 3DE4.script.name:	Set Next Proxy Footage...
#
# 3DE4.script.version:	v1.0
# 3DE4.script.gui.config_menus: true
# Patcha Saheb(patchasaheb@gmail.com)



cam = tde4.getCurrentCamera()


current_count = tde4.getCameraProxyFootage(cam)

#check which proxy footage has the plate
null = -1
for i in range(0,4):
	tde4.setCameraProxyFootage(cam,i)
	path = tde4.getCameraPath(cam)
	if path != "":
		null = null + 1
tde4.setCameraProxyFootage(cam,current_count)


for i in range(0,null):
	if current_count == null:
		tde4.setCameraProxyFootage(cam,0)
	else:		
		tde4.setCameraProxyFootage(cam,current_count+1)	
	break
