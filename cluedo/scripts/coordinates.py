#!/usr/bin/env python

from cluedo.srv import Coordinate, CoordinateResponse
import rospy
import random

oracle_room =[0.5,1.0]

rooms_dict = {'lounge': [1.5,1.5], 'kitchen': [2.0,2.5], 'dinning_room': [2.5,3.0], 'hall': [3.0,3.5], 'study': [3.5,4.0], 'library': [4.0,4.5], 'ball_room': [4.5,5.0], 'convervatory': [5.0,5.5], 'billiard_room': [6.0,6.0]}

def send_coordinates(req):
	request_state = req.reqState
	if (request_state == True):
		rooms_coord = list(rooms_dict.values())
		rand_coord = random.choice(rooms_coord)
		resp= CoordinateResponse(x = rand_coord[0], y = rand_coord[1])
	else:
		resp= CoordinateResponse(x = oracle_room[0], y = oracle_room[1])
	
	return resp
	
def main():
	rospy.init_node('coordinate_server')
	s = rospy.Service('coordinates', Coordinate, send_coordinates)
	rospy.spin()
	
if __name__ == '__main__':
	main()
