- Name : Prem Atul Jethwa 
- UTA ID : 1001861810

- Programming Language Used : Python 
- About: This is a Python 3 script implementing Minimax algorithm with alpha-beta pruning for playing max connect 4 game. 
- References: 
	1. Basic script structure written by Chris Conly.
	2. Lecture material of Artificial Intelligence 1 course by Prof. Vamsikrishna Gopiskrishna.

- Command line commands to be used for runing the code :
	1. One move mode: python maxconnect4.py one-move input1.txt output1.txt 5 
	2. Interactive mode: python maxconnect4.py interactive input2.txt computer-next 5

- Description :

In above line "input1.txt" is the input file, it can be any name, "output1.txt" is the output file, it can be any name and "5" is the depth limit.
In above line "input1.txt" is the input file, it can be any name, "computer-first" is the flag that who plays first, it can also be "human-first" 
and "5" is the depth limit.
No additional compile command is required, it is not compatible with Omega.

- Code Structure :

	1. aiPlay() function calls the function Minimax() which returns the column number to be played by ai using minimax algorithm.
	2. In Minimax() function performs two things. First is creation of tree with calculated eval scores and second is perform 
	alpha beta pruning.
	3. The first part from above is performed using function create_child() function [to create tree] and get_leaf_val() function 
	to calculate evaluation scores for all possible boards after (depth-1) moves.
	4. The second part is performed using AlphaBetaPruning() function which performs alpha beta pruning by recursive call to MaxValue()
	and MinValue() function. These functions: AlphaBetaPruning(), MaxValue() and MinValue() are closely based on the function descriptions
	given by Prof. Vamsikrishna during the lecture.
	5. The AlphaBetaPruning() function determines the action i.e. column number to be played next and returns it to the Minimax()

- Evaluation function:

The evaluation function used here is computationally expensive but it is better at determining the next move compared to other functions that I used. 
The eval function is implemented as eval_func(). 

This eval_func() performs 3 operations:
	1. It creates dummy gameboard and replaces current player pieces with 1, zeros with 0 and opponent pieces with -1.
	2. It then applies multiple masks (around 70 masks in gen_masks() func) to dummy gameboard and sums up the resultant scores for each mask 
           applied gameboard. Each mask checks if the current player can get a score at that a particular set of 4 positions.
	3. After applying all masks, it also checks who is winning at that particular gameboard config using eval_func_custom() which just finds score
	   of current player minus score of the opponent and our main eval func adds it to final score as well.

More information about mask application to gameboard is present in "Mask generator" excel file, containing time required for different depth values.
