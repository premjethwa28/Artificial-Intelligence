Name: Prem Atul Jethwa
UTA ID: 1001861810
Programming language: Python 

********************************
Task 2A: Posterior Probabilities
********************************

Description: Calculate the posterior probabilities given the prior probabilities.

Here the 'observations' is the string of combination of C's and L's.

For example: python compute_a_posteriori.py LLLLLLLLLLCCCCCCCCCC 

Structure:
The program takes the observation string as input from command-line.
The domain values provided in the question are used in the program. There are loops that start their execution 
until the end of the string. Then the probability of each candy is calculated and the new values are updated 
and these updated values are used for calculation in the next iteration.

Command line syntax to execute the code:
Execute : python compute_a_posteriori.py observation

Example:
Execute : python compute_a_posteriori.py CCLLCLCL

