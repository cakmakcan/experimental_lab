#!/usr/bin/env python

import rospy
import actionlib
import time
from cludeo.msg import RobotAction, RobotFeedback, RobotResult, RobotGoal

class ActionServer():

	def __init__(self):
		self.a_server = actionlib.SimpleActionServer("navigation_as", RobotAction, execute_cb= self.execute_cb, auto_start = False)
		self.a_server.start()
		
	def execute_cb(self,goal):
	
		success = True
		desired_positionx = goal.x
		desiderd_positiony = goal.y
		feedback = RobotFeedBack()
		outcome = RobotResult()
		outcome.result = False
		while not rospy.is_shutdown():
			feedback.x = desired_positionx
			feedback.y = desired_positiony
			self.a_server.publish_feedback(feedback)
			if self.server.is_preempt_requested():
				rospy.loginfo("Goal was reempted')
				self.server.set_preempted()
				success = False
				break
			time.sleep(5)
			if success:
				outcome.result = True
				self.a_server.set_succeeded(result)	
		
			
if __name__ = '__main__':
	rospy.init_node("navigation_server")
	s = ActionServer()
	rospy.spin()	
