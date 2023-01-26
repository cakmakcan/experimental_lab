#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import actionlib
import time
import random
from armor_api.armor_client import ArmorClient
from cluedo.msg import RobotAction, RobotFeedback, RobotResult, RobotGoal
from cluedo.srv import Hint, HintRequest, HypCheck, HypCheckRequest
from cluedo.srv import Coordinate, CoordinateResponse, CoordinateRequest

path = "/root/Desktop/" #the path to cluedo ontology (.owl) file
ontology_IRI = "http://www.emarolab.it/cluedo-ontology"
ID=[1,2,3,4,5,6,7,8]

class GoToRoom(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['reached'])
		
	def execute(self, userdata):
		rospy.loginfo('Executıng state GoToRoom')
		req = CoordinateRequest(reqState = True)
		resp = coordinate_client(req)
		goal = RobotGoal(x = resp.x, y =resp.y)
		robot_action_client.send_goal(goal)
		robot_action_client.wait_for_result()
		result = robot_action_client.get_result()
		while result.result == False:
			req = CoordinateRequest(reqState = True)
			resp = coordinate_client(req)
			goal = RobotGoal(x = resp.x, y =resp.y)
			robot_action_client.send_goal(goal)
			robot_action_client.wait_for_result()
			result = robot_action_client.get_result()
		print("Robot has reached room target")
		return 'reached'
						
class SearchHints(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['hyp_comp','hyp_non_comp'])
	
	def execute(self,userdata):
		req = HintRequest(ID = randInd)
		hint_args = oracle_hint_client(req)
		print("the hint is:", hint_args)
		command = hint_args.arg0
		thing = hint_args.arg1
		#add the hint to the current hypothesis object properties
		if hint_args.arg1 == "what":
			armor_client.manipulation.add_ind_to_class(thing, "WEAPON")
			armor_client.manipulation.add_objectprop_to_ind(hint_args.arg1, currID, hint_args.arg2)
		elif hint_args.arg1 == "who":
			armor_client.manipulation.add_ind_to_class(thing, "PERSON")
			armor_client.manipulation.add_objectprop_to_ind(hint_args.arg1, currID, hint_args.arg2)
		elif hint_args.arg1 == "where":
			armor_client.manipulation.add_ind_to_class(thing, "PLACE")
			armor_client.manipulation.add_objectprop_to_ind(hint_args.arg1, currID, hint_args.arg2)
        
		#apply the changes
		armor_client.utils.apply_buffered_changes()
		armor_client.utils.sync_buffered_reasoner()
		#get the list of current complete hypotheses
		complete_hyp_links = armor_client.query.ind_b2_class("COMPLETED")
		complete_hyp = [x.replace("<"+ontology_IRI+"#", '').replace('>','') for x in complete_hyp_links]
        
		#check if the current hypothesis is complete
		if currID in complete_hyp:
			print("hypothesis %s is COMPLETE",currID)
			return "hyp_comp"
		else:
			print("Hypothesis not complete yet! Keep searching for hints")
			return "hyp_non_comp"


class GoToOracle(smach.State):

	def __init__(self):
		smach.State.__init__(self, outcomes=['reached'])
		
	def execute(self,userdata):
		rospy.loginfo('Executıng state GoToRoom')
		req = CoordinateRequest(reqState = False)
		resp = coordinate_client(req)
		goal = RobotGoal(x = resp.x, y =resp.y)
		robot_action_client.send_goal(goal)
		robot_action_client.wait_for_result()
		result = robot_action_client.get_result()
		while result.result == False:
			req = CoordinateRequest(reqState = True)
			resp = coordinate_client(req)
			goal = RobotGoal(x = resp.x, y =resp.y)
			robot_action_client.send_goal(goal)
			robot_action_client.wait_for_result()
			result = robot_action_client.get_result()
		print("Robot has reached room target")
		return 'reached'
		
class CheckHypothesis(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['hyp_comp','hyp_false'])
	
	def execute(self, userdata):
		global currID
		rospy.loginfo('Executing state CheckHypothesis')
		
		#get all object properties of this hypothesis ID
		ind_names_links = armor_client.query.objectprop_b2_ind('who', currID)
		who_name = [x.replace("<"+ontology_IRI+"#", '').replace('>','') for x in ind_names_links]
		ind_names_links = armor_client.query.objectprop_b2_ind('where', currID)
		where_name = [x.replace("<"+ontology_IRI+"#", '').replace('>','') for x in ind_names_links]
		ind_names_links = armor_client.query.objectprop_b2_ind('what', currID)
		what_name = [x.replace("<"+ontology_IRI+"#", '').replace('>','') for x in ind_names_links]
		
		print("The collected hypothesis ",currID, " is: who-->",who_name[0] , ", where-->",where_name[0], ", what-->",what_name[0])
		
		#check if hypothesis is correct or not
		req = HypCheckRequest(ID = randInd)
		res = oracle_check_client(req)
		if res.correct:
			print("THIS IS THE CORRECT ANSWER! Please, terminate the program")
			armor_client.utils.save_ref_with_inferences(path + "cluedo_submitted.owl")
			#wait for two minutes to allow the user to terminate
			time.sleep(120)
			return "hyp_comp"
		else:
			print("Hypothesis is FALSE")
			# Get a new random hypothesis ID
			randInd = random.randint(0,len(IDs)-1)  #get a random index of the IDs list
			currID = 'ID'+str(IDs[randInd])  #get the current hypothesis ID to be investigated (chosen randomly)
			del ID[randInd]    #delete this ID from the list so as not to be chosen again
			print("new hypothesis ID is %s"%currID)
			return "hyp_false"
def main():
	global armor_client
	global coordinate_client, robot_action_client,oracle_hint_client, oracle_check_client
	global ID
	global currID,randInd
	
	rospy.init_node('state_machine')
	
	
	#initialize the server coordinate of rooms
	coordinate_client = rospy.ServiceProxy('/coordinates', Coordinate)
	
	#initialize navigation server
	robot_action_client = actionlib.SimpleActionClient('/navigation_as', RobotAction)
	robot_action_client.wait_for_server()
	
	#initialize the oracle server
	oracle_hint_client = rospy.ServiceProxy('/hint', Hint)
	oracle_check_client = rospy.ServiceProxy('/check_hyp', HypCheck)
	
	
	# Start ARMOR client and load the cluedo ontology
	armor_client = ArmorClient("client", "reference")
	armor_client.utils.load_ref_from_file(path + "cluedo_ontology.owl", ontology_IRI,
                                True, "PELLET", True, False)  # initializing with buffered manipulation and reasoning
	armor_client.utils.mount_on_ref()
	armor_client.utils.set_log_to_terminal(True)
	
	# Create a SMACH state machine
	sm = smach.StateMachine(outcomes=['container_interface'])
	
	with sm:
		# Add states to the container
		smach.StateMachine.add('GoToRoom', GoToRoom(), 
                               	transitions={'reached':'SearchHints'
                               		     })
		smach.StateMachine.add('SearchHints', SearchHints(), 
                               	transitions={'hyp_non_comp':'GoToRoom',
                                            	     'hyp_comp':'GoToOracle'
                                            	     })
		smach.StateMachine.add('GoToOracle', GoToOracle(), 
                               	transitions={'reached':'CheckHypothesis', 
                                            	    })
		smach.StateMachine.add('CheckHypothesis', CheckHypothesis(), 
                               	transitions={'hyp_comp':'CheckHypothesis',
                                                    'hyp_false':'GoToRoom'})
	
	randInd = random.randint(0,len(ID)-1)  #get a random index of the IDs list
	currID = 'ID'+str(ID[randInd])  #get the current hypothesis ID to be investigated (chosen randomly)
	del ID[randInd]    #delete this ID from the list so as not to be chosen again
	print("New hypothesis ID is %s"%currID)
    
	#add it to the hypothesis class
	armor_client.manipulation.add_ind_to_class(currID, "HYPOTHESIS")
	armor_client.manipulation.add_dataprop_to_ind("hasID", currID, "STRING", currID)
	#apply the changes
	armor_client.utils.apply_buffered_changes()
	armor_client.utils.sync_buffered_reasoner()
    
	# Create and start the introspection server for visualization
	#sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
	#sis.start()

	# Execute the state machine
	outcome = sm.execute()

	# Wait for ctrl-c to stop the application
	rospy.spin()
	sis.stop()


if __name__ == '__main__':
    main()
		
