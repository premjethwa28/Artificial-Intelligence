# -*- coding: utf-8 -*-
"""

@author: Prem Atul Jethwa
UTA id: 1001861810
Programming language used: Python 3.9.6

"""

import sys

#Given the probabilities of Cherry, Lime and Bags
Cherry_Probability = [1, 0.75, 0.5, 0.25, 0]
Lime_Probability = [0, 0.25, 0.5, 0.75, 1]
H_Prior_Probability = [0.1, 0.2, 0.4, 0.2, 0.1]

#Open the result.txt file in write mode
try:
    result_file = open("result.txt", 'w')
except Exception:
    print ('Unable to create the result.txt file!')

#Function to calculate the posterior probability using the formula
def Next_H_Prob(obs_prob, h_prob, last_obs_prob):
    result = [0, 0, 0, 0, 0]
    for index in range(5):
        result[index] = ((obs_prob[index] * h_prob[index]) / last_obs_prob)
    return result

#Function to calculate the probability after the observation
def Next_Obs_Prob(observed_prob, h_prob):
    result = 0
    for index in range(5):
        result += (observed_prob[index] * h_prob[index])
    return result

#Function to calculate the probability that next object selected is Cherry and Lime 
def Check_Obs_Sequence(obs_sequence, h_prob, lime_prior_prob, cherry_prior_prob):
    for val in range(len(obs_sequence)):
        
        if obs_sequence[val] == 'C':
            if (val + 1) == 1:
                h_prob = [0.1, 0.2, 0.4, 0.2, 0.1]
            h_prob = Next_H_Prob(Cherry_Probability, h_prob, cherry_prior_prob)
            cherry_prior_prob = Next_Obs_Prob(Cherry_Probability, h_prob)
            lime_prior_prob = 1 - cherry_prior_prob

            result_file.write('After Observation %d = %s:\r\n' % (val, obs_sequence[val]))

            index = 0
            while index < 5:
                result_file.write('P(h%d | Q) = %8.5f\r' % (index + 1, h_prob[index]))
                index += 1

            result_file.write('\nProbability that the next candy we pick will be C, given Q: %8.9f\r' %  cherry_prior_prob)
            result_file.write('Probability that the next candy we pick will be L, given Q: %8.9f\r\n' %  lime_prior_prob)

        else:
            if (val + 1) == 1:
                h_prob = [0.1, 0.2, 0.4, 0.2, 0.1]
            h_prob = Next_H_Prob(Lime_Probability, h_prob, lime_prior_prob)
            lime_prior_prob = Next_Obs_Prob(Lime_Probability, h_prob)
            cherry_prior_prob = 1 - lime_prior_prob
            
            result_file.write('After Observation %d = %s:\r\n' % (val, obs_sequence[val]))

            index = 0
            while index < 5:
                result_file.write('P(h%d | Q) = %8.5f\r' % (index + 1, h_prob[index]))
                index += 1

            result_file.write('\nProbability that the next candy we pick will be C, given Q: %8.9f\r' %  cherry_prior_prob)
            result_file.write('Probability that the next candy we pick will be L, given Q: %8.9f\r\n' %  lime_prior_prob)


def Write_To_File(argv):
    if (len(argv) > 1):
        obs_sequence = argv[1]
        cherry_prior_prob = Next_Obs_Prob(Cherry_Probability, H_Prior_Probability)
        lime_prior_prob = 1 - cherry_prior_prob
        h_prob = [0, 0, 0, 0, 0]

        result_file.write('Observation sequence Q: %s\r\n' % (obs_sequence))
        result_file.write('Length of Q: %s\r\n' % str(len(obs_sequence)))
        Check_Obs_Sequence(obs_sequence, h_prob, lime_prior_prob, cherry_prior_prob)

    else:
        result_file.write('No observation sequence Q yet : \r\n')

        cherry_prior_prob = Next_Obs_Prob(Cherry_Probability, H_Prior_Probability)
        lime_prior_prob = 1 - cherry_prior_prob

        result_file.write(
            '\nProbability that the next candy we pick will be C, given there is no observation: %8.9f\r' % (cherry_prior_prob))
        result_file.write(
            'Probability that the next candy we pick will be L, given there is no observation: %8.9f\r\n' % (lime_prior_prob))

    result_file.close()
    print ('Check result.txt file for output of sequence entered!')

# Main function starts from here
def main(argv):
    # To make sure we have sufficient command-line arguments
    if len(argv) > 2:
        print('Two command-line arguments are needed:')
        print('Usage: %s [observation-sequence]' % argv[0])
        print('or: %s' % argv[0])
        sys.exit(0)
    Write_To_File(argv)


if __name__ == '__main__':
    main(sys.argv)
    
