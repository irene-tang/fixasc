import glob
import subprocess

"""
Runs makeasc.py for every .asc file in the directory that is not already processed
"""
print('running makeasc.py')

file_list = glob.glob('../data/original_asc/*.asc')
# print (file_list)

for asc in file_list:
    # print asc
    p = subprocess.call(['python', 'makeasc.py', asc])

# """
# Runs question_acc.py
# """
# print('running question_acc.py')
#
# p = subprocess.call(['python3', '../data/processed_asc/question_acc_copy.py', '../data/processed_asc/limerick_parameters.txt' ])
