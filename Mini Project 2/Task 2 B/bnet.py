# -*- coding: utf-8 -*-
"""

@author: Prem Atul Jethwa
UTA id: 1001861810
Programming language used: Python 3.9.6
"""

import sys
from sys import argv

class BayesianNetwork(object):
    def probabilityDistribution(self,q,v1,v2,v3):
        #Given probability for Burglary b = 0.001 and ~b is (1-b) & Burglary has no parent
        if q == "B":
            if v1:
                return 0.001
            else:
                return (1-0.001)

        #Given probability for Earthquake e = 0.002 and ~e = (1-e) & earthquake has no parent
        if q == "E":
            if v1:
                return 0.002
            else:
                return (1-0.002)
               
        #Given probability of JohnCalls & parent is Alarm
        if q == "J|A":
            if v2:
                tmp = 0.9
            else:
                tmp = 0.05
            if v1:
                return tmp
            else:
                return (1-tmp)
        
        #Given probability of MaryCalls & parent is Alarm
        if q == "M|A":
            if v2:
                tmp = 0.7
            else:
                tmp = 0.01
            if v1:
                return tmp
            else:
                return (1-tmp)
        
        #Given probability of Alarm & parents are Burglary and Earthquake
        if q == "A|B,E":
            if v2 and v3:
                tmp = 0.95
            if v2 and not v3:
                tmp = 0.94
            if not v2 and v3:
                tmp = 0.29
            if not v2 and not v3:
                tmp = 0.001
            if v1:
                return tmp
            else:
                return (1-tmp)

    def values(self,values):
        res = []
        
        #Burglary all possible values
        if "Bt"	in values:
            res.append(True)
        elif "Bf" in values:
            res.append(False)
        else:
            res.append(None)
        
        #Earthquake all possible values
        if "Et"	in values:
            res.append(True)
        elif "Ef" in values:
            res.append(False)
        else:
            res.append(None)

        #Alarm all possible values
        if "At"	in values:
            res.append(True)
        elif "Af" in values:
            res.append(False)
        else:
            res.append(None)
        
        #JohnCalls all possible values
        if "Jt"	in values:
            res.append(True)
        elif "Jf" in values:
            res.append(False)
        else:
            res.append(None)
        
        #MaryCalls all possible values
        if "Mt"	in values:
            res.append(True)
        elif "Mf" in values:
            res.append(False)
        else:
            res.append(None)
        return res

    def computeProbability(self, b, e, a, j, m):
        result = (self.probabilityDistribution("B",b,None,None) * 
                self.probabilityDistribution("E",e,None,None) * 
                self.probabilityDistribution("A|B,E",a,b,e) * 
                self.probabilityDistribution("J|A",j,a,None) * 
                self.probabilityDistribution("M|A",m,a,None))
        return result

    def numerator(self,v):
        if not None in v:
                return self.computeProbability(v[0],v[1],v[2],v[3],v[4])
        else:
            noIndex = v.index(None)
            var = list(v)
            var[noIndex] = True
            val1 = self.numerator(var)
            var[noIndex] = False
            val2 = self.numerator(var)
            return (val1 + val2)

#isGiven = False
observation = []
userInput = []
given = 0
print("Input: ")
for x in range(1,len(argv)):
    print(argv[x])
    if argv[x] == "given":
        #isGiven = True
        given = 1
        continue
    
    userInput.append(argv[x])
    if given:
        observation.append(argv[x])

bnet = BayesianNetwork()

if userInput:
	numerator = bnet.numerator(bnet.values(userInput))
	if observation:
		denominator = bnet.numerator(bnet.values(observation))
	else:
		denominator = 1
	print("\nProbability = %.10f" %(numerator/denominator))
else:
	print("Invalid input entered")
    