import sys, os
import csv
import numpy as np

# declare output path
OUTPUT_PATH = "../data/eyedry/edited_originals/"
FILES_TO_PROCESS = [
    "../data/eyedry/originals/firstPassIXS",
    "../data/eyedry/originals/goPastIXS",
    "../data/eyedry/originals/probFixationIXS",
    "../data/eyedry/originals/probRegressionIXS",
    "../data/eyedry/originals/firstFixationReg3IXS",
]

# check for correct commandline args
# if len(sys.argv) != 2:
#     print('incorrect usage: python3 dataanal.py [file]')

# get name of file
# inputFilename = sys.argv[1]

for inputFilename in FILES_TO_PROCESS:
    print(inputFilename)
    # enter data as list
    with open(inputFilename, newline='') as readFile:
        data = list(csv.reader(readFile))

    # convert to numpy array
    # data = np.asarray(data)

    # perform our conversions
    count = 0
    num_rows = len(data)
    num_cols = len(data[0])
    for i in range(len(data)):
        for j in range(len(data[0])):
            # replace missing values with 0
            if data[i][j] == '':
                data[i][j] = '0'
            # edit the condition in 4th column
            if j == 3 and data[i][j] == '1':
                data[i][j] = 'match_tap'
            elif j == 3 and data[i][j] == '2':
                data[i][j] = 'match_this'
            elif j == 3 and data[i][j] == '3':
                data[i][j] = 'clash_tap'
            elif j == 3 and data[i][j] == '4':
                data[i][j] = 'clash_this'
            # if condition value is zero but sequence value is non-zero,
            # replace the sequence value with 0
            elif j == 3 and data[i][j] == '0' and data[i][0] != 0:
                data[i][0] = 0
                count+=1
    print(count)


    # save it to the output file
    outputFilename = OUTPUT_PATH + inputFilename.rsplit('/',1)[-1] + '_edited'
    print(outputFilename)

    with open(outputFilename, 'w+') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(data)

    # close files
    readFile.close()
    writeFile.close()