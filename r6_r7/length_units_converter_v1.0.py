# 3DE4.script.name: Length Units Converter...
# 3DE4.script.version:v1.0
# April 02 2018
# Montreal
# Patcha Saheb (patchasaheb@gmail.com)




window_title = "Patcha Length Units Converter v1.0"
req = tde4.createCustomRequester()

#add Centimeters text field widget...
tde4.addTextFieldWidget(req,"cm_widget","Centimetre(cm)","1.0")
tde4.setWidgetAttachModes(req,"cm_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"cm_widget",28,48,10,0)

#add Metres text field widget...
tde4.addTextFieldWidget(req,"m_widget","Metre(m)","0.01")
tde4.setWidgetAttachModes(req,"m_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"m_widget",75,95,10,0)

#add Millimetres text field widget...
tde4.addTextFieldWidget(req,"mm_widget","Millimetre(mm)","10.0")
tde4.setWidgetAttachModes(req,"mm_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"mm_widget",28,48,50,0)

#add KiloMetres text field widget...
tde4.addTextFieldWidget(req,"km_widget","Kilometre(km)","0.00001")
tde4.setWidgetAttachModes(req,"km_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"km_widget",75,95,50,0)

#add Miles text field widget...
tde4.addTextFieldWidget(req,"mi_widget","Mile(mi)","0.000006")
tde4.setWidgetAttachModes(req,"mi_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"mi_widget",28,48,90,0)

#add Yards text field widget...
tde4.addTextFieldWidget(req,"yd_widget","Yard(yd)","0.01093")
tde4.setWidgetAttachModes(req,"yd_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"yd_widget",75,95,90,0)

#add Feets text field widget...
tde4.addTextFieldWidget(req,"ft_widget","Feet(ft)","0.0328")
tde4.setWidgetAttachModes(req,"ft_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"ft_widget",28,48,130,0)

#add Inches text field widget...
tde4.addTextFieldWidget(req,"in_widget","Inch(in)","0.3937")
tde4.setWidgetAttachModes(req,"in_widget","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
tde4.setWidgetOffsets(req,"in_widget",75,95,130,0)
























tde4.postCustomRequesterAndContinue(req,window_title,500,175)
