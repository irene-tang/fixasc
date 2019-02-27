import glob
import subprocess

"""
Runs make_new_asc.py
"""
print('==========\nrunning make_new_asc\n==========\n', end='')

file_list = glob.glob('../data/original_asc/*.asc')

for asc in file_list:
    p = subprocess.call(['python', 'make_new_asc/make_new_asc.py', asc])
    print('.', end='', flush=True)

print()

"""
Runs question_acc.py
"""
print('\n==========\nrunning question_acc\n==========')

p = subprocess.call(['python3', 'copy_question_acc/copy_question_acc.py', 'copy_Robodoc/limerick_parameters.txt'])

"""
Runs scripter2.pl
"""
print('\n==========\nrunning scripter2\n==========')

p = subprocess.call(['perl', 'copy_Scripter2/copy_scripter2.pl'])

"""
Runs make_cnt.py
"""
print('\n==========\nrunning make_cnt\n==========')

p = subprocess.call(['python3', 'copy_make_cnt/copy_make_cnt.py'])

"""
Runs fix_align.R
"""
print('\n==========\nrunning fix_align\n==========')

p = subprocess.call(['Rscript', 'copy_fix_align/copy_fix_align_v0p92.R'])

"""
Runs Robodoc.py
"""
print('\n==========\nrunning robodoc.py\n==========')

p = subprocess.call(['python3', 'copy_Robodoc/copy_Robodoc.py', 'copy_Robodoc/limerick_parameters.txt'])
