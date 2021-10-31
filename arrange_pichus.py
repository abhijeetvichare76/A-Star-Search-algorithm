#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Name: Abhijeet Vichare; username: abvichar; email: abvichar@iu.edu
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.' ]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

# Return all the locations that are horizontal, vertical and diagonal to the pichu
def agent_directional_locs(house_map):
    # input: house map (list)
    # steps: get all the pichu locations and then return all the directions to check for each of these pichus. 
    # return: all the pairs to check in the order of checking (list of tuples)
    pichu_locs = [ (r,c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == 'p' ]
    pairs_to_check = []
    for row,col in pichu_locs:
        #horizontal - right 
        pairs_to_check.append( [(row,col_check) for col_check in range(col+1,len(house_map[0]))  ] )
        #horizontal - left
        pairs_to_check.append([(row,col_check) for col_check in reversed(range( 0,col ))  ] )
        #vertical - down 
        pairs_to_check.append( [(row_check,col) for row_check in range(row+1,len(house_map))  ] )
        #vertical - up
        pairs_to_check.append( [(row_check,col) for row_check in reversed(range(0,row) ) ] )
        #diagonal - right-down
        pairs_to_check.append([(row + diag_check, col + diag_check) for diag_check in range(1, min(len(house_map) - row,len(house_map[0]) - col) )  ])
        #diagonal - left up
        pairs_to_check.append([(row - diag_check, col - diag_check) for diag_check in range(1,min(row,col) ) ])
        #diagonal - right up
        pairs_to_check.append([(row + diag_check, col - diag_check) for diag_check in range(1, min(len(house_map) - row,col ))  ])
        #diagonal - left up
        pairs_to_check.append([(row - diag_check, col + diag_check) for diag_check in range(1,min(row,len(house_map[0]) - col) ) ])
    return pairs_to_check

def check_violation(house_map):
    # input: housemap (2D list)
    # Steps: get all the pairs to be checked. these are the horizontal, vertical and the diagonals for each pichu. 
    #   Then check if there are any other pichus it the directional path. If it sees any obstacle first then stop the search. 
    # return: bool (0/1)
    flag = 1 # 1 means no violation, 0 means violation
    locs_to_check = agent_directional_locs(house_map)
        #check all the directions to see if there are any violations
    for direction in locs_to_check:
        for r,c in direction:
            if house_map[r][c] in 'X@':
                break
            elif house_map[r][c]  == 'p':
                flag = 0
        if flag ==0:
            break
    return flag

def arrangement_cost(house_map):
    # input: house map (2D list)
    # Finds the locations blocked by new arrangement of pichus
    # Steps: Get all the directions for each pichu and then return number of unique locations blocked by the arrangement of pichus.
    blocking_locs = []
    locs_to_check = agent_directional_locs(house_map)
        #check all the directions to see if there are any violations
    for direction in locs_to_check:
        for r,c in direction:
            if house_map[r][c] in 'X@':
                break
            elif house_map[r][c]  == '.':
                blocking_locs.append((r,c))
    return len(list(set(blocking_locs)))

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#

# The solution to the provided problem was that it was not checking for violations in the positions and just checking the
# number of agents in the board. 

def solve(initial_house_map,k):
    # input: housemap (2D map), k -> int (number of pichus to be placed)
    # sort the fringe that has the lowest cost and pick its substates.
    # for each successors check if there are any states without any violations and check if its the goal state else add the successor the fringe.
    initial_cost = arrangement_cost(initial_house_map)
    fringe = [(initial_house_map,initial_cost)] # house map and costs
    while len(fringe) > 0:
        # fringe.sort(key = lambda i: i[1],reverse = True)
        for new_house_map in successors( fringe.pop()[0] ):
            if check_violation(new_house_map):
                if is_goal(new_house_map,k):
                    return (new_house_map,True)
                new_cost = arrangement_cost(new_house_map)
                fringe.append((new_house_map,new_cost))
    return (new_house_map,False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")

