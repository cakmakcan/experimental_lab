#!/usr/bin/env python

import rospy
import action_msgs.srv import Navigation, NavigationResponse
import time

def go_poi(poi_req):
        #rosparam get /<name of parameter>
	goal= rospy.get_param("/map/{poi_req}")
	rospy.loginfo("Robot goes tp the poi {goal_cord['loc']} x: {goal_cord['x']}, y: {goal_cord['y']}")
	
	time.sleep(3)
	
	return "goal reached"
	
def robot_nav_clbk(req):
	if rospy.has_param("/map/{req.goal}"):
		result = go_poi(req.goal)
		#returning the result("goal reached") as response
		return NavigationResponse(result)
	
	else:
		return NavigationResponse("Invalid target")
		
def main():
	#Initialize the ros node
	rospy.init_node("robot_navigation")
	#Initilize the service
	rospy.Service("robot_nav_srv", RobotNav, robot_nav_clbk)
	
	rospy.spin()
	
if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass
