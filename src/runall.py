import glob
import subprocess

"""
Runs makeasc.py for every .asc file in the directory that is not already processed
"""
print('\nrunning makeasc.py', end='')

file_list = glob.glob('../data/original_asc/*.asc')

for asc in file_list:
    p = subprocess.call(['python', 'makeasc/makeasc.py', asc])
    print('.', end='', flush=True)

print()

"""
Runs question_acc.py
"""
print('\nrunning question_acc.py')

p = subprocess.call(['python3', 'copy_question_acc/copy_question_acc.py', 'copy_Robodoc/limerick_parameters.txt'])

"""
Runs scripter2.pl
"""
print('\nrunning scripter.pl')

p = subprocess.call(['perl', 'copy_Scripter2/copy_scripter2.pl'])

# TODO: automatic stdin
# copy_Scripter2/input_to_scripter.txt
# ../data/scripter/output_from_scripter.script

"""
Runs make_cnt.py
"""
print('\nrunning make_cnt.py')

p = subprocess.call(['python3', 'copy_make_cnt/copy_make_cnt.py'])

# TODO: automatic stdin
# ../data/scripter/output_from_scripter.script
# ^
# 1
# 2

"""
Runs Robodoc.py
"""
print('\nrunning robodoc.py')

p = subprocess.call(['python3', 'copy_Robodoc/copy_Robodoc.py', 'copy_Robodoc/limerick_parameters.txt'])
