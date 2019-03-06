import sys, os
import csv
import numpy as np

# check for correct commandline args
if len(sys.argv) != 2:
    print('incorrect usage: python3 dataanal.py [file]')

# get name of file
inputFilename = sys.argv[1]

# enter data as list
with open(inputFilename, newline='') as readFile:
    data = list(csv.reader(readFile))

# convert to numpy array
# data = np.asarray(data)

# perform our conversions
num_rows = len(data)
num_cols = len(data[0])
for i,row in enumerate(data):
    for j, col in enumerate(row):
        # replace missing values with 0
        if data[i][j] == '':
            data[i][j] = '0'
        # edit the condition in 4th column
        elif j == 3 and data[i][j] == '1':
            data[i][j] = 'match_tap'
        elif j == 3 and data[i][j] == '2':
            data[i][j] = 'match_this'
        elif j == 3 and data[i][j] == '3':
            data[i][j] = 'clash_tap'
        elif j == 3 and data[i][j] == '4':
            data[i][j] = 'clash_this'

# save it to the output file
outputFilename = inputFilename.split('.')[0] + '_edited'
with open(outputFilename, 'w+') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(data)

# close files
readFile.close()
writeFile.close()