#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : name: Abhijeet Vichare; username: abvichar; email: abvichar@iu.edu
#
# Based on skeleton code provided in CSCI B551, Fall 2021.
import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]
def direction(curr_move,next_move):
        # Find the direction of move from move:
        # Input: curr_move (grid location in tuple) and next_move (grid location in tuple)
        # The function takes the relative movement of the pichu and converts it to a direction in a string format
        # return: single character string containing one of the following values ["U","D","L","R" ,""]
        if curr_move[0]+1 == next_move[0]:
                return 'D'
        elif curr_move[0]-1 == next_move[0]:
                return 'U'
        elif curr_move[1]+1 == next_move[1]:
                return 'R'
        elif curr_move[1]-1 == next_move[1]:
                return 'L'
        else:
                return ''
def manhattan_heuristic(curr_move,target_loc):
        # returns the manhattan distance between the current location and the target location
        # Input: Takes the location of pichu and the person in tuple form 
        # Return: int representing the manhattan distinace
        return abs(curr_move[0] - target_loc[0]) + abs(curr_move[1] - target_loc[1])

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Implementing the a* search algorithm to find the shortest distance to the agent.

        # Find pichu start position and the target start location
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        target_loc = [(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
        fringe=[(pichu_loc,0,'',0+manhattan_heuristic(pichu_loc ,target_loc))] #fringe format : (location, cost_function, steps taken in a string format, heuristic fn value)
        # if initial state is goal state return initial state. Won't happen in our case but better to cover it
        if house_map[pichu_loc[0]][pichu_loc[1]] == "@":
                return (0,'')

        # closed will keep track of the visited locations and the shortest path to reach there. ( coordinates, curr_dist, heurstic + curr_dist cost , path); default variable is the closed state of start position
        closed = [(pichu_loc,0,0 + manhattan_heuristic(pichu_loc,target_loc),'')] 

        # Steps followed below: 
        # 1. Sort the fringe in a decending manner based on its heuristic value.
        # 2. Take the last element of fringe and remove it, and find all the succesors.
        # 3. If the successor is target location end the function
        # 4. elif the path has already been used then don't add it to the fringe. 
        # 5. elif we can reach the next successor in a reduced cost, skip addiing this state to the fringe.
        # 5. Else add the state to the fringe.
        while fringe:
                fringe.sort(key = lambda i: i[3],reverse = True)
                (curr_move, curr_dist,curr_path,curr_cost)=fringe.pop()
                closed.append((curr_move,curr_dist,curr_dist+manhattan_heuristic(curr_move ,target_loc),curr_path))
                for move in moves(house_map, *curr_move):
                        next_path= curr_path + direction(curr_move,move)
                        if house_map[move[0]][move[1]]=="@":
                                return (curr_dist+1, next_path)
                        elif next_path in [element[2] for element in closed] :
                                continue
                        elif len([close_instance for close_instance in closed if (close_instance[0] == move) &
                                                                (close_instance[1]<= curr_dist+1 + manhattan_heuristic(move ,target_loc) )]
                                                                )>0:
                                continue
                        else:
                                fringe.append((move, curr_dist + 1,next_path,curr_dist+1 + manhattan_heuristic(move ,target_loc)))
        return -1

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

