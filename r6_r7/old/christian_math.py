"""r = tde4.createCustomRequester()
tde4.addTextFieldWidget(r,"textfield1","t1","1")
tde4.addTextFieldWidget(r,"textfield2","t2","2")
tde4.addTextFieldWidget(r,"textfield3","t3","3")


#Stick left and right to the requester with distance 20 to left and 10 to right
#ATTACH_WINDOW for left sticks left widget border to left window border
#ATTACH_WINDOW for right sticks right widget border to right window border
#ATTACH_OPPOSITE_WINDOW sticks left widget border to right window border and right widget border to left window border
tde4.setWidgetAttachModes(r,"textfield1","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_AS_IS","ATTACH_AS_IS")
tde4.setWidgetOffsets(r,"textfield1",40,10,10,10)

#Stick left and right to the requester with distance 20% to left and 50% to left !!!!
tde4.setWidgetAttachModes(r,"textfield2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_AS_IS")
tde4.setWidgetOffsets(r,"textfield2",20,40,10,10)

#Attaching textfield3 to texfield2
# textfield3.left attach to textfield2.right (ATTACH_WIDGET)
# textfield3.top attach to textfield2.top (ATTACH_OPPOSITE_WIDGET) --- ATTACH_WIDGET would link textfield3.top to textfield2.bottom
tde4.setWidgetAttachModes(r,"textfield3","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetLinks(r,"textfield3","textfield2","","textfield2","")
tde4.setWidgetOffsets(r,"textfield3",20,10,00,40)
#we have no bottom link defined -> adjust height
tde4.setWidgetSize(r,"textfield3",20,20)


tde4.postCustomRequesterAndContinue(r,"Hello World", 300,300)"""





r = tde4.createCustomRequester()
tde4.addTextFieldWidget(r,"textfield1","t1","1")
tde4.addTextFieldWidget(r,"textfield2","t2","2")
tde4.addTextFieldWidget(r,"textfield3","t3","3")


#Stick left and right to the requester with distance 20 to left and 10 to right
#ATTACH_WINDOW for left sticks left widget border to left window border
#ATTACH_WINDOW for right sticks right widget border to right window border
#ATTACH_OPPOSITE_WINDOW sticks left widget border to right window border and right widget border to left window border
tde4.setWidgetAttachModes(r,"textfield1","ATTACH_WINDOW","ATTACH_WINDOW","ATTACH_AS_IS","ATTACH_AS_IS")
tde4.setWidgetOffsets(r,"textfield1",40,10,10,10)

#Stick left and right to the requester with distance 20% to left and 50% to left !!!!
tde4.setWidgetAttachModes(r,"textfield2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_AS_IS","ATTACH_AS_IS")
tde4.setWidgetOffsets(r,"textfield2",20,40,10,10)

#Attaching textfield3 to texfield2
# textfield3.left attach to textfield2.right (ATTACH_WIDGET)
# textfield3.top attach to textfield2.top (ATTACH_OPPOSITE_WIDGET) --- ATTACH_WIDGET would link textfield3.top to textfield2.bottom
tde4.setWidgetAttachModes(r,"textfield3","ATTACH_WIDGET","ATTACH_WINDOW","ATTACH_OPPOSITE_WIDGET","ATTACH_NONE")
tde4.setWidgetLinks(r,"textfield3","textfield2","","textfield2","")
tde4.setWidgetOffsets(r,"textfield3",30,10,00,40)
#we have no bottom link defined -> adjust height
tde4.setWidgetSize(r,"textfield3",20,20)


tde4.postCustomRequesterAndContinue(r,"Hello World", 300,300)
