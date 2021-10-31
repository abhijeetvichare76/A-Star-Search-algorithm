### This code is part of the assignment for the subject CS-B551 (Elements of Artificial Intelligence) taught by Prof. David Crandall. 
#### The code is the application of A-star search algorithm to solve a route finding and the "8 Queen" problem.
# a0
## Q1: route_pichu

The given problem is finding an optimal route to a target location, given there is a possible route to take. 
The agent (Pichu) can move one step in one of the directions (up, down, left, or right). 

The code provided is a good starting point to solve this problem. 
It can filter all the moves possible by the agent. 
The original search function finds the initial state of the agent. and the initial state of the fringe.
It also provides the base framework of a DFS algorithm where it constantly searches for the successor of the last item in the fringe. 

Following are the main issues with the default solution :
1. it would not give the most optimal solution and the first solution that it finds. 
2. It does not consider the locations that it has already visited. So if the agent moves two steps forward, it would also add a state to the fringe where it will again move two steps backward, and the process will repeat indefinitely.

The final solution tries to solve this problem by solving the problem with the A* algorithm.
The function *"direction"* translates the relative movement of the agent into a string, and this movement is stored in the fringe to follow the agent's path. 

**The final solution uploaded assumes that the agent knows the location of the target. The assumption is used to design the heuristic function, which considers the manhattan distance between the agent and the target location.**

The solution takes the lowest ```f(s)``` value which is a combination of the cost function (distance travelled) and the heuristic function (manhattan distance) which makes the algorithm optimal and complete. 

The problem of revisiting the location is solved by the following logic: 
    1. If the path has already been travelled don't add it to the fringe. 
    2. If the current location is already visited and the agent has reached there in a lower cost than the current cost then don't add it to the fringe. 
    
**State Space:** All the possible locations the agent can travel to. 
**Cost:** The distance travelled by the pichu. 
**Heuristic:** Manhattan distance between the agent and the target location.

## Q2: arrange_pichu

The given problem aims to find a solution where you place pichus so they can't look at each other—the walls and the person in the house act as obstacles. 

The given problem has an almost perfect solution. It starts by putting the pichus in empty places and checks if it found a solution arrangement. 
The issue with that is that it does not check whether the agents can see each other or not. 

The main goal of solving the issue is by figuring out a way to check the violations happening in the arrangements. 
The solution approach here is that first, all the present location of the pichus is stored in a list. Then, for each Pichu, we move outwards from that Pichu in 8 directions (up, down, left, right, up-left, down-left, down-right, up-right) and see if there are any pichus placed before we find any wall in that direction. 

Adding the mentioned condition makes the algorithm complete. 

2. To make the algorithm a bit faster, a heuristic function was added that calculated the number of locations blocked by the current arrangement of pichus, where a location is called as "blocked" is any Pichu can "see" the location. Each state from the fringe is selected to branch out based on the minimum value of a heuristic. 

**State Space:** All the dots in the map, i.e., all the possible locations where the agent can be placed. 
**Cost:** The space occupied by the pichus (+1 for each new successor)
**Goal State:** Arrangement of k agents (pichus) so they can't "see" each other. 
**Successor function:** A agent placed in an empty location if any other Pichu can't see them. 