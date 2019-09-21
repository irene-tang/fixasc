import sys, os, glob
import csv
import numpy as np

# declare output path
# INPUT_FOLDER =  "../data/eyedry_output/graphs5/original_eyedry_output_5/*IXS"
# OUTPUT_FOLDER = "../data/eyedry_output/graphs5/edited_eyedry_output_5/"
INPUT_FOLDER = sys.argv[1] + '/*IXS'
OUTPUT_FOLDER = sys.argv[2] + '/'

FILES_TO_PROCESS = [f for f in glob.glob(INPUT_FOLDER)]

# check for correct commandline args
if len(sys.argv) != 3:
    print('incorrect usage: python3 edit_cond.py [INPUT_FOLDER] [OUTPUT_FOLDER]')
    exit(-1)

# get name of file
# inputFilename = sys.argv[1]

for inputFilename in FILES_TO_PROCESS:
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

    # save it to the output file
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    outputFilename = OUTPUT_FOLDER + inputFilename.rsplit('/',1)[-1] + '_edited'
    print(outputFilename)

    with open(outputFilename, 'w+') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(data)

    # close files
    readFile.close()
    writeFile.close()
