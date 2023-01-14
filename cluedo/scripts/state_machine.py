#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import actionlib
import time
import random
from cluedo.msg import RobotAction, RobotFeedback, RobotResult, RobotGoal
from cluedo.msg import Hint, HintRequest,HypCheck, HypCheckRequest
from cluedo.srv import Coordinate, CoordinateResponse, CoordinateRequest

class GoToRoom(smach.State):
	def __init__(self):
		smach.State.__init(self, outcomes=['reached']
		
	def execute(self, userdata):
		rospy.loginfo('Executıng state GoToRoom')
		req = CoordinateRequest(reqState = True)
		resp = coordinate_client(req)
		goal = RobotGoal(x = resp.x, y =resp.y)
		robot_action_client.send_goal(goal)
		robot_actıon_client.wait_for_result()
		result = robot_action_client.get_result()
	while result.result == False:
		
				
def main():

	#initialize coordinate of rooms server
	coordinate_client = rospy.ServiceProxy('/coordinates', Coordinate)
	
	#initialize navigation server
	robot_action_client = actionlib.SimpleActionClient('/navigation', RobotAction)
	robot_action_client.wait_for_server()
	
	
		
