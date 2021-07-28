# 3DE4.script.name:Nudge3D...
# 3DE4.script.version:	 v1.0b2.99
# 3DE4.script.gui.button:	Lineup Controls::Nudge3D, align-bottom-left, 80, 20
# 3DE4.script.gui.button:	Orientation Controls::Nudge3D, align-bottom-left, 70, 20
# 3DE4.script.gui:	Lineup Controls::Edit
# 3DE4.script.gui:	Orientation Controls::Edit
# 3DE4.script.comment:	Nudges translation, rotation and scale, of Cameras, Objects, 3D Models or Motion paths, in Local, Global, Screen space.
# Author : Patcha Saheb (patchasaheb@gmail.com)



from vl_sdv import *
import math


class Nudge():

	def main(self):
		self.GUI()

#update function...		
	def update(self,requester):
		self.req = requester
		s_type = tde4.getWidgetValue(self.req,"selected_menu")	
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		offset = tde4.getCameraFrameOffset(cam)-1
		pl = tde4.getPointList(pg,1)
		r_space = tde4.getWidgetValue(self.req,"r_space")
		if s_type == 2:	
			tde4.setWidgetValue(self.req,"sel",str(tde4.getPGroupName(tde4.getCurrentPGroup())))
		if s_type == 3:
			l = []
			mlist = tde4.get3DModelList(pg,1)
			for model in mlist:
				name = tde4.get3DModelName(pg,model)
				l.append(name)
			tde4.setWidgetValue(self.req,"sel",str(l))

#increment sensitive funciton...
	def Increment_Sensitive(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
#getting widgets values...
		t_slider_v = tde4.getWidgetValue(self.req,"t_increment")
		t_factor_v = tde4.getWidgetValue(self.req,"t_increment_factor")
		r_slider_v = tde4.getWidgetValue(self.req,"r_increment")
		r_factor_v = tde4.getWidgetValue(self.req,"r_increment_factor")
		s_slider_v = tde4.getWidgetValue(self.req,"s_increment")
		s_factor_v = tde4.getWidgetValue(self.req,"s_increment_factor")
#translation increment sensitive...
		if self.widget == "t_increment":
			tde4.setWidgetValue(self.req,"t_increment_factor",str(t_slider_v))
		if self.widget == "t_increment_factor":
			if float(t_factor_v) > 0.1:
				tde4.setWidgetSensitiveFlag(self.req,"t_increment",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)
				tde4.setWidgetValue(self.req,"t_increment",str(t_factor_v))
#rotation increment sensitive...
		if self.widget == "r_increment":
			tde4.setWidgetValue(self.req,"r_increment_factor",str(r_slider_v))
		if self.widget == "r_increment_factor":
			if float(r_factor_v) > 0.1:
				tde4.setWidgetSensitiveFlag(self.req,"r_increment",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
				tde4.setWidgetValue(self.req,"r_increment",str(r_factor_v))
#scale increment sensitive...
		if self.widget == "s_increment":
			tde4.setWidgetValue(self.req,"s_increment_factor",str(s_slider_v))
		if self.widget == "s_increment_factor":
			if float(s_factor_v) > 1.0:
				tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			else:
				tde4.setWidgetSensitiveFlag(self.req,"s_increment",1)
				tde4.setWidgetValue(self.req,"s_increment",str(s_factor_v))

#pivot option menu edit...	
	def Pivot_Menu_Edit(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		s_type = tde4.getWidgetValue(self.req,"selected_menu")
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		pl = tde4.getPointList(pg,1)
		name = tde4.getCameraName(cam)
		t_space = tde4.getWidgetValue(self.req,"t_space")
		r_space = tde4.getWidgetValue(self.req,"r_space")			
		if s_type == 1:
			tde4.modifyOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local/Screen")
			tde4.modifyOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local/Screen","Around 3DPoints")	
			tde4.setWidgetValue(self.req,"sel",str(tde4.getCameraName(tde4.getCurrentCamera())))
			tde4.setWidgetValue(self.req,"look"," ")
		if s_type == 2:
			tde4.modifyOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local","Screen")
			tde4.modifyOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local","Screen","Around 3DPoints")
			tde4.setWidgetValue(self.req,"sel",str(tde4.getPGroupName(tde4.getCurrentPGroup())))	
			if t_space == 3 or r_space == 3:
				tde4.setWidgetValue(self.req,"look",str(tde4.getCameraName(tde4.getCurrentCamera())))	
			else:
				tde4.setWidgetValue(self.req,"look"," ")
		if s_type == 3:
			l = []
			mlist = tde4.get3DModelList(pg,1)
			for model in mlist:
				name = tde4.get3DModelName(pg,model)
				l.append(name)
			tde4.modifyOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local","Screen")
			tde4.modifyOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local","Screen")
			tde4.setWidgetValue(self.req,"sel",str(l))
			if t_space == 3 or r_space == 3:
				tde4.setWidgetValue(self.req,"look",str(tde4.getCameraName(tde4.getCurrentCamera())))
			else:
				tde4.setWidgetValue(self.req,"look"," ")

#disable/enable scale buttons...	
		if s_type == 1 or s_type == 2:
			tde4.setWidgetSensitiveFlag(self.req,"rot_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_z+",1)	
			tde4.setWidgetSensitiveFlag(self.req,"rot_z-",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_increment_factor",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_space",1)	
			tde4.setWidgetSensitiveFlag(self.req,"scale_x+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_x-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z-",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",0)
		if s_type == 3:
			tde4.setWidgetSensitiveFlag(self.req,"rot_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_z+",1)	
			tde4.setWidgetSensitiveFlag(self.req,"rot_z-",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_increment_factor",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_space",1)	
			tde4.setWidgetSensitiveFlag(self.req,"scale_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z+",1)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z-",1)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",1)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",1)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",1)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",1)
		if s_type == 1 or s_type == 2:										
			tde4.setWidgetSensitiveFlag(self.req,"rot_x+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_x-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y+",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_y-",1)
			tde4.setWidgetSensitiveFlag(self.req,"rot_z+",1)	
			tde4.setWidgetSensitiveFlag(self.req,"rot_z-",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_increment",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_increment_factor",1)
			tde4.setWidgetSensitiveFlag(self.req,"r_space",1)										
			tde4.setWidgetSensitiveFlag(self.req,"scale_x+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_x-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_y-",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z+",0)
			tde4.setWidgetSensitiveFlag(self.req,"scale_z-",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",0)
			tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
			tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",0)

#pick pivot point function...	
	def Pick_Pivot(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		pl = tde4.getPointList(pg,1)
		if len(pl) == 1:
			name = tde4.getPointName(pg,pl[0])
			tde4.setWidgetValue(self.req,"pivot_3dpoint",str(name))
		else:
			tde4.postQuestionRequester(self.window_title,"Error, exactly one 3dpoint must be selected.","Ok")			

#average 3dpoint function...	
	def Average_3dpoint(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg =tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		pl = tde4.getPointList(pg,1)
		pg_type = tde4.getPGroupType(pg)
		if len(pl) >= 2 :	
			x_list = []
			y_list = []
			z_list = []
			for point in pl:
				p3d = tde4.getPointCalcPosition3D(pg,point)
				x_list.append(p3d[0])
				y_list.append(p3d[1])
				z_list.append(p3d[2])
			x = sum(x_list) / len(x_list)
			y = sum(y_list) / len(y_list)
			z = sum(z_list) / len(z_list)
			p3d = [x,y,z]
			p = tde4.createPoint(pg)
			tde4.setPointName(pg,p,"Avg_3dpoint_01")
			tde4.setPointSurveyMode(pg,p,"SURVEY_EXACT")
			tde4.setPointSurveyPosition3D(pg,p,p3d)
		else:
			tde4.postQuestionRequester(self.window_title,"Error, atleast two points must be selected.","Ok")

#enable frame range widget function...
	def Frame_Range(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		toggle_value = tde4.getWidgetValue(self.req,"toggle")
		if toggle_value == 1:
			tde4.setWidgetSensitiveFlag(self.req,"frame_in",1)
			tde4.setWidgetSensitiveFlag(self.req,"frame_out",1)
		if toggle_value == 0:
			tde4.setWidgetSensitiveFlag(self.req,"frame_in",0)
			tde4.setWidgetSensitiveFlag(self.req,"frame_out",0)			

#bake buffer curves fuction...
	def Bake_Buffer_Curves(self):
		pg = tde4.getCurrentPGroup()
		cam = tde4.getCurrentCamera()
		frames = tde4.getCameraNoFrames(cam)
		pg_type = tde4.getPGroupType(pg)
		currentFrame = tde4.getCurrentFrame(cam)
		if pg_type == "CAMERA":
			for i in range(1,frames+1):
				tde4.setCurrentFrame(cam,i)
				frame = tde4.getCurrentFrame(cam)	
				pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
				rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
				scale = tde4.getPGroupScale3D(pg)
				focal = tde4.getCameraFocalLength(cam,frame)
				tde4.setPGroupPosition3D(pg,cam,frame,pos.list())
				tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
				tde4.setPGroupScale3D(pg,scale)
				tde4.setCameraFocalLength(cam,frame,focal)
				tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		if pg_type == "OBJECT":
			for i in range(1,frames+1):
				tde4.setCurrentFrame(cam,i)
				frame = tde4.getCurrentFrame(cam)
				obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
				obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
				scale = tde4.getPGroupScale3D(pg)
				focal = tde4.getCameraFocalLength(cam,frame)
				new_values = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), obj_pos.list(), 1.0, 0)
				tde4.setPGroupPosition3D(pg,cam,frame,new_values[1])
				tde4.setPGroupRotation3D(pg,cam,frame,new_values[0])
				tde4.setPGroupScale3D(pg,scale)
				tde4.setCameraFocalLength(cam,frame,focal)
				tde4.setPGroupPostfilterMode(pg,"POSTFILTER_OFF")
		#only change from public, returns to parked frame
		tde4.setCurrentFrame(cam,currentFrame)		

#main callback...			
	def Nudge_Callback(self,requester,widget,action):
		self.req = requester
		self.widget = widget
		self.action = action
		pg = tde4.getCurrentPGroup()
		pgl = tde4.getPGroupList()
		pg_type = tde4.getPGroupType(pg)
		cam = tde4.getCurrentCamera()
		frame = tde4.getCurrentFrame(cam)
		frames = tde4.getCameraNoFrames(cam)
		offset = tde4.getCameraFrameOffset(cam)-1
		mlist = tde4.get3DModelList(pg,1)
		pl = tde4.getPointList(pg,1)
		s_type = tde4.getWidgetValue(self.req,"selected_menu")
		p_space = tde4.getWidgetValue(self.req,"t_space")
		r_space = tde4.getWidgetValue(self.req,"r_space")
		power = tde4.getWidgetValue(self.req,"t_increment_factor")
		r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
		s_power = tde4.getWidgetValue(self.req,"s_increment_factor")
		toggle_value = tde4.getWidgetValue(self.req,"toggle")
		#if camera type selected...
		if s_type == 1:
			if pg_type == "CAMERA":
				if pg != None:
					self.Bake_Buffer_Curves()
					if toggle_value == 0:
						loop_start = frame+offset
						loop_end = (frame+1)+offset
					if toggle_value == 1:
						loop_start = tde4.getWidgetValue(self.req,"frame_in")
						loop_end = tde4.getWidgetValue(self.req,"frame_out")					
					if p_space == 1:
#camera global translation nudge...
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							if loop_start != None and loop_end != None and (int(loop_start)-offset) >= 1 and (int(loop_start)-offset) <= frames and (int(loop_end)-offset) >= 1 and (int(loop_end)-offset) <= frames and (int(loop_start)-offset) <= (int(loop_end)-offset):
								for frame in range(int(loop_start)-offset,(int(loop_end)+1)-offset):
									cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))								
									if toggle_value == 0:
										power = tde4.getWidgetValue(self.req,"t_increment_factor")
									if toggle_value == 1:
										power = tde4.getWidgetValue(self.req,"t_increment_factor")
										power = float(power)/((int(loop_end) - int(loop_start)) + 1)
									if widget == "pos_x+" or widget == "pos_x-":
										if widget == "pos_x-": power = -float(power)
										pos_x = float(cam_pos[0]) + float(power)
										tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,cam_pos[1],cam_pos[2]])
									if widget == "pos_y+" or widget == "pos_y-":
										if widget == "pos_y-": power = -float(power)
										pos_y = float(cam_pos[1]) + float(power)
										tde4.setPGroupPosition3D(pg,cam,frame,[cam_pos[0],pos_y,cam_pos[2]])
									if widget == "pos_z+" or widget == "pos_z-":
										if widget == "pos_z-": power = -float(power)
										pos_z = float(cam_pos[2]) + float(power)
										tde4.setPGroupPosition3D(pg,cam,frame,[cam_pos[0],cam_pos[1],pos_z])
									tde4.filterPGroup(pg,cam)
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please enter correct frame range as you see in timeline or frame out value should be greater than frame in.","Ok")
#camera global rotation nudge...
					if r_space == 1:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							if loop_start != None and loop_end != None and (int(loop_start)-offset) >= 1 and (int(loop_start)-offset) <= frames and (int(loop_end)-offset) >= 1 and (int(loop_end)-offset) <= frames and (int(loop_start)-offset) <= (int(loop_end)-offset):
								for frame in range(int(loop_start)-offset,(int(loop_end)+1)-offset):						
									cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									cam_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))	
									if toggle_value == 0:
										r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
									if toggle_value == 1:
										r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
										r_power = float(r_power)/((int(loop_end) - int(loop_start)) + 1)												
									x_axis = vec3d(1,0,0)
									y_axis = vec3d(0,1,0)
									z_axis = vec3d(0,0,1)
									if widget == "rot_x+" or widget == "rot_x-":
										if widget == "rot_x-": r_power = -float(r_power)
										r = mat3d(rot3d(x_axis,math.radians(float(r_power))))
										rot = r * cam_rot
										tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
									if widget == "rot_y+" or widget == "rot_y-":
										if widget == "rot_y-": r_power = -float(r_power)
										r = mat3d(rot3d(y_axis,math.radians(float(r_power))))
										rot = r * cam_rot
										tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
									if widget == "rot_z+" or widget == "rot_z-":
										if widget == "rot_z-": r_power = -float(r_power)
										r = mat3d(rot3d(z_axis,math.radians(float(r_power))))
										rot = r * cam_rot
										tde4.setPGroupRotation3D(pg,cam,frame,rot.list())
									tde4.filterPGroup(pg,cam)
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please enter correct frame range as you see in timeline or frame out value should be greater than frame in.","Ok")								
#camera local translation buttons nudge...
					if p_space == 2:
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							if loop_start != None and loop_end != None and (int(loop_start)-offset) >= 1 and (int(loop_start)-offset) <= frames and (int(loop_end)-offset) >= 1 and (int(loop_end)-offset) <= frames and (int(loop_start)-offset) <= (int(loop_end)-offset):
								for frame in range(int(loop_start)-offset,(int(loop_end)+1)-offset):
									cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									cam_rot = tde4.getPGroupRotation3D(pg,cam,frame)
									cam_rot = mat3d(cam_rot).trans()	
									x_axis = vec3d(cam_rot[0]).unit()
									y_axis = vec3d(cam_rot[1]).unit()
									z_axis = vec3d(cam_rot[2]).unit()
									if toggle_value == 0:
										power = tde4.getWidgetValue(self.req,"t_increment_factor")
									if toggle_value == 1:
										power = tde4.getWidgetValue(self.req,"t_increment_factor")
										power = float(power)/((int(loop_end) - int(loop_start)) + 1)												
									if widget == "pos_x+":
										v1 = x_axis * float(power)
										cam_pos = v1 + cam_pos
										tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
									if widget == "pos_x-":
										v1 = x_axis * float(power)
										cam_pos = cam_pos - v1
										tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
									if widget == "pos_y+":
										v1 = y_axis * float(power)
										cam_pos = v1 + cam_pos
										tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
									if widget == "pos_y-":
										v1 = y_axis * float(power)
										cam_pos = cam_pos - v1
										tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
									if widget == "pos_z+":
										v1 = z_axis * float(power)
										cam_pos = v1 + cam_pos
										tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
									if widget == "pos_z-":
										v1 = z_axis * float(power)
										cam_pos = cam_pos - v1
										tde4.setPGroupPosition3D(pg,cam,frame,cam_pos.list())
									tde4.filterPGroup(pg,cam)
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please enter correct frame range as you see in timeline or frame out value should be greater than frame in.","Ok")								
#camera local rotation nudge...
					if r_space == 2:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":
							if loop_start != None and loop_end != None and (int(loop_start)-offset) >= 1 and (int(loop_start)-offset) <= frames and (int(loop_end)-offset) >= 1 and (int(loop_end)-offset) <= frames and (int(loop_start)-offset) <= (int(loop_end)-offset):
								for frame in range(int(loop_start)-offset,(int(loop_end)+1)-offset):						
									pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
									rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
									x_axis = rot * vec3d(1,0,0)
									y_axis = rot * vec3d(0,1,0)
									z_axis = rot * vec3d(0,0,1)
									if toggle_value == 0:
										r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
									if toggle_value == 1:
										r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
										r_power = float(r_power)/((int(loop_end) - int(loop_start)) + 1)									
									if widget == "rot_x+" or widget == "rot_x-":
										if widget == "rot_x-": r_power = -float(r_power)
										r = mat3d(rot3d(x_axis,math.radians(float(r_power))))
										rot1 = r * rot
										tde4.setPGroupRotation3D(pg,cam,frame,rot1.list())
									if widget == "rot_y+" or widget == "rot_y-":
										if widget == "rot_y-": r_power = -float(r_power)
										r = mat3d(rot3d(y_axis,math.radians(float(r_power))))
										rot1 = r * rot
										tde4.setPGroupRotation3D(pg,cam,frame,rot1.list())
									if widget == "rot_z+" or widget == "rot_z-":
										if widget == "rot_z-": r_power = -float(r_power)
										r = mat3d(rot3d(z_axis,math.radians(float(r_power))))
										rot1 = r * rot
										tde4.setPGroupRotation3D(pg,cam,frame,rot1.list())
									tde4.filterPGroup(pg,cam)
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please enter correct frame range as you see in timeline or frame out value should be greater than frame in.","Ok")

#rotate camera around 3dpoint(changes camera pivot to selected 3dpoint)...
					if r_space == 3:
						if widget == "rot_x+" or widget == "rot_x-" or widget == "rot_y+" or widget == "rot_y-" or widget == "rot_z+" or widget == "rot_z-":						
							if loop_start != None and loop_end != None and (int(loop_start)-offset) >= 1 and (int(loop_start)-offset) <= frames and (int(loop_end)-offset) >= 1 and (int(loop_end)-offset) <= frames and (int(loop_start)-offset) <= (int(loop_end)-offset):
								pivot = tde4.getWidgetValue(self.req,"pivot_3dpoint")
								f = tde4.findPointByName(pg,pivot)
								if f != None:
									p3d = tde4.getPointCalcPosition3D(pg,f)
									for frame in range(int(loop_start)-offset,(int(loop_end)+1)-offset):
										#if 3dmodel exists delete that...	
										mlist = tde4.get3DModelList(pg,0)
										for m in mlist:
											if tde4.get3DModelName(pg,m) == "patcha":
												tde4.delete3DModel(pg,m)
										tde4.updateGUI()
										#create 3dmodel...
										model = tde4.create3DModel(pg, 2)
										tde4.set3DModelName(pg, model, "patcha")
										tde4.add3DModelVertex(pg, model, [0.0, 0.0, 0.0])
										tde4.add3DModelVertex(pg, model, [0.0, 5.0, 0.0])
										tde4.add3DModelLine(pg, model, [0, 1])
										#get wanted 3dmodel...
										mlist = tde4.get3DModelList(pg,0)
										for m1 in mlist:
											if tde4.get3DModelName(pg,m1) == "patcha":
												model = m1
												break
										#do constraint 3dmodel to camera...		
										mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
										mrot = tde4.get3DModelRotationScale3D(pg,model)
										campos = tde4.getPGroupPosition3D(pg,cam,frame)
										camrot = tde4.getPGroupRotation3D(pg,cam,frame)
										rot_matrix = mat3d(camrot)
										scale_matrix = mat3d(1,0,0,0,1,0,0,0,1)
										f = rot_matrix * scale_matrix
										tde4.set3DModelPosition3D(pg,model,campos)
										tde4.set3DModelRotationScale3D(pg,model,f.list())
										#update mpos and mrot
										mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
										mrot = tde4.get3DModelRotationScale3D(pg,model)
										#move 3dmodel pivot...
										vector = mat3d(mrot).invert() * (vec3d(p3d) - vec3d(mpos))
										vlist = tde4.get3DModelNoVertices(pg,model)
										for i in range(0,vlist):
											v = tde4.get3DModelVertex(pg,model,i,cam,frame)
											v[0] = v[0] - vector[0]
											v[1] = v[1] - vector[1]
											v[2] = v[2] - vector[2]
											tde4.set3DModelVertex(pg,model,i,v)
										tde4.set3DModelPosition3D(pg,model,p3d)
										#update mpos and mrot
										pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
										rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
										x_vec = vec3d(1,0,0)
										y_vec = vec3d(0,1,0)
										z_vec = vec3d(0,0,1)
										if toggle_value == 0:
											r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
										if toggle_value == 1:
											r_power = tde4.getWidgetValue(self.req,"r_increment_factor")
											r_power = float(r_power)/((int(loop_end) - int(loop_start)) + 1)										
										if widget == "rot_x+" or widget == "rot_x-":
											if widget == "rot_x-": r_power = -float(r_power)
											vector = x_vec
										if widget == "rot_y+" or widget == "rot_y-":
											if widget == "rot_y-": r_power = -float(r_power)
											vector = y_vec
										if widget == "rot_z+" or widget == "rot_z-":
											if widget == "rot_z-": r_power = -float(r_power)
											vector = z_vec
										#local rotate 3dmodel as per increment slider...
										r = mat3d(rot3d(vector,math.radians(float(r_power))))
										rot = rot * r
										tde4.set3DModelRotationScale3D(pg,model,rot.list())	
										#separate 3dmodel rotation to apply on camera...
										m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
										s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
										r_matrix = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
										mpos = tde4.get3DModelPosition3D(pg,model,cam,frame)
										mrot = tde4.get3DModelRotationScale3D(pg,model)
										#bake 3dmodel first vertex to global space...
										com_global = (mat3d(mrot)*vec3d(tde4.get3DModelVertex(pg,model,0,cam,frame))) + vec3d(mpos)
										tde4.setPGroupPosition3D(pg,cam,frame,com_global.list())
										tde4.setPGroupRotation3D(pg,cam,frame,r_matrix.list())
										tde4.filterPGroup(pg,cam)
										tde4.delete3DModel(pg,model)
								else:
									tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")	
							else:
								tde4.postQuestionRequester(self.window_title,"Error, please enter correct frame range as you see in timeline or frame out value should be greater than frame in.","Ok")																		
			else:
				tde4.postQuestionRequester(self.window_title,"Camera PGroup must be selected","OK")			
######################################################################################
#if object PGroup type selected...
		if s_type == 2:
			if pg_type == "OBJECT":
				if pg!= None:
					self.Bake_Buffer_Curves()
					if p_space == 2:
						obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
						obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
						newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), obj_pos.list(), 1.0, 0)
						pos = newvalues[1]
						rot = newvalues[0]
#object pgroup local translation nudge...
						if widget == "pos_x+" or widget == "pos_x-":
							if widget == "pos_x-": power = -float(power)
							pos_x = float(pos[0]) + float(power)
							tde4.setPGroupPosition3D(pg,cam,frame,[pos_x,pos[1],pos[2]])
						if widget == "pos_y+" or widget == "pos_y-":
							if widget == "pos_y-": power = -float(power)
							pos_y = float(pos[1]) + float(power)
							tde4.setPGroupPosition3D(pg,cam,frame,[pos[0],pos_y,pos[2]])
						if self.widget == "pos_z+" or widget == "pos_z-":
							if widget == "pos_z-": power = -float(power)
							pos_z = float(pos[2]) + float(power)
							tde4.setPGroupPosition3D(pg,cam,frame,[pos[0],pos[1],pos_z])
						tde4.filterPGroup(pg,cam)
#object local rotation nudge...
					if r_space == 2:
						obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
						obj_pos = tde4.getPGroupPosition3D(pg,cam,frame)
						if r_space == 2:
							xaxis = obj_rot * vec3d(1,0,0)
							yaxis = obj_rot * vec3d(0,1,0)
							zaxis = obj_rot * vec3d(0,0,1)
						if widget == "rot_x+" or widget == "rot_x-":
							if widget == "rot_x-": r_power = -float((r_power))
							r = mat3d(rot3d(xaxis,math.radians(float(r_power))))
							m1 = r * obj_rot
							newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m1.list(),obj_pos,1.0,0)
							pos = newvalues[1]
							rot = newvalues[0]
							tde4.setPGroupPosition3D(pg,cam,frame,pos)
							tde4.setPGroupRotation3D(pg,cam,frame,rot)
						if widget == "rot_y+" or widget == "rot_y-":
							if widget == "rot_y-": r_power = -float((r_power)) 
							r = mat3d(rot3d(yaxis,math.radians(float(r_power))))
							m1 = r * obj_rot
							newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m1.list(),obj_pos,1.0,0)
							pos = newvalues[1]
							rot = newvalues[0]
							tde4.setPGroupPosition3D(pg,cam,frame,pos)
							tde4.setPGroupRotation3D(pg,cam,frame,rot)
						if widget == "rot_z+" or widget == "rot_z-":
							if widget == "rot_z-": r_power = -float((r_power))
							r = mat3d(rot3d(zaxis,math.radians(float(r_power))))
							m1 = r * obj_rot
							newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m1.list(),obj_pos,1.0,0)
							pos = newvalues[1]
							rot = newvalues[0]
							tde4.setPGroupPosition3D(pg,cam,frame,pos)
							tde4.setPGroupRotation3D(pg,cam,frame,rot)
						tde4.filterPGroup(pg,cam)
#object pgroup global translation nudge...
					if p_space == 1:
						obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
						obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
						if widget == "pos_x+" or widget == "pos_x-":
							if widget == "pos_x-": power = -float(power)
							xaxis = obj_pos[0] + float(power)
							pos = vec3d(xaxis,obj_pos[1],obj_pos[2])
							newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,obj_rot.list(),pos.list(),1.0,0)
							tde4.setPGroupPosition3D(pg,cam,frame,newvalues[1])
						if widget == "pos_y+" or widget == "pos_y-":
							if widget == "pos_y-": power = -float(power)
							yaxis = obj_pos[1] + float(power)
							pos = vec3d(obj_pos[0],yaxis,obj_pos[2])
							newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,obj_rot.list(),pos.list(),1.0,0)
							tde4.setPGroupPosition3D(pg,cam,frame,newvalues[1])
						if widget == "pos_z+" or widget == "pos_z-":
							if widget == "pos_z-": power = -float(power)
							zaxis = obj_pos[2] + float(power)
							pos = vec3d(obj_pos[0],obj_pos[1],zaxis)
							newvalues = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,obj_rot.list(),pos.list(),1.0,0)
							tde4.setPGroupPosition3D(pg,cam,frame,newvalues[1])
						tde4.filterPGroup(pg,cam)
#object pgroup global rotation nudge...
					if r_space == 1:
						obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
						obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
						if widget == "rot_x+" or widget == "rot_x-":
							if widget == "rot_x-": r_power = -float(r_power)
							r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
							m = r * obj_rot
							n = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m.list(),obj_pos.list(),1.0,0)
							tde4.setPGroupPosition3D(pg,cam,frame,n[1])
							tde4.setPGroupRotation3D(pg,cam,frame,n[0])
						if widget == "rot_y+" or widget == "rot_y-":
							if widget == "rot_y-": r_power = -float(r_power)
							r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
							m = r * obj_rot
							n = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m.list(),obj_pos.list(),1.0,0)
							tde4.setPGroupPosition3D(pg,cam,frame,n[1])
							tde4.setPGroupRotation3D(pg,cam,frame,n[0])
						if widget == "rot_z+" or widget == "rot_z-":
							if widget == "rot_z-": r_power = -float(r_power)
							r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
							m = r * obj_rot
							n = tde4.convertObjectPGroupTransformationWorldTo3DE(cam,frame,m.list(),obj_pos.list(),1.0,0)
							tde4.setPGroupPosition3D(pg,cam,frame,n[1])
							tde4.setPGroupRotation3D(pg,cam,frame,n[0])
						tde4.filterPGroup(pg,cam)
#object pgroup screen translation nudge...
					if p_space == 3:						
						cam	= tde4.getCurrentCamera()
						pg	= tde4.getCurrentPGroup()
						frame = tde4.getCurrentFrame(cam)
						pgl = tde4.getPGroupList(0)
						for campg in pgl:
							if tde4.getPGroupType(campg) == "CAMERA":
								break
						cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
						cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
						obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
						obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
						cam_rot = mat3d(cam_rot).trans()	
						d = vec3d(obj_pos) - vec3d(cam_pos)
						x_axis = vec3d(cam_rot[0]).unit()
						y_axis = vec3d(cam_rot[1]).unit()
						z_axis = vec3d(cam_rot[2]).unit()
						if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
							if float(power) <= 0.1:
								if widget == "pos_x+" or widget == "pos_x-":
									if widget == "pos_x-": power = -float(power)
									x_axis = x_axis * float(power)
									x_axis = x_axis + cam_pos + d
									f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), x_axis.list(), 1.0, 0)
									tde4.setPGroupPosition3D(pg,cam,frame,f[1])
								if widget == "pos_y+" or widget == "pos_y-":
									if widget == "pos_y-": power = -float(power)
									y_axis = y_axis * float(power)
									y_axis = y_axis + cam_pos + d
									f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), y_axis.list(), 1.0, 0)
									tde4.setPGroupPosition3D(pg,cam,frame,f[1])
								#aim math for screen Z...							
								if widget == "pos_z+" or widget == "pos_z-":
									if widget == "pos_z-": power = -float(power)
									p1	= cam_pos+((obj_pos-cam_pos)*(1.0+float(power)))
									f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, obj_rot.list(), p1.list(), 1.0, 0)
									tde4.setPGroupPosition3D(pg,cam,frame,f[1])
								tde4.filterPGroup(pg,cam)
							else:
								tde4.postQuestionRequester(self.window_title,"Error, screen translation nudge maximum value is 0.1","Ok")
								tde4.setWidgetValue(self.req,"t_increment_factor","0.05")
								tde4.setWidgetValue(self.req,"t_increment","0.05")
								tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)
#object pgroup screen rotation nudge...
					if r_space == 3:
						pgl = tde4.getPGroupList(0)
						for campg in pgl:
							if tde4.getPGroupType(campg) == "CAMERA":
								break
						cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
						cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
						obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
						obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
						x_axis = cam_rot * vec3d(1,0,0)
						y_axis = cam_rot * vec3d(0,1,0)
						z_axis = cam_rot * vec3d(0,0,1)
						if widget == "rot_x+" or widget == "rot_x-":
							if widget == "rot_x-": r_power = -float((r_power))						
							r1 = mat3d(rot3d(x_axis,math.radians(float(r_power))))
							r = r1 * mat3d(obj_rot)
							f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, r.list(), obj_pos.list(), 1.0, 0)
						if widget == "rot_y+" or widget == "rot_y-":
							if widget == "rot_y-": r_power = -float((r_power))						
							r1 = mat3d(rot3d(y_axis,math.radians(float(r_power))))
							r = r1 * mat3d(obj_rot)
							f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, r.list(), obj_pos.list(), 1.0, 0)
						if widget == "rot_z+" or widget == "rot_z-":
							if widget == "rot_z-": r_power = -float((r_power))						
							r1 = mat3d(rot3d(z_axis,math.radians(float(r_power))))
							r = r1 * mat3d(obj_rot)
							f = tde4.convertObjectPGroupTransformationWorldTo3DE(cam, frame, r.list(), obj_pos.list(), 1.0, 0)
						tde4.setPGroupPosition3D(pg,cam,frame,f[1])
						tde4.setPGroupRotation3D(pg,cam,frame,f[0])
						tde4.filterPGroup(pg,cam)

#rotate objectPGroup around 3dpoint(changes objectPGroup pivot to selected 3dpoint)...
					if r_space == 4:
						pivot = tde4.getWidgetValue(self.req,"pivot_3dpoint")
						f = tde4.findPointByName(pg,pivot)
						if f != None:
							p3d = tde4.getPointCalcPosition3D(pg,f)
							pivot_local = vec3d(p3d[0],p3d[1],p3d[2])
							# Find camera point group
							for i_pg in tde4.getPGroupList():
								if tde4.getPGroupType(i_pg) == "CAMERA":
									id_cpg = i_pg
									break
							# We pick the first object point group. Please modify according to your requirements.
							for i_pg in tde4.getPGroupList():
								if tde4.getPGroupType(i_pg) == "OBJECT":
									id_opg = i_pg
									break
							# Current camera
							id_cam = tde4.getCurrentCamera()
							# Current rotation and position of the object point group.
							pos_opg_global = vec3d(tde4.getPGroupPosition3D(id_opg,id_cam,frame))
							rot_opg_global = mat3d(tde4.getPGroupRotation3D(id_opg,id_cam,frame))
							pivot_global = (mat3d(rot_opg_global)*vec3d(pivot_local)) + vec3d(pos_opg_global)

							# Feel free to try out some of the following three segments.
							# 1. This will just do nothing.
							#	rot_opg_new_global = rot_opg_global
							#	pos_opg_new_global = pos_opg_global

							# 2. This will translate the entire point group to the left by fifty units.
							#	rot_opg_new_global = rot_opg_global
							#	pos_opg_new_global = vl.igl3d(vl.mat3d(1),vl.vec3d(-50,0,0)) * pos_opg_global
								
							# 3. This one rotates the entire point group and its path
							# around the given pivot in global coords by the given global matrix.
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float((r_power))
								delta_rot_global = rot3d(vec3d(1,0,0),math.radians(float(r_power))).mat()
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float((r_power))
								delta_rot_global = rot3d(vec3d(0,1,0),math.radians(float(r_power))).mat()
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float((r_power))
								delta_rot_global = rot3d(vec3d(0,0,1),math.radians(float(r_power))).mat()
							rot_opg_new_global = delta_rot_global * rot_opg_global
							pos_opg_new_global = igl3d(mat3d(1),pivot_global) * igl3d(delta_rot_global) * igl3d(mat3d(1),-pivot_global) * pos_opg_global
							# The base transform from the camera point group.
							# We need rot_pos_base because unfortunately our set-functions
							# are not the exact counterpart to the get-functions. It's well-defined, but unpleasent.
							rot_cpg = mat3d(tde4.getPGroupRotation3D(id_cpg,id_cam,frame))
							pos_cpg = vec3d(tde4.getPGroupPosition3D(id_cpg,id_cam,frame))
							rot_pos_base = igl3d(rot_cpg,pos_cpg)
							# Now we can build rotation and position of the object point group.
							rot_pos_opg_new = igl3d(rot_opg_new_global,pos_opg_new_global).invert() * rot_pos_base
							tde4.setPGroupRotation3D(id_opg,id_cam,frame,rot_pos_opg_new.m.list())
							tde4.setPGroupPosition3D(id_opg,id_cam,frame,rot_pos_opg_new.v.list())
							tde4.filterPGroup(i_pg,id_cam)
						else:
							tde4.postQuestionRequester(self.window_title,"Error, please pick pivot 3dpoint.","Ok")
			else:
				tde4.postQuestionRequester(self.window_title,"Object PGroup must be selected","OK")	
##########################################################################################
#if 3D Model type selected under camera group... 	
		if s_type == 3:
			if len(mlist) > 0:
				for model in mlist:
					tde4.set3DModelSurveyFlag(pg,model,0)
					if tde4.getPGroupType(pg) == "CAMERA":
						if p_space == 1:
							pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
#3D model global translation nudge...
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								pos_x = float(pos[0]) + float(power)
								tde4.set3DModelPosition3D(pg,model,[pos_x,pos[1],pos[2]])
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								pos_y = float(pos[1]) + float(power)
								tde4.set3DModelPosition3D(pg,model,[pos[0],pos_y,pos[2]])	
							if widget == "pos_z+" or widget == "pos_z-":
								if widget == "pos_z-": power = -float(power)
								pos_z = float(pos[2]) + float(power)
								tde4.set3DModelPosition3D(pg,model,[pos[0],pos[1],pos_z])			
#3D model global rotation nudge...
						if r_space == 1:
							rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
								rot = r * rot
								tde4.set3DModelRotationScale3D(pg,model,rot.list())							
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
								rot = r * rot
								tde4.set3DModelRotationScale3D(pg,model,rot.list())								
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
								rot = r * rot
								tde4.set3DModelRotationScale3D(pg,model,rot.list())								
#3D model local translation buttons nudge...
						if p_space == 2:
							pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
							rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
							rot1 = mat3d(rot).trans()
							x_axis = vec3d(rot1[0]).unit()
							y_axis = vec3d(rot1[1]).unit()
							z_axis = vec3d(rot1[2]).unit()
							if widget == "pos_x+":
								v = x_axis * float(power)
								pos = vec3d(v) + vec3d(pos)
								tde4.set3DModelPosition3D(pg,model,pos.list())
							if widget == "pos_x-":
								v = x_axis * float(power)
								pos = vec3d(pos) - vec3d(v) 
								tde4.set3DModelPosition3D(pg,model,pos.list())
							if widget == "pos_y+":
								v = y_axis * float(power)
								pos = vec3d(v) + vec3d(pos)
								tde4.set3DModelPosition3D(pg,model,pos.list())
							if widget == "pos_y-":
								v = y_axis * float(power)
								pos = vec3d(pos) - vec3d(v)
								tde4.set3DModelPosition3D(pg,model,pos.list()) 
							if widget == "pos_z+":
								v = z_axis * float(power)
								pos = vec3d(v) + vec3d(pos)
								tde4.set3DModelPosition3D(pg,model,pos.list())
							if widget == "pos_z-":
								v = z_axis * float(power)
								pos = vec3d(pos) - vec3d(v) 
								tde4.set3DModelPosition3D(pg,model,pos.list())
#3D model local rotation nudge...
						if r_space == 2:
							rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
								rot = rot * r
								tde4.set3DModelRotationScale3D(pg,model,rot.list())							
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
								rot = rot * r
								tde4.set3DModelRotationScale3D(pg,model,rot.list())								
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
								rot = rot * r
								tde4.set3DModelRotationScale3D(pg,model,rot.list())								
#3D model screen translate nudge...		
						if p_space == 3:
							cam_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							cam_rot = tde4.getPGroupRotation3D(pg,cam,frame)
							cam_rot = mat3d(cam_rot).trans()	
							m_pos = tde4.get3DModelPosition3D(pg,mlist[0],cam,frame)
							d = vec3d(m_pos) - vec3d(cam_pos)
							x_axis = vec3d(cam_rot[0]).unit()
							y_axis = vec3d(cam_rot[1]).unit()
							z_axis = vec3d(cam_rot[2]).unit()
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":
								if float(power) <= 0.1: 
									if widget == "pos_x+" or widget == "pos_x-":
										if widget == "pos_x-": power = -float(power)
										x_axis = x_axis * float(power)
										x_axis = x_axis + cam_pos + d
										tde4.set3DModelPosition3D(pg,mlist[0],x_axis.list())
									if widget == "pos_y+" or widget == "pos_y-":
										if widget == "pos_y-": power = -float(power)
										y_axis = y_axis * float(power)
										y_axis = y_axis + cam_pos + d
										tde4.set3DModelPosition3D(pg,mlist[0],y_axis.list())
									m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
									s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
									r3d = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
									#aim math for screen Z mode...							
									if widget == "pos_z+" or widget == "pos_z-":
										if widget == "pos_z-": power = -float(power)
										l	= r3d*vec3d(0.0,0.0,1.0)
										p0 = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
										p1	= cam_pos+((p0-cam_pos)) * (1.0+float(power))
										tde4.set3DModelPosition3D(pg,model,p1.list())
								else:
									tde4.postQuestionRequester(self.window_title,"Error, screen translation nudge maximum value is 0.1","Ok")
									tde4.setWidgetValue(self.req,"t_increment_factor","0.05")
									tde4.setWidgetValue(self.req,"t_increment","0.05")
									tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)								
#3D model screen rotation nudge...	
						if r_space == 3:
							pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							x_axis = rot * vec3d(1,0,0)
							y_axis = rot * vec3d(0,1,0)
							z_axis = rot * vec3d(0,0,1)
							m = mat3d(tde4.get3DModelRotationScale3D(pg,mlist[0])).trans()
							s = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
							s = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
							r = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r1 = mat3d(rot3d(x_axis,math.radians(float(r_power))))
								r = r1 * r
								r = r *s
								tde4.set3DModelRotationScale3D(pg,mlist[0],r.list())
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r1 = mat3d(rot3d(y_axis,math.radians(float(r_power))))
								r = r1 * r
								r = r *s
								tde4.set3DModelRotationScale3D(pg,mlist[0],r.list())
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r1 = mat3d(rot3d(z_axis,math.radians(float(r_power))))
								r = r1 * r
								r = r *s
								tde4.set3DModelRotationScale3D(pg,mlist[0],r.list())
#if 3D Model type selected under object group... 	
					if tde4.getPGroupType(pg) == "OBJECT":
#3D model global translation nudge...
						if p_space == 1:
							rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							xaxis = rot.invert()*vec3d(1,0,0)
							yaxis = rot.invert()*vec3d(0,1,0)
							zaxis = rot.invert()*vec3d(0,0,1)
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								xaxis = xaxis*float(power)
								xaxis = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame)) + vec3d(xaxis)
								tde4.set3DModelPosition3D(pg,model,[xaxis[0],xaxis[1],xaxis[2]])
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								yaxis = yaxis*float(power)
								yaxis = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame)) + vec3d(yaxis)
								tde4.set3DModelPosition3D(pg,model,[yaxis[0],yaxis[1],yaxis[2]])
							if widget == "pos_z+" or widget == "pos_z-":
								if widget == "pos_z-": power = -float(power)
								zaxis = zaxis*float(power)
								zaxis = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame)) + vec3d(zaxis)
								tde4.set3DModelPosition3D(pg,model,[zaxis[0],zaxis[1],zaxis[2]])
#3D model local translation nudge...
						if p_space == 2:
							pos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
							rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
							rot1 = mat3d(rot).trans()
							x_axis = vec3d(rot1[0]).unit()
							y_axis = vec3d(rot1[1]).unit()
							z_axis = vec3d(rot1[2]).unit()
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								v = x_axis * float(power)
								pos = vec3d(v) + vec3d(pos)
								tde4.set3DModelPosition3D(pg,model,pos.list())
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								v = y_axis * float(power)
								pos = vec3d(v) + vec3d(pos)
								tde4.set3DModelPosition3D(pg,model,pos.list())
							if widget == "pos_z+" or widget == "pos_z-":
								if widget == "pos_z-": power = -float(power)
								v = z_axis * float(power)
								pos = vec3d(v) + vec3d(pos)
								tde4.set3DModelPosition3D(pg,model,pos.list())
#3D model global rotation nudge...
						if r_space == 1:
							rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							xaxis = (rot.invert()*vec3d(1,0,0))
							yaxis = (rot.invert()*vec3d(0,1,0))
							zaxis = (rot.invert()*vec3d(0,0,1))
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r = mat3d(rot3d(xaxis,math.radians(float(r_power))))
								f = r * mat3d(tde4.get3DModelRotationScale3D(pg,model))
								tde4.set3DModelRotationScale3D(pg,model,f.list())
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r = mat3d(rot3d(yaxis,math.radians(float(r_power))))
								f = r * mat3d(tde4.get3DModelRotationScale3D(pg,model))
								tde4.set3DModelRotationScale3D(pg,model,f.list())
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r = mat3d(rot3d(zaxis,math.radians(float(r_power))))
								f = r * mat3d(tde4.get3DModelRotationScale3D(pg,model))
								tde4.set3DModelRotationScale3D(pg,model,f.list())
#3D model local rotation nudge...
						if r_space == 2:
							rot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(1,0,0),math.radians(float(r_power))))
								rot = rot *r
								tde4.set3DModelRotationScale3D(pg,model,rot.list())							
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,1,0),math.radians(float(r_power))))
								rot = rot *r
								tde4.set3DModelRotationScale3D(pg,model,rot.list())	
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float(r_power)
								r = mat3d(rot3d(vec(0,0,1),math.radians(float(r_power))))
								rot = rot *r
								tde4.set3DModelRotationScale3D(pg,model,rot.list())	
#3D model screen translate nudge...	
						if p_space == 3:						
							cam	= tde4.getCurrentCamera()
							pg	= tde4.getCurrentPGroup()
							frame = tde4.getCurrentFrame(cam)
							pgl = tde4.getPGroupList(0)
							for campg in pgl:
								if tde4.getPGroupType(campg) == "CAMERA":
									break
							mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
							cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
							cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
							obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
							#convert 3DModel local to global...
							mpos = (mat3d(obj_rot)*vec3d(mpos)) + vec3d(obj_pos)
							vector = vec3d(mpos) - vec3d(obj_pos)
							cam_rot = mat3d(cam_rot).trans()	
							d = vec3d(obj_pos) - vec3d(cam_pos)
							x_axis = vec3d(cam_rot[0]).unit()
							y_axis = vec3d(cam_rot[1]).unit()
							z_axis = vec3d(cam_rot[2]).unit()
							if widget == "pos_x+" or widget == "pos_x-":
								if widget == "pos_x-": power = -float(power)
								x_axis = x_axis * float(power)
								x_axis = x_axis + cam_pos + d
								x_axis = vec3d(x_axis) + vec3d(vector)
								#convert 3DModel global to local...
								mpos = mat3d(obj_rot).invert() * (vec3d(x_axis)-vec3d(obj_pos))
								tde4.set3DModelPosition3D(pg,model,mpos.list())
							if widget == "pos_y+" or widget == "pos_y-":
								if widget == "pos_y-": power = -float(power)
								y_axis = y_axis * float(power)
								y_axis = y_axis + cam_pos + d
								y_axis = vec3d(y_axis) + vec3d(vector)
								#convert 3DModel global to local...
								mpos = mat3d(obj_rot).invert() * (vec3d(y_axis)-vec3d(obj_pos))
								tde4.set3DModelPosition3D(pg,model,mpos.list())
							#aim math for screen Z...
							if widget == "pos_x+" or widget == "pos_x-" or widget == "pos_y+" or widget == "pos_y-" or widget == "pos_z+" or widget == "pos_z-":							
								if float(power) <= 0.1: 
									if widget == "pos_z+" or widget == "pos_z-":
										if widget == "pos_z-": power = -float(power)
										pg = tde4.getCurrentPGroup()
										cam = tde4.getCurrentCamera()
										frame = tde4.getCurrentFrame(cam)
										pgl	= tde4.getPGroupList(0)
										for campg in pgl:
											pgt	= tde4.getPGroupType(campg)
											if pgt=="CAMERA": break
										cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
										cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
										obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
										obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))
										p3d = obj_rot.trans()*(cam_pos-obj_pos)
										p0 = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
										p1 = p3d+((p0-p3d)*(1.0+float(power)))
										tde4.set3DModelPosition3D(pg,model,[p1[0],p1[1],p1[2]])
								else:
									tde4.postQuestionRequester(self.window_title,"Error, screen translation nudge maximum value is 0.1","Ok")
									tde4.setWidgetValue(self.req,"t_increment_factor","0.05")
									tde4.setWidgetValue(self.req,"t_increment","0.05")
									tde4.setWidgetSensitiveFlag(self.req,"t_increment",1)
#3D model screen rotation nudge...	
						if r_space == 3:
							pgl = tde4.getPGroupList(0)
							for campg in pgl:
								if tde4.getPGroupType(campg) == "CAMERA":
									break
							mpos = vec3d(tde4.get3DModelPosition3D(pg,model,cam,frame))
							cam_pos = vec3d(tde4.getPGroupPosition3D(campg,cam,frame))
							cam_rot = mat3d(tde4.getPGroupRotation3D(campg,cam,frame))
							obj_pos = vec3d(tde4.getPGroupPosition3D(pg,cam,frame))
							obj_rot = mat3d(tde4.getPGroupRotation3D(pg,cam,frame))	
							#convert 3DModel local to global...
							mpos = (mat3d(obj_rot)*vec3d(mpos)) + vec3d(obj_pos)	
							mrot = mat3d(tde4.get3DModelRotationScale3D(pg,model))
							mrot = mat3d(obj_rot) * mat3d(mrot)
							#extract 3DModel rot and scale matrices...
							m = mat3d(mrot).trans()
							s        = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
							scale_matrix = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
							r = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
							x_axis = cam_rot * vec3d(1,0,0)
							y_axis = cam_rot * vec3d(0,1,0)
							z_axis = cam_rot * vec3d(0,0,1)
							if widget == "rot_x+" or widget == "rot_x-":
								if widget == "rot_x-": r_power = -float((r_power))						
								r1 = mat3d(rot3d(x_axis,math.radians(float(r_power))))
								r = r1 * r
								r = r*scale_matrix
								#convert global rotations to local...
								f = mat3d(obj_rot).invert()*mat3d(r)
								tde4.set3DModelRotationScale3D(pg,model,f.list())
							if widget == "rot_y+" or widget == "rot_y-":
								if widget == "rot_y-": r_power = -float((r_power))						
								r1 = mat3d(rot3d(y_axis,math.radians(float(r_power))))
								r = r1 * r
								r = r*scale_matrix
								#convert global rotations to local...
								f = mat3d(obj_rot).invert()*mat3d(r)
								tde4.set3DModelRotationScale3D(pg,model,f.list())
							if widget == "rot_z+" or widget == "rot_z-":
								if widget == "rot_z-": r_power = -float((r_power))						
								r1 = mat3d(rot3d(z_axis,math.radians(float(r_power))))
								r = r1 * r
								r = r*scale_matrix
								#convert global rotations to local...
								f = mat3d(obj_rot).invert()*mat3d(r)
								tde4.set3DModelRotationScale3D(pg,model,f.list())
#3d model scale...
					m = mat3d(tde4.get3DModelRotationScale3D(pg,model)).trans()
					s        = vec3d(m[0].norm2(),m[1].norm2(),m[2].norm2())
					r_matrix        = mat3d(m[0].unit(),m[1].unit(),m[2].unit()).trans()
					if widget == "scale_x+" or widget == "scale_x-":
						if widget == "scale_x-": s_power = -float(s_power)
						s_matrix = mat3d(s[0]+float(s_power),0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2])
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "scale_y+" or widget == "scale_y-":
						if widget == "scale_y-": s_power = -float(s_power)
						s_matrix = mat3d(s[0],0.0,0.0,0.0,s[1]+float(s_power),0.0,0.0,0.0,s[2])
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "scale_z+" or widget == "scale_z-":
						if widget == "scale_z-": s_power = -float(s_power)
						s_matrix = mat3d(s[0],0.0,0.0,0.0,s[1],0.0,0.0,0.0,s[2]+float(s_power))
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "uniform_scale+":
						s_matrix = mat3d(s[0]+float(s_power),0.0,0.0,0.0,s[1]+float(s_power),0.0,0.0,0.0,s[2]+float(s_power))
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
					if widget == "uniform_scale-":
						if float(s_power) >= s[0]-0.1 or float(s_power) >= s[1]-0.1 or float(s_power) >= s[2]-0.1:
							s_power = float((s[0]+s[1]+s[2])/3)/10.0
							tde4.setWidgetValue(self.req,"s_increment",str(s_power))
							tde4.setWidgetValue(self.req,"s_increment_factor",str(s_power))
						if s[0] <= 0.2 or s[1] <= 0.2 or s[2] <= 0.2:
							tde4.setWidgetValue(self.req,"s_increment","0.001")
							tde4.setWidgetValue(self.req,"s_increment_factor","0.001")
							s_power = tde4.getWidgetValue(self.req,"s_increment_factor")
						s_matrix = mat3d(s[0]-float(s_power),0.0,0.0,0.0,s[1]-float(s_power),0.0,0.0,0.0,s[2]-float(s_power))
						m = r_matrix * s_matrix
						tde4.set3DModelRotationScale3D(pg,model,m.list())
			else:
				tde4.postQuestionRequester(self.window_title,"atleast one 3DModel must be selected or 3DModels should be under current PGroup.","OK")	
			
				
##################################################################################################3
#build GUI....
	def GUI(self):
		self.window_title = "Patcha Nudge3D Tool v1.0b2.99"
		self.req = tde4.createCustomRequester()
#type widget...
		tde4.addOptionMenuWidget(self.req,"selected_menu","Selected Type","Camera","Object PGroup","3D Model")
#sep1 widget...
		tde4.addSeparatorWidget(self.req,"sep1")
		tde4.setWidgetAttachModes(self.req,"sep1","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep1",2,98,25,0)	
#translation menubar widget...
		tde4.addMenuBarWidget(self.req,"t_menu_bar")
		tde4.setWidgetAttachModes(self.req,"t_menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"t_menu_bar",0,100,45,0)
		tde4.addMenuWidget(self.req,"t_nudge","Translation Nudge","t_menu_bar",0)
#translation button widgets...
		tde4.addButtonWidget(self.req,"pos_x+","Pos +X",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_x+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_x+",10,30,70,0)		
		tde4.addButtonWidget(self.req,"pos_y+","Pos +Y",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_y+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_y+",40,60,70,0)			
		tde4.addButtonWidget(self.req,"pos_z+","Pos +Z",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_z+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_z+",70,90,70,0)			
		tde4.addButtonWidget(self.req,"pos_x-","Pos -X",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_x-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_x-",10,30,100,0)		
		tde4.addButtonWidget(self.req,"pos_y-","Pos -Y",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_y-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_y-",40,60,100,0)			
		tde4.addButtonWidget(self.req,"pos_z-","Pos -Z",70,10)
		tde4.setWidgetAttachModes(self.req,"pos_z-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pos_z-",70,90,100,0)	
#translation pivot widgets...
		tde4.addOptionMenuWidget(self.req,"t_space","Pivot Space","Global","Local/Screen")
		tde4.addScaleWidget(self.req,"t_increment"," ","DOUBLE",0.001,0.1,0.05)
		tde4.setWidgetAttachModes(self.req,"t_increment","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"t_increment",5,75,153,0)	
		tde4.addTextFieldWidget(self.req,"t_increment_factor"," ","0.05")
		tde4.setWidgetAttachModes(self.req,"t_increment_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"t_increment_factor",78,98,153,0)
#rotation menubar widget...
		tde4.addMenuBarWidget(self.req,"r_menu_bar")
		tde4.setWidgetAttachModes(self.req,"r_menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"r_menu_bar",0,100,180,0)
		tde4.addMenuWidget(self.req,"r_nudge","Rotation Nudge","r_menu_bar",0)		
#rotation button widgets...
		tde4.addButtonWidget(self.req,"rot_x+","Rot +X",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_x+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_x+",10,30,205,0)
		tde4.addButtonWidget(self.req,"rot_y+","Rot +Y",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_y+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_y+",40,60,205,0)		
		tde4.addButtonWidget(self.req,"rot_z+","Rot +Z",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_z+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_z+",70,90,205,0)		
		tde4.addButtonWidget(self.req,"rot_x-","Rot -X",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_x-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_x-",10,30,235,0)		
		tde4.addButtonWidget(self.req,"rot_y-","Rot -Y",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_y-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_y-",40,60,235,0)			
		tde4.addButtonWidget(self.req,"rot_z-","Rot -Z",70,10)
		tde4.setWidgetAttachModes(self.req,"rot_z-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"rot_z-",70,90,235,0)	
#rotation pivot widgets...
		tde4.addOptionMenuWidget(self.req,"r_space","Pivot Space","Global","Local/Screen","Around 3DPoints")
		tde4.addScaleWidget(self.req,"r_increment"," ","DOUBLE",0.001,0.1,0.05)
		tde4.setWidgetAttachModes(self.req,"r_increment","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"r_increment",5,75,288,0)
		tde4.addTextFieldWidget(self.req,"r_increment_factor"," ","0.05")
		tde4.setWidgetAttachModes(self.req,"r_increment_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"r_increment_factor",78,98,288,0)
#scale menubar widget...
		tde4.addMenuBarWidget(self.req,"s_menu_bar")
		tde4.setWidgetAttachModes(self.req,"s_menu_bar","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"s_menu_bar",0,100,315,0)
		tde4.addMenuWidget(self.req,"s_nudge","Scale Nudge","s_menu_bar",0)	
#scale button widgets...
		tde4.addButtonWidget(self.req,"scale_x+","Scale +X",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_x+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_x+",10,30,340,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_x+",0)		
		tde4.addButtonWidget(self.req,"scale_y+","Scale +Y",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_y+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_y+",40,60,340,0)	
		tde4.setWidgetSensitiveFlag(self.req,"scale_y+",0)			
		tde4.addButtonWidget(self.req,"scale_z+","Scale +Z",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_z+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_z+",70,90,340,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_z+",0)				
		tde4.addButtonWidget(self.req,"scale_x-","Scale -X",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_x-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_x-",10,30,370,0)	
		tde4.setWidgetSensitiveFlag(self.req,"scale_x-",0)		
		tde4.addButtonWidget(self.req,"scale_y-","Scale -Y",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_y-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_y-",40,60,370,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_y-",0)				
		tde4.addButtonWidget(self.req,"scale_z-","Scale -Z",70,10)
		tde4.setWidgetAttachModes(self.req,"scale_z-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"scale_z-",70,90,370,0)
		tde4.setWidgetSensitiveFlag(self.req,"scale_z-",0)	
		tde4.addButtonWidget(self.req,"uniform_scale-","Uniform Scale -",70,10)
		tde4.setWidgetAttachModes(self.req,"uniform_scale-","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"uniform_scale-",10,45,395,0)
		tde4.setWidgetSensitiveFlag(self.req,"uniform_scale-",0)		
		tde4.addButtonWidget(self.req,"uniform_scale+","Uniform Scale +",70,10)
		tde4.setWidgetAttachModes(self.req,"uniform_scale+","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"uniform_scale+",55,90,395,0)	
		tde4.setWidgetSensitiveFlag(self.req,"uniform_scale+",0)
		tde4.addScaleWidget(self.req,"s_increment"," ","DOUBLE",0.001,1.0,0.5)
		tde4.setWidgetAttachModes(self.req,"s_increment","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"s_increment",5,75,423,0)
		tde4.setWidgetSensitiveFlag(self.req,"s_increment",0)
		tde4.addTextFieldWidget(self.req,"s_increment_factor"," ","0.5")
		tde4.setWidgetAttachModes(self.req,"s_increment_factor","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"s_increment_factor",78,98,423,0)
		tde4.setWidgetSensitiveFlag(self.req,"s_increment_factor",0)
#sep2 widget...
		tde4.addSeparatorWidget(self.req,"sep2")
		tde4.setWidgetAttachModes(self.req,"sep2","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep2",2,98,440,0)		
#look through camera text field widget...
		tde4.addTextFieldWidget(self.req,"look","look thru camera"," ")
		tde4.setWidgetAttachModes(self.req,"look","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"look",37,98,457,0)
		tde4.setWidgetSensitiveFlag(self.req,"look",0)
#selected text field widget...
		tde4.addTextFieldWidget(self.req,"sel","effected"," ")
		tde4.setWidgetAttachModes(self.req,"sel","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sel",20,98,487,0)
		tde4.setWidgetValue(self.req,"sel",str(tde4.getCameraName(tde4.getCurrentCamera())))
		tde4.setWidgetSensitiveFlag(self.req,"sel",0)
#pivot on 3dpoint...
		tde4.addTextFieldWidget(self.req,"pivot_3dpoint","Pivot on 3DPoints"," ")
		tde4.setWidgetAttachModes(self.req,"pivot_3dpoint","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pivot_3dpoint",38,98,517,0)
		tde4.setWidgetSensitiveFlag(self.req,"pivot_3dpoint",0)
#pick pivot point button...
		tde4.addButtonWidget(self.req,"pick_pivot","Pick Pivot 3dpoint",70,10)
		tde4.setWidgetAttachModes(self.req,"pick_pivot","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"pick_pivot",5,45,545,0)	
#average 3dpoint button...
		tde4.addButtonWidget(self.req,"avg_3dpoint","Create average 3dpoint",70,10)
		tde4.setWidgetAttachModes(self.req,"avg_3dpoint","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"avg_3dpoint",50,95,545,0)
#add sep3 widget...
		tde4.addSeparatorWidget(self.req,"sep3")
		tde4.setWidgetAttachModes(self.req,"sep3","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"sep3",2,98,562,0)
#frame in widget...
		tde4.addTextFieldWidget(self.req,"frame_in","Frame in")
		tde4.setWidgetAttachModes(self.req,"frame_in","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"frame_in",20,45,580,0)	
		tde4.setWidgetSensitiveFlag(self.req,"frame_in",0)			
#frame out widget...
		tde4.addTextFieldWidget(self.req,"frame_out","Frame out")
		tde4.setWidgetAttachModes(self.req,"frame_out","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"frame_out",70,97,580,0)
		tde4.setWidgetSensitiveFlag(self.req,"frame_out",0)
#enable frame range widget...
		tde4.addToggleWidget(self.req,"toggle","enable frame range")
		tde4.setWidgetAttachModes(self.req,"toggle","ATTACH_POSITION","ATTACH_POSITION","ATTACH_WINDOW","ATTACH_AS_IS")
		tde4.setWidgetOffsets(self.req,"toggle",65,71,605,0)		

#widget callbacks...
		tde4.setWidgetCallbackFunction(self.req,"pos_x+","do.Nudge_Callback")				
		tde4.setWidgetCallbackFunction(self.req,"pos_x-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_y+","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_y-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_z+","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"pos_z-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_x+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_x-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_y+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_y-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_z+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"rot_z-","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_x+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_x-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"scale_y+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_y-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"scale_z+","do.Nudge_Callback")	
		tde4.setWidgetCallbackFunction(self.req,"scale_z-","do.Nudge_Callback")			
		tde4.setWidgetCallbackFunction(self.req,"uniform_scale+","do.Nudge_Callback")		
		tde4.setWidgetCallbackFunction(self.req,"uniform_scale-","do.Nudge_Callback")	
#increment widgets callbacks...
		tde4.setWidgetCallbackFunction(self.req,"t_increment","do.Increment_Sensitive")
		tde4.setWidgetCallbackFunction(self.req,"t_increment_factor","do.Increment_Sensitive")
		tde4.setWidgetCallbackFunction(self.req,"r_increment","do.Increment_Sensitive")	
		tde4.setWidgetCallbackFunction(self.req,"r_increment_factor","do.Increment_Sensitive")
		tde4.setWidgetCallbackFunction(self.req,"s_increment","do.Increment_Sensitive")	
		tde4.setWidgetCallbackFunction(self.req,"s_increment_factor","do.Increment_Sensitive")	
#pivot menu callback...
		tde4.setWidgetCallbackFunction(self.req,"selected_menu","do.Pivot_Menu_Edit")
		tde4.setWidgetCallbackFunction(self.req,"t_space","do.Pivot_Menu_Edit")
		tde4.setWidgetCallbackFunction(self.req,"r_space","do.Pivot_Menu_Edit")	
#pick pivot point callback...
		tde4.setWidgetCallbackFunction(self.req,"pick_pivot","do.Pick_Pivot")
#average 3dpoint callback...
		tde4.setWidgetCallbackFunction(self.req,"avg_3dpoint","do.Average_3dpoint")	
		tde4.setWidgetCallbackFunction(self.req,"toggle","do.Frame_Range")							
		tde4.postCustomRequesterAndContinue(self.req,self.window_title,380,630,"do.update")
		
do = Nudge()
do.main()
		


