import glob
import subprocess

"""
Runs makeasc.py for every .asc file in the directory that is not already processed
"""

file_list = glob.glob('data/original_asc/*.asc')
print (file_list)

for asc in file_list:
    p = subprocess.call(['python', 'makeasc.py', asc])
