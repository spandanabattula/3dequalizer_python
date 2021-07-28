# 3DE4.script.name:     Create Seq Camera from Ref Cameras...
# 3DE4.script.version:  v1.0
# 3DE4.script.gui:	Object Browser::Context Menu Reference Camera

# Patcha Saheb(patchasaheb@gmail.com)
# Montreal, Canada.


import tde4
import os, sys
import os.path

WINDOW_TITLE = "Create Sequence Camera from Reference Cameras v1.0"
SUFFIX = "COMBINED"

pg = tde4.getCurrentPGroup()
pg_type = tde4.getPGroupType(pg)
cam = tde4.getCurrentCamera()
cam_name = tde4.getCameraName(cam)
cam_type = tde4.getCameraType(cam)
cam_path = tde4.getCameraPath(cam)
image_name = cam_path.split(".")[0]
image_format = cam_path.split(".")[2]
lens = tde4.getCameraLens(cam)
ld_model = str(tde4.getLensLDModel(lens))
fback_width = tde4.getLensFBackWidth(lens)	
fback_height = tde4.getLensFBackHeight(lens)	
cam_list = tde4.getCameraList(0)

ref_cams = []

#used from 3de scripts 'duplicatelens' 
def duplicateLens(lens_id):
	l0	= lens_id
	l	= tde4.createLens()
	
	name	= tde4.getLensName(l0)
	name	= name+"`"
	tde4.setLensName(l,name)

	d	= tde4.getLensFBackWidth(l0)
	tde4.setLensFBackWidth(l,d)
	d	= tde4.getLensFBackHeight(l0)
	tde4.setLensFBackHeight(l,d)
	
	fl	= tde4.getLensFocalLength(l0)
	tde4.setLensFocalLength(l,fl)
	
	focus	= tde4.getLensFocus(l0)
	tde4.setLensFocus(l,focus)

	d	= tde4.getLensFilmAspect(l0)
	tde4.setLensFilmAspect(l,d)

	d	= tde4.getLensLensCenterX(l0)
	tde4.setLensLensCenterX(l,d)

	d	= tde4.getLensLensCenterY(l0)
	tde4.setLensLensCenterY(l,d)

	d	= tde4.getLensPixelAspect(l0)
	tde4.setLensPixelAspect(l,d)

	return l

# Close button callback
def closeButtonCallback(req, widget, action):
	tde4.unpostCustomRequester(req)

# Create camera callback
def createCameraCallback(req, widget, action):
	# Duplicate lens and set properties
	new_lens = duplicateLens(lens)
	new_name = tde4.getWidgetValue(req, "camera_name_text")
	tde4.setLensName(new_lens, new_name)
	tde4.setLensLDModel(new_lens, ld_model)
	tde4.setLensDynamicDistortionMode(new_lens, "DISTORTION_DYNAMIC_FOCUS_DISTANCE")

	# New camera image sequence path
	new_path = image_name + "." + "####" + "." + image_format

	# Image sequence directory
	"""pattern = new_path.split(str(image_name[0]))[-1]
	image_dir = str(new_path).replace(pattern, "")
	images = os.listdir(image_dir)
	images.sort()"""

	image_dir = os.path.split(new_path)[0]
	images = os.listdir(image_dir)
	images.sort()

	# Get image sequence start and end frames
	total_frames_list = []
	pattern= os.path.split(new_path)[1]
	pattern_split = pattern.split(".")
	for image in images:
		image_split = image.split(".")
		if pattern_split[0] == image_split[0]:
			if len(pattern_split) == len(image_split):
				total_frames_list.append(image_split[1])



	# Create new camera and set properties
	new_cam = tde4.createCamera("SEQUENCE")
	tde4.setCameraName(new_cam, new_name)
	tde4.setCameraPath(new_cam, new_path)

	start_frame = int(min(total_frames_list))
	end_frame = int(max(total_frames_list))

	tde4.setCameraSequenceAttr(new_cam, start_frame, end_frame, 1)
	tde4.setCameraLens(new_cam, new_lens)
	tde4.setCameraFocalLengthMode(new_cam, "FOCAL_DYNAMIC")
	tde4.setCameraFocusMode(new_cam, "FOCUS_DYNAMIC")
	b,w	= tde4.getCamera8BitColorBlackWhite(cam)
	tde4.setCamera8BitColorBlackWhite(new_cam,b,w)
	gamma	= tde4.getCamera8BitColorGamma(cam)
	tde4.setCamera8BitColorGamma(new_cam,gamma)
	sclip	= tde4.getCamera8BitColorSoftclip(cam)
	tde4.setCamera8BitColorSoftclip(new_cam,sclip)
	# Set Focus curve linear
	focus_curve = tde4.getCameraFocusCurve(new_cam)
	key = tde4.createCurveKey(focus_curve, [1.0,1.0])
	tde4.setCurveKeyMode(focus_curve, key, "LINEAR")
	frames_length = tde4.getCameraNoFrames(new_cam)
	key = tde4.createCurveKey(focus_curve, [frames_length, frames_length])
	tde4.setCurveKeyMode(focus_curve, key, "LINEAR")

	for ref_cam in ref_cams:
		# (b+1)-a(Thanks to Spandana)
		ref_cam_frame = tde4.getCameraPath(ref_cam)
		ref_cam_frame = ref_cam_frame.split(".")[-2]
		frame = (int(ref_cam_frame) + 1) - start_frame
		ref_cam_lens = tde4.getCameraLens(ref_cam)
				
		# Set transformation on new sequence camera
		pos3d = tde4.getPGroupPosition3D(pg, ref_cam, 1)
		rot3d = tde4.getPGroupRotation3D(pg, ref_cam, 1)
		tde4.setPGroupPosition3D(pg, new_cam, frame, pos3d)
		tde4.setPGroupRotation3D(pg, new_cam, frame, rot3d)

		# Set animated focal
		ref_cam_focal = tde4.getLensFocalLength(ref_cam_lens)
		tde4.setCameraFocalLength(new_cam, frame, ref_cam_focal)

		# Set animated distortion
		no_of_params = tde4.getLDModelNoParameters(ld_model)
		ref_cam_focus = tde4.getCameraFocus(ref_cam, 1)		
		for parameter in range(no_of_params):
			parameter_name = tde4.getLDModelParameterName(ld_model, parameter)
			if tde4.getLDModelParameterType(ld_model,parameter_name)=="LDP_DOUBLE_ADJUST":
				parameter_value = tde4.getLensLDAdjustableParameter(ref_cam_lens, parameter_name, ref_cam_focal, ref_cam_focus)
				parameter_curve = tde4.getLensLDAdjustableParameterCurve(new_lens, parameter_name)
				key = tde4.createCurveKey(parameter_curve, [frame, parameter_value])
				tde4.setCurveKeyMode(parameter_curve, key, "LINEAR")
				tde4.setCurveKeyFixedXFlag(parameter_curve, key, 1)
		

	# Handle postfilter mode
	current_mode = tde4.getPGroupPostfilterMode(pg)
	tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
	tde4.filterPGroup(pg, new_cam)			
	tde4.setPGroupPostfilterMode(pg, current_mode)

	# Set new camera as current camera
	tde4.setCurrentCamera(new_cam)


# Open window function
def showUI():
	# Check reference camera type
	if not cam_type== "REF_FRAME":
		tde4.postQuestionRequester(WINDOW_TITLE, "Current camera type is not a Referece camera.","Ok")
		return

	# Check camera pgroup type
	if not pg_type == "CAMERA":
		tde4.postQuestionRequester(WINDOW_TITLE, "Current point group is not a camera point group.","Ok")
		return

	# Declare check variables
	have_same_film_back = True
	have_same_ld_model = True
	have_all_lenses = True

	# Check reference cameras have same film back and distortion model
	for camera in cam_list:
		if tde4.getCameraType(camera) == "REF_FRAME":
			path = tde4.getCameraPath(camera).split(".")[0]
			if image_name == path:
				camera_lens = tde4.getCameraLens(camera)
				if not camera_lens:
					have_all_lenses = False
					break
				camera_lens_fback_width = tde4.getLensFBackWidth(camera_lens)
				camera_lens_fback_height = tde4.getLensFBackHeight(camera_lens)
				camera_lens_ld_model = tde4.getLensLDModel(camera_lens)
				if not camera_lens_fback_width == fback_width or not camera_lens_fback_height == fback_height:
					have_same_film_back = False
					break
				if not camera_lens_ld_model == ld_model:
					have_same_ld_model = False
					break
				if have_same_ld_model is True and have_same_film_back is True:
					ref_cams.append(camera)

	if have_all_lenses is False:
		tde4.postQuestionRequester(WINDOW_TITLE, "Few of same image sequence referece cameras are not connected with any lense.","Ok")
		return

	if have_same_film_back is False:
		tde4.postQuestionRequester(WINDOW_TITLE, "Same image sequence referece cameras film back values are not same.","Ok")
		return

	if have_same_ld_model is False:
		tde4.postQuestionRequester(WINDOW_TITLE, "Same image sequence referece cameras lens distortion model is not same.","Ok")
		return

	new_cam_name = cam_name + "_" + SUFFIX

	# GUI
	req = tde4.createCustomRequester()
	tde4.addListWidget(req,"ref_cams_list","Ref cameras",0)
	tde4.setWidgetOffsets(req,"ref_cams_list",98,10,12,100)
	tde4.setWidgetAttachModes(req,"ref_cams_list","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_WINDOW")
	tde4.setWidgetSize(req,"ref_cams_list",150,250)

	tde4.addLabelWidget(req,"camera_name_label","New Camera Name","ALIGN_LABEL_LEFT")
	tde4.setWidgetOffsets(req,"camera_name_label",5,5,-80,0)
	tde4.setWidgetAttachModes(req,"camera_name_label","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
	tde4.setWidgetSize(req,"camera_name_label",100,20)

	tde4.addTextFieldWidget(req,"camera_name_text","","")
	tde4.setWidgetOffsets(req,"camera_name_text",135,10,0,0)
	tde4.setWidgetAttachModes(req,"camera_name_text","ATTACH_OPPOSITE_WIDGET","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
	tde4.setWidgetSize(req,"camera_name_text",200,20)
	tde4.addLabelWidget(req,"ld_model_label","   Distortion Model","ALIGN_LABEL_LEFT")
	tde4.setWidgetOffsets(req,"ld_model_label",5,5,30,0)
	tde4.setWidgetAttachModes(req,"ld_model_label","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
	tde4.setWidgetSize(req,"ld_model_label",100,20)
	tde4.addTextFieldWidget(req,"ld_model_text","","")
	tde4.setWidgetOffsets(req,"ld_model_text",135,10,0,0)
	tde4.setWidgetAttachModes(req,"ld_model_text","ATTACH_OPPOSITE_WIDGET","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
	tde4.setWidgetSize(req,"ld_model_text",200,20)
	tde4.setWidgetSensitiveFlag(req,"ld_model_text",0)
	tde4.addButtonWidget(req,"create_camera_btn","Create Sequence camera from Reference cameras")
	tde4.setWidgetOffsets(req,"create_camera_btn",20,110,30,0)
	tde4.setWidgetAttachModes(req,"create_camera_btn","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
	tde4.setWidgetSize(req,"create_camera_btn",80,20)
	tde4.addButtonWidget(req,"close_btn","Close")
	tde4.setWidgetOffsets(req,"close_btn",15,20,0,41)
	tde4.setWidgetAttachModes(req,"close_btn","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
	tde4.setWidgetSize(req,"close_btn",80,20)
	tde4.setWidgetLinks(req,"ref_cams_list","","","","")
	tde4.setWidgetLinks(req,"camera_name_label","","camera_name_text","","")
	tde4.setWidgetLinks(req,"camera_name_text","camera_name_label","","","")
	tde4.setWidgetLinks(req,"ld_model_label","","ld_model_text","","")
	tde4.setWidgetLinks(req,"ld_model_text","ld_model_label","","","")
	tde4.setWidgetLinks(req,"create_camera_btn","","","","")
	tde4.setWidgetLinks(req,"close_btn","create_camera_btn","","","")

	# Set widget values
	tde4.setWidgetValue(req, "camera_name_text", new_cam_name)
	tde4.setWidgetValue(req, "ld_model_text", ld_model)

	# Add reference cameras to list widget
	for count in range(len(ref_cams)):
		ref_cam_name = tde4.getCameraName(ref_cams[count])
		tde4.insertListWidgetItem(req, "ref_cams_list", ref_cam_name)
		tde4.setListWidgetItemSelectableFlag(req, "ref_cams_list", count, 0)

	# Callbacks
	tde4.setWidgetCallbackFunction(req, "close_btn", "closeButtonCallback")
	tde4.setWidgetCallbackFunction(req, "create_camera_btn", "createCameraCallback")

	# Post requester
	tde4.postCustomRequesterAndContinue(req,WINDOW_TITLE,500,375)

showUI()

