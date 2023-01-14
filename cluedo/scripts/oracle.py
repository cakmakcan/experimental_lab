#!/usr/bin/env python

import rospy
import random
from cluedo.srv import Hint, HintResponse
from cluedo.srv import HypCheck



IDlist= [ID1,ID2,ID3,ID4,ID5,ID6,ID7,ID8]

ID1 =[["who","Plum"],["where","kitchen"],["what","revolver"]]
ID2 = [["who","Mustard"],["where","hall"],["what","pipe"]]
ID3 = [["who","Green"],["where","library"],["what","rope"]]
ID4 = [["who","Peacock"],["where","study"],["what","dagger"]]
ID5 = [["who","White"],["where","lounge"],["what","spanner"]]
ID6 = [["who","Mustard"],["where","dining"],["what","candlestick"]]
ID7 = [["who","Green"],["where","billiard"],["what","pipe"]]
ID8 = [["who","Plum"],["where","library"],["what","revolver"]

correctID = ID4

def send_hint(req):

	 reqid= req.ID
	 chosenID = IDlist[reqid]
	 randomindex = random.randint(0,len(chosenID)-1)
	 hint = chosenID[randomindex]
	 resp = HintResponse(arg1 = hint[0], hint[1] )
	 del chosenID[randomindex]
	 
	 return resp
	 
def check(req):
    """
    This function is the callback for the service /check_hyp 
    It receives a request with a specific hypothesis ID, and checks whether this ID is the correct hypothesis ID or not.
    
    Args:
      req(HypCheckRequest): the service request containing the hypothesis ID to be checked
    
    Returns:
      a boolean value indicating whether this is the correct ID or not
     
    """
    return req.ID == correct_ID 
    
def main():

	rospy.init_node('oracle')
	hint_service = rospy.Service('/hint', Hint, send_hint)
	check_service = rospy.Service('/check_hyp', HypCheck, check)
	rospy.spin()
	
if __name__ == 'main':
	main()
	 
