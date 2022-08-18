# -*- coding: utf-8 -*-
"""
@author: premjethwa, UTA ID : 1001861810
- Task 1: Implement a search algorithm that can find a route between any two cities.
- References: Lecture material of Artificial Intelligence 1 by Prof. Vamsikrishna Gopiskrishna

"""

import sys
#----------------------------------------------------Uninformed Search------------------------------------------------------#   
#------------------------------------------------------UCS algorithm--------------------------------------------------------#
class node_struct_u:
    def __init__(self, name, predecessor, cost):
        self.name = name
        self.predecessor = predecessor
        self.cost = cost
        
        
#Function to print the contents of the fringe
def display_fringe(fringe):
    if fringe == []:
        print("\nFringe is empty.")
    else:
        print("\nFringe: ")
        for i in fringe:
            print(f'|{i.name}||{i.cost}|')

#Function to print costs g(n) of cities
def return_city_cost(links, city, closed):
    c = list(links[city.name].keys()) 
    return_c = []    
    for i in range(len(c)):
        if c[i] not in closed: 
            return_c.append(node_struct_u(c[i], city, city.cost + links[city.name][c[i]])) # Node creation
    return return_c

#Function to determine node with min cost and pop the same
def ucs_pop(fringe, closed):
    min_cost = fringe[0].cost    
    return_node = fringe[0]      
    for i in fringe:              #find minimum cost
        if i.cost < min_cost:
            min_cost = i.cost
    print("Min cost:", min_cost)  #print min cost
    for i in fringe:            
        if i.cost == min_cost:
            return_node = i
            fringe.remove(i)    
    print("Popped node:", return_node.name) #print node to be popped
    if return_node.name not in closed:
        closed.append(return_node.name)  #add the popped node to closed
    return fringe, closed, return_node 

#Function to perform UCS algorithm
def UCS_algo(fringe, closed, goal, links, pm):
    #nodes_poped = 0
    nodes_expanded = 0
    nodes_generated = 0
    while True:
        fringe, closed, node = ucs_pop(fringe, closed) 
        if node.name == goal:
            print("Goal found!") 
            break
        city_cost = return_city_cost(links, node, closed)  
        nodes_expanded += 1
        for i in city_cost:
            if i.name not in closed:
                nodes_generated += 1
        for i in city_cost:
            fringe.append(i) # add to fringe
        display_fringe(fringe) if pm == 1 else None 
        print("Closed:", closed) if pm == 1 else None 
        
        # if fringe is empty then return to main function and print no path exists
        if fringe == []: 
            return -1
    
    #Path Tracing
    path = []
    x = node    
    path.append(node.name)
    print("\nPrint route information: ")
    while x.predecessor != None:
        path.append(x.predecessor.name)
        x = x.predecessor
    path = path[::-1]
    #print("Nodes Poped: ", nodes_poped)
    print("Nodes Expanded: ", nodes_expanded)
    print("Nodes Generated: ", nodes_generated)
    print(f'Distance: {node.cost} km')
    #print the path found
    print("Route:")
    for i in range(len(path) - 1):
        print(f'{path[i]} to {path[i+1]}, {links[path[i]][path[i+1]]} km')
    return node.cost

def uninformed_search(infile, start, goal):
    print(f"Input file: {infile}")
    print(f"Start city: {start}")
    print(f"Goal city: {goal}\n")
    #Read input file provided
    try:
        input1_txt = open(infile,'r')
    except Exception :
        print("ERROR: Unable to open the file.")
        return
    x = ''
    contents = []
    count = 1   
    while True:
        x = input1_txt.readline().rstrip("\n")
        contents.append(x)
        if x == 'END OF INPUT':
            break 
        count += 1               
    input1_txt.close()
    print("Completed reading input file.")
    contents.remove('END OF INPUT')
    #Creating a dictionary for links between every city combination available
    links = {}
    for i in contents:
        temp = i.split(" ")
        if temp[0] not in links.keys():
            links[temp[0]] = {temp[1]: int(temp[2])}
        else:
            links[temp[0]][temp[1]] = int(temp[2])
        if temp[1] not in links.keys():
            links[temp[1]] = {temp[0]: int(temp[2])}
        else:
            links[temp[1]][temp[0]] = int(temp[2])
    print_mode = -1
    while print_mode != 0 and print_mode != 1:
        try:
            print_mode = int(input("Enter 1 if you want to enter print mode or else 0: "))
        except Exception:
            print("Please enter either 1 or 0")
    start_node = node_struct_u(start, None, 0) 
    fringe = [start_node]        
    closed = []                  
    display_fringe(fringe) if print_mode == 1 else None  
    print("Closed:", closed) if print_mode == 1 else None 
    path = UCS_algo(fringe, closed, goal, links, print_mode) #Function call
    if path != -1:
        print(f'The total path cost is {path} km.') # Print path cost of the path found
    else:
        print(f'\nNo path exists between {start} and {goal}.') # Print message if no path found
        
        
#--------------------------------------------------Informed Search----------------------------------------------------------#   
#---------------------------------------------------A* algorithm------------------------------------------------------------#
class node_struct_i:
    def __init__(self, name, predecessor, cost , heuristic):
        self.name = name
        self.predecessor = predecessor
        self.cost = cost
        self.heuristic = heuristic

#Function to print the contents of the fringe
def display_fringe_i(fringe):
    if fringe == []:
        print("\nFringe is empty.")
    else:
        print("\nFringe: ")
        for i in fringe:
            print(f'|{i.name}||{i.cost}||{i.heuristic}|')

#Function to print cost g(n) of citiess
def return_city_cost_i(links, city, closed, heur):
    c = list(links[city.name].keys())
    return_c = []
    for i in range(len(c)):
        if c[i] not in closed:
            #Here heuristic is added to node structure which is f(n) = g(n) + h(n)
            return_c.append(node_struct_i(c[i], city, city.cost + links[city.name][c[i]], city.cost + links[city.name][c[i]] + heur[c[i]]))
    return return_c

#Function to determine node with min cost g(n) + heuristic h(n) i.e. f(n) and pop the same
def ucs_pop_i(fringe, closed):
    min_cost = fringe[0].heuristic
    return_node = fringe[0]
    for i in fringe:                    #find minimum cost
        if i.heuristic < min_cost:
            min_cost = i.heuristic
    print("Min cost:", min_cost)        #print min cost
    for i in fringe:
        if i.heuristic == min_cost:
            return_node = i
            fringe.remove(i)
    print("Popped node:", return_node.name)     #Pop min node
    if return_node.name not in closed:
        closed.append(return_node.name)
    return fringe, closed, return_node

#Function to perform A* algorithm
#Here we are considering heuristic parameter of node i.e. f(n) instead of just cost i.e. g(n)
def Astar_algo(fringe, closed, goal, links, heuristic_dict, pm):
    #nodes_poped = 0
    nodes_expanded = 0
    nodes_generated = 0
    while True:
        fringe, closed, node = ucs_pop_i(fringe, closed)
        if node.name == goal:
            print("Goal found!")
            break
        city_cost = return_city_cost_i(links, node, closed, heuristic_dict)
        nodes_expanded += 1
        for i in city_cost:
            if i.name not in closed:
                nodes_generated += 1
        for i in city_cost:
            fringe.append(i)
        display_fringe_i(fringe) if pm == 1 else None 
        print("Closed:", closed) if pm == 1 else None 
        if fringe == []:
            return -1
    # Path Tracing    
    path = []
    x = node
    #Find the path by tracing the predecessorecessor
    path.append(node.name)
    print("\nPrint route information: ")
    while x.predecessor != None:
        path.append(x.predecessor.name)
        x = x.predecessor
    #Print the path found
    path = path[::-1]
    #print("Nodes Poped: ", nodes_poped)
    print("Nodes Expanded: ", nodes_expanded)
    print("Nodes Generated: ", nodes_generated)
    print(f'Distance: {node.cost} km')
    # print the path found
    print("Route:")
    for i in range(len(path) - 1):
        print(f'{path[i]} to {path[i+1]}, {links[path[i]][path[i+1]]} km')
    return node.cost

def informed_search(infile, start, goal, hfile):
    print(f"Input file: {infile}")
    print(f"Start city: {start}")
    print(f"Goal city: {goal}")
    print(f"heuristic file: {hfile}\n")
    try:
        input1_txt = open(infile,'r')
    except Exception :
        print("ERROR: Unable to open the file.")
        return 
    x = ''
    contents = []
    count = 1
    while True:
        x = input1_txt.readline().rstrip("\n")
        contents.append(x)
        if x == 'END OF INPUT':
            break 
        count += 1
    input1_txt.close()
    print("Completed reading input file.")
    contents.remove('END OF INPUT')
    #Creating a dictionary for links between every city combination available
    links = {}
    for i in contents:
        temp = i.split(" ")
        if temp[0] not in links.keys():
            links[temp[0]] = {temp[1]: int(temp[2])}
        else:
            links[temp[0]][temp[1]] = int(temp[2])
        if temp[1] not in links.keys():
            links[temp[1]] = {temp[0]: int(temp[2])}
        else:
            links[temp[1]][temp[0]] = int(temp[2])                            
    #Reading heuristic file
    try:
        h_kassel_txt = open( hfile,'r')
    except Exception :
        print("ERROR: Unable to open the file.")
        return
    x = ''
    heur = []
    count = 1   
    while True:
        x = h_kassel_txt.readline().rstrip("\n")
        heur.append(x)
        if x == 'END OF INPUT':
            break 
        count += 1
    h_kassel_txt.close()
    print("Completed reading heuristic file.")
    heur.remove('END OF INPUT')
    heuristic = {}
    for i in heur:
        x = i.split(" ")
        heuristic[x[0]] = int(x[1])
    print_mode = -1
    while print_mode != 0 and print_mode != 1:
        try:
            print_mode = int(input("Enter 1 if you want to enter print mode or else 0: "))
        except Exception :
            print("Please enter either either 1 or 0")
    start_node = node_struct_i(start, None, 0, heuristic[start]) 
    fringe = [start_node]       
    closed = []                 
    display_fringe_i(fringe) if print_mode == 1 else None 
    print("Closed:", closed) if print_mode == 1 else None
    path = Astar_algo(fringe, closed, goal, links, heuristic, print_mode) #Function call
    if path != -1:
        print(f'The total path cost is {path} km.')   #Print path cost of the path found
    else:
        print(f'\nNo path exists between {start} and {goal}.')   #Print message if no path found

#main function
def main():
    if len(sys.argv) == 4:
        print("3 arguments are provided. Therefore performing uninformed search\n")
        uninformed_search(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        print("4 arguments are provided. Therefore performing informed search\n")
        informed_search(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("ERROR: Number of arguments in the command are not as standard.")
           
main()