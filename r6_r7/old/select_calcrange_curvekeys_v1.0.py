# 3DE4.script.name:	Select Calc Range Curve Keys...
# 3DE4.script.version:	v1.0
# 3DE4.script.gui:	Curve Editor::Edit
# 3DE4.script.comment:	Selects current curves keys from calc range.
# Patcha Saheb(patchasaheb@gmail.com)
# 27 Sep 2019(Montreal)





tde4.pushCurrentCurvesToUndoStack()
currentCurve = tde4.getFirstCurrentCurve()

while currentCurve!=None:
   pg = tde4.getCurrentPGroup()
   cam = tde4.getCurrentCamera()
   calc_range = tde4.getCameraCalculationRange(cam)

   for i in range(calc_range[0], calc_range[1]+1):
      key_list = tde4.getCurveKeyList(currentCurve, 0)
      for key in key_list:
         pos = tde4.getCurveKeyPosition(currentCurve, key)
         if pos[0] == i:
            tde4.setCurveKeySelectionFlag(currentCurve, key, 1)

   currentCurve = tde4.getNextCurrentCurve(currentCurve)

