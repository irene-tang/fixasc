import glob
import subprocess

"""
Runs makeasc.py for every .asc file in the directory that is not already processed
"""
print('running makeasc.py', end='')

file_list = glob.glob('../data/original_asc/*.asc')
# print (file_list)

for asc in file_list:
    # print asc
    p = subprocess.call(['python', 'makeasc/makeasc.py', asc])
    print('.', end='', flush=True)

"""
Runs question_acc.py
"""
print('\nrunning question_acc.py')

# p = subprocess.call(['python3', 'copyRoboDoc_and_utils/copy_question_acc/copy_question_acc_copy.py', 'copyRoboDoc_and_utils/'])

"""
Runs scripter.pl
"""


"""
Runs make_cnt.py
"""


"""
Runs Robodoc.py
"""
