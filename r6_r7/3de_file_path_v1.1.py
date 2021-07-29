# 3DE4.script.name:	3de filepath
# 3DE4.script.version:	v1.1
# 3DE4.script.gui: Main Window::3DE4
# 3DE4.script.comment: This script shows the 3de project path

# Patcha Saheb(patchasaheb@gmail.com)
# July 28 2021, Montreal

import os, sys

WINDOW_TITLE = "Patcha 3de file path v1.1"

def close_btn_clicked(req, widget, action):
	if not tde4.isCustomRequesterPosted(req) == "REQUESTER_UNPOSTED":
		tde4.unpostCustomRequester(req)

def copy_dir_path_clicked(req, widget, action):
	dir_path = tde4.getWidgetValue(req, "directory_path_txt")
	if dir_path:
		tde4.setClipboardString(str(dir_path))

def copy_full_path_clicked(req, widget, action):
	full_path = tde4.getWidgetValue(req, "full_path_txt")
	if full_path:
		tde4.setClipboardString(str(full_path))

project_path = tde4.getProjectPath()

req = tde4.createCustomRequester()
tde4.addTextFieldWidget(req,"directory_path_txt","Directory","")
tde4.setWidgetOffsets(req,"directory_path_txt",10,99,15,0)
tde4.setWidgetAttachModes(req,"directory_path_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(req,"directory_path_txt",200,20)
tde4.addTextFieldWidget(req,"file_name_txt","File name","")
tde4.setWidgetOffsets(req,"file_name_txt",10,99,15,0)
tde4.setWidgetAttachModes(req,"file_name_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"file_name_txt",200,20)
tde4.addTextFieldWidget(req,"full_path_txt","Full path","")
tde4.setWidgetOffsets(req,"full_path_txt",10,99,15,0)
tde4.setWidgetAttachModes(req,"full_path_txt","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"full_path_txt",200,20)
tde4.addButtonWidget(req,"copy_dir_path_btn","Copy directory path to clipboard")
tde4.setWidgetOffsets(req,"copy_dir_path_btn",5,42,20,0)
tde4.setWidgetAttachModes(req,"copy_dir_path_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"copy_dir_path_btn",200,20)
tde4.addButtonWidget(req,"copy_full_path_btn","Copy full path to clipboard")
tde4.setWidgetOffsets(req,"copy_full_path_btn",47,78,20,0)
tde4.setWidgetAttachModes(req,"copy_full_path_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"copy_full_path_btn",200,20)
tde4.addButtonWidget(req,"close_btn","Close")
tde4.setWidgetOffsets(req,"close_btn",83,95,20,0)
tde4.setWidgetAttachModes(req,"close_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WIDGET","ATTACH_NONE")
tde4.setWidgetSize(req,"close_btn",80,20)
tde4.setWidgetLinks(req,"directory_path_txt","","","","")
tde4.setWidgetLinks(req,"file_name_txt","","","directory_path_txt","")
tde4.setWidgetLinks(req,"full_path_txt","","","file_name_txt","")
tde4.setWidgetLinks(req,"copy_dir_path_btn","","","full_path_txt","")
tde4.setWidgetLinks(req,"copy_full_path_btn","","","full_path_txt","")
tde4.setWidgetLinks(req,"close_btn","","","full_path_txt","")

if project_path:
	# Set paths
	full_path = project_path
	tde4.setWidgetValue(req, "full_path_txt", full_path)

	file_name = os.path.basename(project_path)
	tde4.setWidgetValue(req, "file_name_txt", file_name)

	dir_path = project_path.replace(file_name, "")
	tde4.setWidgetValue(req, "directory_path_txt", dir_path)

# Callbacks
tde4.setWidgetCallbackFunction(req, "copy_dir_path_btn", "copy_dir_path_clicked")
tde4.setWidgetCallbackFunction(req, "copy_full_path_btn", "copy_full_path_clicked")
tde4.setWidgetCallbackFunction(req, "close_btn", "close_btn_clicked")

tde4.postCustomRequesterAndContinue(req,WINDOW_TITLE,750,155)