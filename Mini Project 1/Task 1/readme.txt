- Name : Prem Atul Jethwa
- UTA ID : 1001861810

- Programming Language Used : Python (Not compatible on Omega)
- About: This is a Python 3 script that performs uninformed and informed state space search on the graph provided in text file.
- References: Lecture material of Artificial Intelligence 1 course by Prof. Vamsikrishna Gopiskrishna

- Command line commands to be used for runing the code:
	1. Uninformed search: python find_route.py input1.txt Bremen Kassel
	2. Informed search: python find_route.py input1.txt Bremen Kassel h_kassel.txt

- Functions/Methods:

1. def return_city_cost(links, city, closed): Function to cities that are adjacent to 'city' along with their costs g(n)
2. def ucs_pop(fringe, closed): Function to determine node with min cost and pop the same
3. def UCS_algo(fringe, closed, goal, links, pm): Function to perform UCS algorithm	
4. def ucs_pop_i(fringe, closed): which is f(n) i.e. g(n) + h(n) instead of just cost i.e. g(n)
5. def Astar_algo(fringe, closed, goal, links, heuristics_dict, pm): Function to perform A* algorithm

- Description:

The python file 'find_route.py' performs uninformed (UCS) and informed (A star) state space search on the graph provided in input_textfile. 
For informed search, it uses additional file heursitics_textfile which provides heuristics to perform the search.
Following is the basic operation of the code.

1: Uninformed search:
After executing the command as mentioned above it will ask whether you want to print fringe and closed list after every node 
is popped from the list. If you enter 1 then it will print fringe and closed otherwise it will just print the nodes that are popped.
Next it will perform the UCS using graph search. Depending upon whether a path exists between entered source and destination, the code 
will display the minimum cost path between them or print that no path exists between them.

2: Informed search:
Works exactly like uninformed search but using heuristics file as well. f(n) = g(n) + h(n)

