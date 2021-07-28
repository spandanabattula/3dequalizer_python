# 3DE4.script.name:	Deform Live
# 3DE4.script.version: v1.1    
# 3DE4.script.gui.button:   Manual Tracking Controls::Deform Live, align-bottom-left, 80, 20
# 3DE4.script.comment:  Offsets or deforms a 2D tracking curve based on a buffered source curve and its edited versions.
# Wolfgang Niedermeier 2012
# Modified by Patcha Saheb(patchasaheb@gmail.com) 2019

import tde4dtr


def Test(req):
   global dtr
   dtr = tde4dtr.DeformTrack()
   if tde4.getWidgetValue(req, "live_toggle") == 1:
      dtr.evalDeform()


def _deformTrackCallback(req, widget, action):
    global dtr
    if widget == 'buffer_track':
        dtr = tde4dtr.DeformTrack()
        dtr.bufferCurve()
        tde4.setWidgetSensitiveFlag(req, 'restore_track', True)
        tde4.setWidgetSensitiveFlag(req, 'deform_track', True)
        tde4.setWidgetSensitiveFlag(req, 'create_key', True)
        tde4.setWidgetSensitiveFlag(req, 'remove_key', True)
        tde4.setWidgetSensitiveFlag(req, 'import_keys', True)
        tde4.setWidgetSensitiveFlag(req, 'auto_extend', True)
    if widget == 'restore_track':
        dtr.restoreCurve()
    if widget == 'deform_track':
        dtr.evalDeform()
    if widget == 'create_key':
        dtr.createKey()
    if widget == 'remove_key':
        dtr.removeKey()
    if widget == 'import_keys':
        dtr.importKeys()
    if widget == 'auto_extend':
        dtr.toggleAutoExtend()
    return


try:
    req = _deform_track_buttons_live
except (ValueError,NameError,TypeError):
   req = tde4.createCustomRequester()
   _deform_track_buttons_live = req
   tde4.addButtonWidget(req, 'buffer_track', 'Buffer Track', 130, 10)
   tde4.setWidgetCallbackFunction(req, 'buffer_track', '_deformTrackCallback')

   tde4.addButtonWidget(req, 'restore_track', 'Restore Track', 130, 10)
   tde4.setWidgetCallbackFunction(req, 'restore_track', '_deformTrackCallback')

   tde4.addSeparatorWidget(req,'sep1')

   tde4.addButtonWidget(req, 'deform_track', 'Deform Track', 130, 10)
   tde4.setWidgetCallbackFunction(req, 'deform_track', '_deformTrackCallback')

   tde4.addSeparatorWidget(req,'sep2')

   tde4.addButtonWidget(req, 'create_key', 'Create Key', 130, 10)
   tde4.setWidgetCallbackFunction(req, 'create_key', '_deformTrackCallback')

   tde4.addButtonWidget(req, 'remove_key', 'Remove Key', 130, 10)
   tde4.setWidgetCallbackFunction(req, 'remove_key', '_deformTrackCallback')

   tde4.addButtonWidget(req, 'import_keys', 'Import Keys', 130, 10)
   tde4.setWidgetCallbackFunction(req, 'import_keys', '_deformTrackCallback')

   tde4.addSeparatorWidget(req,'sep3')

   tde4.addButtonWidget(req, 'auto_extend', 'Auto Extend', 130, 10)
   tde4.setWidgetCallbackFunction(req, 'auto_extend', '_deformTrackCallback')

   tde4.addSeparatorWidget(req,'sep4')

   tde4.addToggleWidget(req, "live_toggle", "Live Update", 0 )
   tde4.setWidgetOffsets(req, "live_toggle", 70,10,0,0)



try:
    dtr
    tde4.setWidgetSensitiveFlag(req, 'restore_track', True)
    tde4.setWidgetSensitiveFlag(req, 'deform_track', True)
    tde4.setWidgetSensitiveFlag(req, 'create_key', True)
    tde4.setWidgetSensitiveFlag(req, 'remove_key', True)
    tde4.setWidgetSensitiveFlag(req, 'import_keys', True)
    tde4.setWidgetSensitiveFlag(req, 'auto_extend', True)
except:
    tde4.setWidgetSensitiveFlag(req, 'restore_track', False)
    tde4.setWidgetSensitiveFlag(req, 'deform_track', False)
    tde4.setWidgetSensitiveFlag(req, 'create_key', False)
    tde4.setWidgetSensitiveFlag(req, 'remove_key', False)
    tde4.setWidgetSensitiveFlag(req, 'import_keys', False)
    tde4.setWidgetSensitiveFlag(req, 'auto_extend', False)

tde4.postCustomRequesterAndContinue(req, "v1.1", 150, 310, "Test")

