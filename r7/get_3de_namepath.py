# 3DE4.script.name: 3de filepath
# 3DE4.script.version: v1.1
# 3DE4.script.gui: Main Window::3DE4
# 3DE4.script.comment: Shows/Opens current 3de project file path.

# July 20 2021, Montreal
# Patcha Saheb(patchasaheb@gmail.com)

WINDOW_TITLE = "3de filepath"

pg = tde4.getCurrentPGroup()
cam = tde4.getCurrentCamera()
frame = tde4.getCurrentFrame(cam)
model_list = tde4.get3DModelList(pg,1)
project_path = tde4.getProjectPath()

req	= tde4.createCustomRequester()
if not project_path: project_path = ""
tde4.addTextFieldWidget(req, "file_path", "3de filepath", project_path)
tde4.setWidgetAttachModes(req,"file_path","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"file_path",16,98,15,0)

tde4.postCustomRequesterAndContinue(req,WINDOW_TITLE,600,60)




