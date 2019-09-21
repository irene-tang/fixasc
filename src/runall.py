import os
import glob
import subprocess
import shutil

"""
Delete all of the subfolders (and their contents) in data/ except for data/original_asc/ or data/eyedry_output/
Then re-create them as empty folders
"""

paths = ["../data/fix_aligned_asc", "../data/reformatted_asc", "../data/question_acc_output", "../data/robodoc_output", "../data/scripter_output"]

for path in paths:
    try:
        shutil.rmtree(path)
    except OSError:
        print ("Deletion of the directory %s failed" % path)
    else:
        print ("Successfully deleted the directory %s " % path)

print()

for path in paths:
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)


"""
Runs reformat_asc.py
"""
print('\n==========\nrunning reformat_asc\n==========\n', end='')

file_list = glob.glob('../data/original_asc/*.asc')

for asc in file_list:
    p = subprocess.call(['python3', 'reformat_asc/reformat_asc.py', asc])
    print('.', end='', flush=True)

print()

"""
Runs question_acc.py
"""
print('\n==========\nrunning question_acc\n==========')

p = subprocess.call(['python3', 'copy_question_acc/copy_question_acc.py', 'copy_Robodoc/limerick_parameters.txt'])

"""
Runs remove_participants_question_acc.py
"""
print('\n==========\nrunning remove_participants\n==========')

p = subprocess.call(['python3', 'copy_question_acc/remove_participants_question_acc.py'])

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
