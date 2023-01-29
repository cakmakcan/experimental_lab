# ExpRob_CluedoGame
This is a ROS implementation of a robot agent playing a simplified Cluedo Game with its knowledge represented in OWL ontology.

Author Name : Can Cakmak
Student Number: 5054534
E-mail Adress: cakmak1213@gmail.com

##Introduction:

Context of this project is the agent goest to random rooms and collects the hints such as (who, Person), (where, Place) and (what, WEAPON). When the hints are colllected, they are checked by oracle in order to determine that whether Hypothesis are correct or not. If it is not correct, agent will look for hints again to be able to find the right one.

##Component Diagram:

- **The knowledge base (ontology)**: this is the OWL ontology representing the current knowledge of the robot agent. In the beginning it contains the class definitions of `HYPOTHESIS`, `COMPLETE`, `INCONSISTENT`, `PERSON`, `PLACE`, and `WEAPON`, as well as the object properties definitions of *(who, PERSON)*, *(where, PLACE)*, and *(what, WEAPON)*. As the robot explores the environment, new individuals and proberties assertions are added to the ontology.

 - **State Machine**: this is the state manager of the robot. It is responsible for controlling the transitions between different robot states (*GoToRoom*, *SearchHints*, *GoToOracle*, and *CheckHypothesis*). It also implements the robot behaviour in each state. It communicates with the other servers through different ROS messages. The ROS messages and parameters are indicated in the component diagram.

- **ARMOR**: the armor service responsible for connection with the knowledge base for querying the ontology or manipulating it. It is fully implemented by [EmaroLab](https://github.com/EmaroLab/armor). In this project, it is mainly used by the state machine for adding new hypotheses and hints, and querying the individuals of COMPLETE hypothesis class.

- **Navigation Server**: This node is composed of room coordinates in order for robot to reach the points. As a request, it takes 'bool randFlag' variable. If the flag is True, it sends a random room coordinate. Otherwise, in the case of False, it responds oracle's coordinate.

- **Oracle**: This component holds ID of hints as a list for each ID. Correct ID of hypothesis is also determined in advance. After receiving ID number by State_machine node, random index of ID is chosend in order to be sent as arg0 and arg1 as response to state machine. Hypothesis check service is also in this node. 

- **Motion Controller**: this is the action server responsible for driving the robot towards a target *(x,y)* position.

![alt text](https://github.com/cakmakcan/experimental_lab/blob/master/cluedo/images/ComponentDiagram.png?raw=true)


