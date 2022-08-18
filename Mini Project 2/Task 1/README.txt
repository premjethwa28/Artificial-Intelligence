Name: Prem Atul Jethwa
UTA ID: 1001861810

*********************
Compiling And Running
*********************

All the text files are kept in the same directory as that of the graphplan on omega server.

To compile the software, use the command:
make graphplan

Once the program compiles, it can be invoked from the commandline as follows:
graphplan -o [operators_file] -f [facts_file]

For example:
************

************************************
Files for The Tower of Hanoi Problem
************************************

Problem 1: operator_file >> hanoi_ops.txt and facts_file >> hanoi_facts1.txt
	graphplan -o hanoi_ops.txt -f hanoi_facts1.txt
Problem 2: operator_file >> hanoi_ops.txt and facts_file >> hanoi_facts2.txt
	graphplan -o hanoi_ops.txt -f hanoi_facts2.txt
	
hanoi_facts_common.txt
The part of each facts file that is common to any problem in this domain

**********************
Task 1: Tower of Hanoi
**********************

Description: Problem consists of 3 towers with n number of disks (where n <= 5). No bigger disk
can be placed on top of smaller disk.

Assumption: disk1 is the smallest disk of all, disk2 is smaller than all disks except for disk1,
disk3 is smaller than disk4 and disk5, disk4 is smaller than disk5 only and disk5 is the biggest.

Constants: disk1, disk2, disk3, disk4, disk5, A, B, C
Here, diskn indicates nth disk and A, B, C are poles.

Predicates: 
1. isDisk(diska) -> True if diska object is disk else False
2. isPole(polea) -> True if polea object is pole else False
3. isSmaller(diska, diskb) -> True is diska is smaller than diskb else False
4. on(diska, diskb) -> True if diska is on diskb
5. on(diska, poleb) -> True if diska is the first disk on poleb
6. clear(object) -> True if the object i.e disk or pole is clear

Note: The initial state, goal state and the below actions are described using the above constants and 
predicates only

Actions:
1. move_d2d4p(diska, diskb, polec) -> This action moves disk diska from disk diskb to empty pole polec
2. move_d2d4d(diska, diskb, diskc) -> This action moves disk diska from disk diskb to clear disk diskc
3. move_d2p4p(diska, poleb, polec) -> This action moves disk diska from pole poleb to empty pole polec
4. move_d2p4d(diska, poleb, diskc) -> This action moves disk diska from pole poleb to clear disk diskc


************************
Task 2: 7 Puzzle Problem
************************

Description: Problem consists of 7 sliding blocks instead of 8 blocks compared to conventional sliding
block puzzle. Puzzle consists of 2 empty blocks instead of 1.

Constants: 1, 2, 3, 4, 5, 6, 7, X

Predicates: 
1. is11(x) -> True if x is present at location 1, 1
2. is12(x) -> True if x is present at location 1, 2
3. is13(x) -> True if x is present at location 1, 3
4. is21(x) -> True if x is present at location 2, 1
5. is22(x) -> True if x is present at location 2, 2
6. is23(x) -> True if x is present at location 2, 3
7. is31(x) -> True if x is present at location 3, 1
8. is32(x) -> True if x is present at location 3, 2
9. is33(x) -> True if x is present at location 3, 3

example: As per the initial state of Problem 1, is11(1) -> True since 1 is present at location 1, 1.

Actions:
Note that here moveYZ_DirectionBlock(a) means that move a from location Y, Z to DirectionBlock block
if DirectionBlock is empty i.e. contains X.
example:
Initial state:
1	X	3
4	5	6
7	2	X

State after move11_right(1):
X	1	3
4	5	6
7	2	X

Following is the list of all the actions defined:

 1. move11_right(a) -> moves a from location 1, 1 to right block if it is empty i.e. X
 2. move11_down(a) -> moves a from location 1, 1 to down block if it is empty i.e. X
 3. move12_left(a) -> moves a from location 1, 2 to left block if it is empty i.e. X
 4. move12_right(a) -> moves a from location 1, 2 to right block if it is empty i.e. X
 5. move12_down(a) -> moves a from location 1, 2 to down block if it is empty i.e. X
 6. move13_left(a) -> moves a from location 1, 3 to left block if it is empty i.e. X
 7. move13_down(a) -> moves a from location 1, 3 to down block if it is empty i.e. X
 8. move21_up(a) -> moves a from location 2, 1 to up block if it is empty i.e. X
 9. move21_down(a) -> moves a from location 2, 1 to down block if it is empty i.e. X
10. move21_right(a) -> moves a from location 2, 1 to right block if it is empty i.e. X
11. move22_up(a) -> moves a from location 2, 2 to up block if it is empty i.e. X
12. move22_down(a) -> moves a from location 2, 2 to down block if it is empty i.e. X
13. move22_right(a) -> moves a from location 2, 2 to right block if it is empty i.e. X
14. move22_left(a) -> moves a from location 2, 2 to left block if it is empty i.e. X
15. move23_up(a) -> moves a from location 2, 3 to up block if it is empty i.e. X
16. move23_down(a) -> moves a from location 2, 3 to down block if it is empty i.e. X
17. move23_left(a) -> moves a from location 2, 3 to left block if it is empty i.e. X
18. move31_up(a) -> moves a from location 3, 1 to up block if it is empty i.e. X
19. move31_right(a) -> moves a from location 3, 1 to right block if it is empty i.e. X
20. move32_up(a) -> moves a from location 3, 2 to up block if it is empty i.e. X
21. move32_right(a) -> moves a from location 3, 2 to right block if it is empty i.e. X
22. move32_left(a) -> moves a from location 3, 2 to left block if it is empty i.e. X
23. move33_up(a) -> moves a from location 3, 3 to up block if it is empty i.e. X
24. move33_left(a) -> moves a from location 3, 3 to left block if it is empty i.e. X

