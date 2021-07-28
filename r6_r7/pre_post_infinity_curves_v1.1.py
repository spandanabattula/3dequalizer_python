#
# 3DE4.script.name:		Pre/Post infinity curves...
#
# 3DE4.script.version:		v1.1
#
# 3DE4.script.gui:Curve Editor::Edit
#
# 3DE4.script.comment: Extends the pre and post velocity of selected translation, rotation and focal length curves, respecting the Frame Range Calculation mode in the Camera Attribute Editor. Similar to Maya Infinity function.
#
# Patcha Saheb(patchasaheb@gmail.com)
# Montreal(29 August 2018)


from vl_sdv import*

def bakeBufferCurves(pg,start_frame,end_frame):
	cam = tde4.getCurrentCamera()
	frames = tde4.getCameraNoFrames(cam)
	pg_type = tde4.getPGroupType(pg)
	currentFrame = tde4.getCurrentFrame(cam)
	if pg_type == "CAMERA":
		for i in range(start_frame,end_frame+1):
			frame = i
			pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
			rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)
			#focal = tde4.getCameraFocalLength(cam,frame)
			tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
			tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
			tde4.setPGroupScale3D(pg,scale)
			#tde4.setCameraFocalLength(cam,frame,focal)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)
	if pg_type == "OBJECT":
		for i_pg in tde4.getPGroupList():
			if tde4.getPGroupType(i_pg) == "CAMERA":
				id_cpg = i_pg
				break
		id_opg = pg	
		for i in range(start_frame,end_frame+1): 
			frame = i
			rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,cam,frame))
			pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,cam,frame))
			rot_pos_base = igl3d(rot_cpg,pos_cpg)
			rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,cam,frame))
			pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,cam,frame))
			scale = tde4.getPGroupScale3D(pg)
			rot_pos_opg_new = igl3d(rot_opg_global,pos_opg_global).invert() * rot_pos_base
			tde4.setPGroupRotation3D(id_opg,cam,frame,rot_pos_opg_new.m.list())
			tde4.setPGroupPosition3D(id_opg,cam,frame,rot_pos_opg_new.v.list())
			#tde4.setPGroupScale3D(pg,scale)
		pf_mode  = tde4.getPGroupPostfilterMode(pg)
		tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		tde4.filterPGroup(pg,cam)
		tde4.setPGroupPostfilterMode(pg,pf_mode)


def infinityCurves(req,widget,action):

	if widget == "pre_infinity_btn" or widget == "post_infinity_btn":

		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		frames = tde4.getCameraNoFrames(cam)
		curve = tde4.getFirstCurrentCurve()

		while curve != None:
			# remember current state for undo...
			tde4.pushCurrentCurvesToUndoStack()			
			curve_mode = tde4.getCurrentCurveMode()
			if curve_mode == "ROTPOS_CURVES" or curve_mode == "ZOOM_CURVES":

				if tde4.getCameraFrameRangeCalculationFlag(cam) == 1:
					start_frame, end_frame = tde4.getCameraCalculationRange(cam)
				else:
					start_frame = 1
					end_frame = frames + 1

				if widget == "pre_infinity_btn":
					if frame < end_frame:
						bakeBufferCurves(pg,start_frame,end_frame-1)
						current_frame_y = float(tde4.evaluateCurve(curve,frame))
						next_frame_y = float(tde4.evaluateCurve(curve,frame+1))
						slope = current_frame_y - next_frame_y

						if slope != 0.0:
							null = 1
							key_list = tde4.getCurveKeyList(curve,0)
							for key in range(len(key_list),0,-1):
								key_pos2d = tde4.getCurveKeyPosition(curve,key_list[key-1])
								if key_pos2d[0] <= frame-1 and key_pos2d[0] > start_frame-1:
									tde4.setCurveKeyPosition(curve,key_list[key-1],[key_pos2d[0],current_frame_y+(slope*null)])
									null = null + 1
							if tde4.getCurveEditorGlobalSpaceModeFlag() == 1:
								tde4.makePGroupChildSpaceCurvesConsistentToGlobalSpaceCurves(pg)
							tde4.copyPGroupEditCurvesToFilteredCurves(pg,cam)

				if widget == "post_infinity_btn":
					if frame > start_frame:
						bakeBufferCurves(pg,start_frame,end_frame-1)
						current_frame_y = float(tde4.evaluateCurve(curve,frame))
						previous_frame_y = float(tde4.evaluateCurve(curve,frame-1))
						slope =  current_frame_y - previous_frame_y
						if slope != 0.0:
							null = 1
							key_list = tde4.getCurveKeyList(curve,0)
							for key in key_list:
								key_pos2d = tde4.getCurveKeyPosition(curve,key)
								if key_pos2d[0] >= frame+1 and key_pos2d[0] <= end_frame:
									tde4.setCurveKeyPosition(curve,key,[key_pos2d[0],current_frame_y+(slope*null)])
									null = null + 1									
							if tde4.getCurveEditorGlobalSpaceModeFlag() == 1:
								tde4.makePGroupChildSpaceCurvesConsistentToGlobalSpaceCurves(pg)									
							tde4.copyPGroupEditCurvesToFilteredCurves(pg,cam)

			curve = tde4.getNextCurrentCurve(curve)
		tde4.updateGUI()


window_title = "Patcha Pre/Post infinity curves v1.1"
req = tde4.createCustomRequester()


tde4.addButtonWidget(req,"pre_infinity_btn","Pre infinity curves from current frame",70,10)
tde4.setWidgetAttachModes(req,"pre_infinity_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"pre_infinity_btn",5,95,15,0)

tde4.addButtonWidget(req,"post_infinity_btn","Post infinity curves from current frame",70,10)
tde4.setWidgetAttachModes(req,"post_infinity_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"post_infinity_btn",5,95,55,0)

tde4.setWidgetCallbackFunction(req,"pre_infinity_btn","infinityCurves")
tde4.setWidgetCallbackFunction(req,"post_infinity_btn","infinityCurves")



tde4.postCustomRequesterAndContinue(req,window_title,400,100)


