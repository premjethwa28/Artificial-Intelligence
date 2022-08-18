Name: Prem Atul Jethwa
UTA ID: 1001861810
Programming language: Python 

*************************
Task 2B: Bayesian Network
*************************

Description: Compute and print out the probability of any combination of events given any other 
combination of events

Structure:
The program takes observations and arguments from the command line. The class BayesianNetwork is used to calculate
the probability of the query. It stores the data of the domain values provided in the functions. The Baynet 
method computeProbability calculates the probability for the given query.

Note: The values are not hardcoded but calculated on the go
            if v1:
                return 0.002
            else:
                return (1-0.002)


Command line syntax to execute the code:
python bnet.py arguments (Only 1-6 arguments are allowed)
python bnet.py query1 query2 given observation1

Example:
python bnet.py At Bf given Mt
python bnet.py Bt Af Mf Jt Et

