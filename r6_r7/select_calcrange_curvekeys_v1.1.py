# 3DE4.script.name:	Select Calc Range Curve Keys...
# 3DE4.script.version:	v1.1
# 3DE4.script.gui:	Curve Editor::Edit
# 3DE4.script.comment:	Selects current curves keys from calc range.
# Patcha Saheb(patchasaheb@gmail.com)
# 27 Sep 2019(Montreal)

def doIt(requester,widget,action):
   tde4.pushCurrentCurvesToUndoStack()
   currentCurve = tde4.getFirstCurrentCurve()

   while currentCurve!=None:
      pg = tde4.getCurrentPGroup()
      cam = tde4.getCurrentCamera()
      frames = tde4.getCameraNoFrames(cam)
      current_frame = tde4.getCurrentFrame(cam)

      if widget == "all_keys_btn":
         calc_range = tde4.getCameraCalculationRange(cam)
      if widget == "intermediate_keys_btn":
         calc_range = tde4.getCameraCalculationRange(cam)
         calc_range[0] = calc_range[0] + 1
         calc_range[1] = calc_range[1] - 1
      if widget == "current_frame_keys_btn":
         calc_range = tde4.getCameraCalculationRange(cam)

      #clear selection
      for i in range(1,frames+1):
         key_list = tde4.getCurveKeyList(currentCurve, 0)
         for key in key_list:
            pos = tde4.getCurveKeyPosition(currentCurve, key)
            if pos[0] == i:
               tde4.setCurveKeySelectionFlag(currentCurve, key, 0)     

      #make selection
      for i in range(calc_range[0], calc_range[1]+1):
         key_list = tde4.getCurveKeyList(currentCurve, 0)
         for key in key_list:
            pos = tde4.getCurveKeyPosition(currentCurve, key)
            if pos[0] == i:
               tde4.setCurveKeySelectionFlag(currentCurve, key, 1)

            #deselect current frame curve key
            if widget == "current_frame_keys_btn":
               if pos[0] == float(current_frame):
                  tde4.setCurveKeySelectionFlag(currentCurve, key, 0)

      currentCurve = tde4.getNextCurrentCurve(currentCurve)


#gui
window_title = "Patcha Select CalcRange Curve Keys v1.1"

requester = tde4.createCustomRequester()
tde4.addLabelWidget(requester,"label_text","Selection will work on Calculation range","ALIGN_LABEL_CENTER")
tde4.setWidgetOffsets(requester,"label_text",10,90,7,501)
tde4.setWidgetAttachModes(requester,"label_text","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.addButtonWidget(requester,"all_keys_btn","Select all keys")
tde4.setWidgetOffsets(requester,"all_keys_btn",10,90,37,501)
tde4.setWidgetAttachModes(requester,"all_keys_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(requester,"all_keys_btn",80,20)
tde4.addButtonWidget(requester,"intermediate_keys_btn","Select all keys exclude first & last")
tde4.setWidgetOffsets(requester,"intermediate_keys_btn",10,90,72,501)
tde4.setWidgetAttachModes(requester,"intermediate_keys_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(requester,"intermediate_keys_btn",80,20)
tde4.setWidgetLinks(requester,"all_keys_btn","","","","")
tde4.setWidgetLinks(requester,"intermediate_keys_btn","","","","")

tde4.addButtonWidget(requester,"current_frame_keys_btn","Select all keys exclude current frame")
tde4.setWidgetOffsets(requester,"current_frame_keys_btn",10,90,112,501)
tde4.setWidgetAttachModes(requester,"current_frame_keys_btn","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_NONE")
tde4.setWidgetSize(requester,"current_frame_keys_btn",80,20)
tde4.setWidgetLinks(requester,"intermediate_keys_btn","","","","")
tde4.setWidgetLinks(requester,"current_frame_keys_btn","","","","")

#Callbacks
tde4.setWidgetCallbackFunction(requester,"all_keys_btn","doIt")
tde4.setWidgetCallbackFunction(requester,"intermediate_keys_btn","doIt")
tde4.setWidgetCallbackFunction(requester,"current_frame_keys_btn","doIt")

tde4.postCustomRequesterAndContinue(requester,window_title,380,150)
