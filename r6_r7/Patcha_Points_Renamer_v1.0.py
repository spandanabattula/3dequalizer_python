# 3DE4.script.name:	Patcha Points Renamer...
# 3DE4.script.version:	v1.0
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.comment:	Renames selected points.
# Author : Patcha Saheb (patchasaheb@gmail.com)
#03-Feb-2015.

class Renamer:

	def Search(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		search_v = str(tde4.getWidgetValue(self.req,"search"))
		replace_v = str(tde4.getWidgetValue(self.req,"replace"))
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		if pg!= None and cam != None:
			if len(tde4.getPointList(pg,1)) > 0:
				for point in tde4.getPointList(pg,1):
					point_name = str(tde4.getPointName(pg,point))
					newname = point_name.replace(search_v,replace_v)
					tde4.setPointName(pg,point,newname)
					tde4.setPointName(pg,point,newname.replace("None",""))
			else:
				tde4.postQuestionRequester(self.window_title,"Error, atleast one point must be selected","Ok")
		else:
			tde4.postQuestionRequester(self.window_title,"Error, there is no Camera or PGroup","Ok")
			
	def Prefix(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		prefix_v = tde4.getWidgetValue(self.req,"prefix")	
		if pg!= None and cam != None:
			if len(tde4.getPointList(pg,1)) > 0:
				for point in tde4.getPointList(pg,1):
					point_name = str(tde4.getPointName(pg,point))	
					newname = "%s%s"%(prefix_v,point_name)
					tde4.setPointName(pg,point,newname)
					tde4.setPointName(pg,point,newname.replace("None",""))				
			else:
				tde4.postQuestionRequester(self.window_title,"Error, atleast one point must be selected","Ok")
		else:
			tde4.postQuestionRequester(self.window_title,"Error, there is no Camera or PGroup","Ok")
			
	def Suffix(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()			
		suffix_v = tde4.getWidgetValue(self.req,"suffix")
		if pg!= None and cam != None:
			if len(tde4.getPointList(pg,1)) > 0:					
				for point in tde4.getPointList(pg,1):			
					point_name = str(tde4.getPointName(pg,point))				
					newname = "%s%s"%(point_name,suffix_v)
					tde4.setPointName(pg,point,newname)
					tde4.setPointName(pg,point,newname.replace("None",""))		
			else:
				tde4.postQuestionRequester(self.window_title,"Error, atleast one point must be selected","Ok")
		else:
			tde4.postQuestionRequester(self.window_title,"Error, there is no Camera or PGroup","Ok")
			
	def Rename(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()	
		rename_v = tde4.getWidgetValue(self.req,"rename")
		if pg!= None and cam != None:
			p_list = tde4.getPointList(pg,1)		
			if len(tde4.getPointList(pg,1)) > 0:
				try:
					start_v = int(tde4.getWidgetValue(self.req,"start"))
					padding_v = int(tde4.getWidgetValue(self.req,"padding"))
					padding = "0" * padding_v
					new_name_list = []
					for i in range(start_v,len(p_list)+start_v):
						for point in p_list:
							point_name = str(tde4.getPointName(pg,point))	
							i = str(i)
							newname = "%s%s"%(rename_v,str(i.rjust(padding_v,"0")))
							new_name_list.append(newname)
							break
					for index in range(len(p_list)):
						tde4.setPointName(pg,p_list[index],str(new_name_list[index]))
				except (ValueError,NameError,TypeError):
					tde4.postQuestionRequester(self.window_title, "Error, all 3 fields values required, 'Start #' and 'Padding' values should be integer", "Ok")
			else:
				tde4.postQuestionRequester(self.window_title,"Error, atleast one point must be selected","Ok")
		else:
			tde4.postQuestionRequester(self.window_title,"Error, there is no Camera or PGroup","Ok")
			
	def Counting(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		if pg!= None and cam != None:
			selected_points = tde4.getPointList(pg,1)
			all_points = tde4.getPointList(pg,0)
			s = tde4.getWidgetValue(self.req,"selected")
			a = tde4.getWidgetValue(self.req,"allpoints")
			if s == 1 and a == 1:
				v =  str(len(selected_points)) + str(",") + str(len(all_points))
				tde4.setWidgetValue(self.req,"count",str(v))
			if s == 1 and a == 0:
				tde4.setWidgetValue(self.req,"count",str(len(selected_points)))
			if a == 1 and s == 0:
				tde4.setWidgetValue(self.req,"count",str(len(all_points)))	
			if s == 0 and a == 0:
				tde4.setWidgetValue(self.req,"count"," ")
		else:
			tde4.postQuestionRequester(self.window_title,"Error, there is no Camera or PGroup","Ok")		
		
	def main(self):
		self.UI()
		
	def UI(self):
		self.window_title = "Patcha Points Renamer v1.0"
		self.req	= tde4.createCustomRequester()
#sep0 widget	
		tde4.addSeparatorWidget(self.req,"sep0")
		tde4.setWidgetAttachModes(self.req,"sep0","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep0",1,99,5,0)	
#search widget	
		tde4.addTextFieldWidget(self.req,"search","Search")
		tde4.setWidgetAttachModes(self.req,"search","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"search",20,98,25,0)	
#replace widget
		tde4.addTextFieldWidget(self.req,"replace","Replace")
		tde4.setWidgetAttachModes(self.req,"replace","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"replace",20,98,50,0)		
#search and replace button widget
		tde4.addButtonWidget(self.req,"s&r","Search and Replace",70,10)
		tde4.setWidgetAttachModes(self.req,"s&r","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"s&r",2,98,75,0)	
#sep1 widget	
		tde4.addSeparatorWidget(self.req,"sep1")
		tde4.setWidgetAttachModes(self.req,"sep1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep1",1,99,95,0)			
#prefix widget
		tde4.addTextFieldWidget(self.req,"prefix","Prefix")
		tde4.setWidgetAttachModes(self.req,"prefix","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"prefix",20,98,115,0)		
#prefix button widget	
		tde4.addButtonWidget(self.req,"addprefix","Add Prefix",70,10)
		tde4.setWidgetAttachModes(self.req,"addprefix","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"addprefix",2,98,140,0)
#sep2 widget			
		tde4.addSeparatorWidget(self.req,"sep2")
		tde4.setWidgetAttachModes(self.req,"sep2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep2",1,99,160,0)	
#suffix widget
		tde4.addTextFieldWidget(self.req,"suffix","Suffix")
		tde4.setWidgetAttachModes(self.req,"suffix","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"suffix",20,98,180,0)
#suffix button widget
		tde4.addButtonWidget(self.req,"addsuffix","Add Suffix",70,10)
		tde4.setWidgetAttachModes(self.req,"addsuffix","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"addsuffix",2,98,205,0)	
#sep3 widget	
		tde4.addSeparatorWidget(self.req,"sep3")
		tde4.setWidgetAttachModes(self.req,"sep3","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep3",1,99,225,0)	
#rename widget
		tde4.addTextFieldWidget(self.req,"rename","Rename")
		tde4.setWidgetAttachModes(self.req,"rename","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rename",20,98,245,0)	
#start widget
		tde4.addTextFieldWidget(self.req,"start","Start #")
		tde4.setWidgetAttachModes(self.req,"start","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"start",20,98,270,0)		
#padding widget
		tde4.addTextFieldWidget(self.req,"padding","Padding")
		tde4.setWidgetAttachModes(self.req,"padding","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"padding",20,98,295,0)		
#rename and number widget
		tde4.addButtonWidget(self.req,"r&n","Rename and Number",70,10)
		tde4.setWidgetAttachModes(self.req,"r&n","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"r&n",2,98,320,0)		
#sep4 widget	
		tde4.addSeparatorWidget(self.req,"sep")
		tde4.setWidgetAttachModes(self.req,"sep","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep",1,99,340,0)		
#count widget
		tde4.addTextFieldWidget(self.req,"count","")
		tde4.setWidgetAttachModes(self.req,"count","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"count",15,55,360,0)	
		tde4.setWidgetSensitiveFlag(self.req,"count",0)
#count button widget
		tde4.addButtonWidget(self.req,"count_button","Count",70,10)
		tde4.setWidgetAttachModes(self.req,"count_button","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"count_button",60,85,360,0)	
#selected points widget
		tde4.addToggleWidget(self.req,"selected","Selected Points",0)
		tde4.setWidgetAttachModes(self.req,"selected","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"selected",40,46,390,0)	
#all points widget
		tde4.addToggleWidget(self.req,"allpoints","All Points",0)
		tde4.setWidgetAttachModes(self.req,"allpoints","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"allpoints",85,91,390,0)
#callbacks
		tde4.setWidgetCallbackFunction(do.req,"s&r","do.Search")
		tde4.setWidgetCallbackFunction(do.req,"addprefix","do.Prefix")	
		tde4.setWidgetCallbackFunction(do.req,"addsuffix","do.Suffix")	
		tde4.setWidgetCallbackFunction(do.req,"r&n","do.Rename")		
		tde4.setWidgetCallbackFunction(do.req,"count_button","do.Counting")
		tde4.postCustomRequesterAndContinue(self.req,self.window_title,310,423)	
do = Renamer()
do.main()		
		

