import glob
import subprocess

# """
# Runs makeasc.py
# """
# print('\nrunning makeasc', end='')
#
# file_list = glob.glob('../data/original_asc/*.asc')
#
# for asc in file_list:
#     p = subprocess.call(['python', 'makeasc/makeasc.py', asc])
#     print('.', end='', flush=True)
#
# print()
#
# """
# Runs question_acc.py
# """
# print('\nrunning question_acc')
#
# p = subprocess.call(['python3', 'copy_question_acc/copy_question_acc.py', 'copy_Robodoc/limerick_parameters.txt'])
#
# """
# Runs scripter2.pl
# """
# print('\nrunning scripter2')
#
# p = subprocess.call(['perl', 'copy_Scripter2/copy_scripter2.pl'])
#
# # TODO: automatic stdin
# # copy_Scripter2/input_to_scripter.txt
# # ../data/scripter/output_from_scripter.script
#
# """
# Runs make_cnt.py
# """
# print('\nrunning make_cnt')
#
# p = subprocess.call(['python3', 'copy_make_cnt/copy_make_cnt.py'])
#
# # TODO: automatic stdin
# # ../data/scripter/output_from_scripter.script
# # ^
# # 1
# # 4
#
# """
# Runs fix_align.R
# """
# print('\nrunning fix_align')
#
# p = subprocess.call(['Rscript', 'copy_fix_align/copy_fix_align_v0p92.R'])

# TODO:
# get fixalign  to  run , make it so that don't have to press return every time, process rest of files
# can we reverse the makeasc to view in dataviewer? ("don't spend more than two hours on this")
# run new stuff with robodoc
# data anal
# un: Experimenter
# pw: none

"""
Runs Robodoc.py
"""
print('\nrunning robodoc.py')

p = subprocess.call(['python3', 'copy_Robodoc/copy_Robodoc.py', 'copy_Robodoc/limerick_parameters.txt'])
