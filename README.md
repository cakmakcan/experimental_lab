# ExpRob_CluedoGame
This is a ROS implementation of a robot agent playing a simplified Cluedo Game with its knowledge represented in OWL ontology.

Author Name : Can Cakmak
Student Number: 5054534
E-mail Adress: cakmak1213@gmail.com

## Introduction:

Context of this project is the agent goest to random rooms and collects the hints such as (who, Person), (where, Place) and (what, WEAPON). When the hints are colllected, they are checked by oracle in order to determine that whether Hypothesis are correct or not. If it is not correct, agent will look for hints again to be able to find the right one.

## Component Diagram:

- **The knowledge base (ontology)**: this is the OWL ontology representing the current knowledge of the robot agent. In the beginning it contains the class definitions of `HYPOTHESIS`, `COMPLETE`, `INCONSISTENT`, `PERSON`, `PLACE`, and `WEAPON`, as well as the object properties definitions of *(who, PERSON)*, *(where, PLACE)*, and *(what, WEAPON)*. As the robot explores the environment, new individuals and proberties assertions are added to the ontology.

 - **State Machine**: this is the state manager of the robot. It is responsible for controlling the transitions between different robot states (*GoToRoom*, *SearchHints*, *GoToOracle*, and *CheckHypothesis*). It also implements the robot behaviour in each state. It communicates with the other servers through different ROS messages. The ROS messages and parameters are indicated in the component diagram.

- **ARMOR**: the armor service responsible for connection with the knowledge base for querying the ontology or manipulating it. It is fully implemented by [EmaroLab](https://github.com/EmaroLab/armor). In this project, it is mainly used by the state machine for adding new hypotheses and hints, and querying the individuals of COMPLETE hypothesis class.

- **Navigation Server**: This node is composed of room coordinates in order for robot to reach the points. As a request, it takes 'bool randFlag' variable. If the flag is True, it sends a random room coordinate. Otherwise, in the case of False, it responds oracle's coordinate.

- **Oracle**: This component holds ID of hints as a list for each ID. Correct ID of hypothesis is also determined in advance. After receiving ID number by State_machine node, random index of ID is chosend in order to be sent as arg0 and arg1 as response to state machine. Hypothesis check service is also in this node. 

- **Motion Controller**: this is the action server responsible for driving the robot towards a target *(x,y)* position.

![alt text](https://github.com/cakmakcan/experimental_lab/blob/master/cluedo/images/ComponentDiagram.png?raw=true)

## State Diagram:

The agent has four possible states:
- **GoToRoom:** the robot is going to a random room for exploration
- **SearchHints:** the robot is looking for hints in the place it is currently in
- **GoToOracle:** the robot is going to the oracle place
- **CheckHypothesis:** the robot is checking whether its current collected hypothesis is true or not

There are, also, four possible events (state transitions):
- **reached:** indicating an event that the robot reached its target position
- **hyp_non_comp:** indicating an event that the robot checked the current hypothesis and found that it is not complete yet
- **hyp_comp:** indicating an event that the robot checked the current hypothesis and found that it is complete
- **false:** indicating that the oracle checked the current hypothesis and found that it is false.

![alt text](https://github.com/cakmakcan/experimental_lab/blob/master/cluedo/images/StateDiagram.png)

## Sequence Diagram:
The temporal sequence of the program goes as follows:

1. The state machine requests a random room from the coordinate server, and receives the *(x,y)* position
2. it sends the room coordinates to the motion controller and waits until the robot reaches the target
3. it sends the current hypothesis ID to the oracle and receives a random hint
4. it adds the hint to the ontology
5. it checks if the current hypothesis is complete or not (by querying the members of the `COMPLETE` class in the ontology)
6. if the current hypothesis is not complete yet, go to step 1
7. if the current hypothesis is complete, the state machine requests the *(x,y)* position of the oracle from the map server
8. it sends the oracle coordinates to the motion controller and waits until the robot reaches the target
9. it sends the current hypothesis ID to the oracle to check if it is correct or not
10. if the sent hypothesis ID is not correct, generate a new random integer (not previously selected) from 1 to 10 to be the current hypothesis ID and go to step 1.
11. if the sent hypothesis ID is correct, end the program.

![alt text](https://github.com/cakmakcan/experimental_lab/blob/master/cluedo/images/SequenceDiagram.png)

## Installation and Running Procedures:

To run the program, you need first to install [ARMOR](https://github.com/EmaroLab/armor) in your ROS workspace.

Then, you need to adapt the code in armor_py_api scripts to be in Python3 instead of Python2:
  - add "from armor_api.armor_exceptions import ArmorServiceInternalError, ArmorServiceCallError" in armor_client.py
  - replace all "except rospy.ServiceException, e" with "except rospy.ServiceException as e"
  - modify line 132 of armor_query_client with: "if res.success and len(res.queried_objects) > 1:"

Add the path of the armor modules to your Python path:
```
export PYTHONPATH=$PYTHONPATH:/root/ros_ws/src/armor/armor_py_api/scripts/armor_api/
```
Download this repository to your workspace. Then, build it

```
catkin_make
```

Place `cluedo_ontology.owl` file on your desktop (or on any other place, but you need to specify the path inside [state_machine.py](https://github.com/yaraalaa0/ExpRob_CluedoGame/blob/main/cluedo/scripts/state_machine.py))

To launch the program, run the following commands on different terminal tabs:
```
roscore
```
```
rosrun armor execute it.emarolab.armor.ARMORMainService
```
```
roslaunch cluedo cluedo.launch`

```

## Result:

**Following are screenshots of the terminal logs in successive timesteps while running the program:**

1. First, Hypothesis ID is chosen by program and the GoToRoom state runs. After return reached, state move SearchHin state.
2. The first hint is found arg0 and arg1. Hypothesis is checked if it is completed or not.
3. The robot will continue to search other hints with GoToRoom state.
4. After hints are completed, robot change the state to GoToOracle.
5. It will check hypothesis, whether hyp is true or not.
6. If it is not true, it will keep searching new hints until hyp is completed.

![alt text](https://github.com/cakmakcan/experimental_lab/blob/master/cluedo/images/Screenshot%20from%202023-01-28%2019-33-49.png)

When the Hypothesis is completed and true, game finish.

![alt text](https://github.com/cakmakcan/experimental_lab/blob/master/cluedo/images/Screenshot%20from%202023-01-28%2019-34-46.png)


## Working Assumptions:
- The hints are selected randomly from the oracle.py node as a list for each ID number.
- In the dictionary of hints stored in the oracle, each hypothesis has four hints. Three are of the types: *(who,PERSON)*, *(what,WEAPON)*, *(where,PLACE)*. The fourth one is the empty hint.
- The robot can get one hint at a time from the same room. 
- The hint obtained at each room doesn't have to be related to the type of room itself. For example, the agent can receive a hint (where, bathroom) in the kitchen.
- Whenever a hint is sent to the robot, it is deleted from the list in order not to be sent again. 
- The robot only goes to the oracle when the current hypothesis is `COMPLETE`
- The new current hypothesis ID is selected randomly from the list of possible hypothesis IDs. 
- The list of possible hypothesis IDs range from 1 to 8 and they can be modified in the beginning of [state_machine.py]
- Whenever an ID is selected, it cannot be selected again.
- The environment map of obstacles is stored in the motion controller action server for path planning purposes.

## Possible Improvements:
- Allow a hypothesis not to necessarily contain all three types of hints. It can contain only one or two types. It can be inconsistent.
- Implement a robot model and a game environment to be more realistic.
- Implement a real motion controller for the robot instead of the simple waiting function.
