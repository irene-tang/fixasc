import sys

"""
inputs:
    subjx.asc
    IA_2.ias ... IA101.ias
"""
original_asc = sys.argv[1]
new_asc = sys.argv[2]

buffer = []
header = False
cal1 = False

freelines = 0 # number of following lines to include with no questions asked

infile = open(original_asc, 'r')
line = ''

count = 0

def get_next_line():
    line = infile.readline()
    if not line:
        return False
    return True

def write_to_outfile():
    with open(new_asc, 'w') as outfile:
        for x in buffer:
            outfile.write(x)
    outfile.close()

def read_ias_word(line, timestamp):
    line = 'COPY OF aoi/' + line.split('/')[-1].strip()
    iasfile = open(line, 'r')

    buffer_slice = []
    word_number = 0
    line_number = 0

    buffer_slice.append('MSG ' + str(timestamp) + ' DISPLAY TEXT 1\n')

    while True:
        line = iasfile.readline()

        if not line:
            return buffer_slice

        line = line.split()

        word = line[-1]
        x_start = int(line[3])
        x_end = int(line[5])
        y_start = int(line[4])
        y_end = int(line[6])

        sequence = int(line[2])
        if sequence == 1:
            line_number += 1
            word_number = 0

        buffer_slice.append('MSG ' + str(timestamp) + ' REGION CHAR ' + str(word_number) + ' ' + str(line_number) + ' ' + word + ' ' + str(x_start) + ' ' + str(y_start) + ' ' + str(x_end) + ' ' + str(y_end) + '\n')
        buffer_slice.append('MSG ' + str(timestamp) + ' DELAY 1 MS' + '\n')

        timestamp += 1
        word_number += 1

def read_ias_letter(line, timestamp):
    line = 'COPY OF aoi/' + line.split('/')[-1].strip()
    iasfile = open(line, 'r')

    buffer_slice = []
    char_number = 0
    line_number = 0

    buffer_slice.append('MSG ' + str(timestamp) + ' DISPLAY TEXT 1\n')

    while True:
        line = iasfile.readline()

        if not line:
            return buffer_slice

        line = line.split()
        word = line[-1]
        x_start = int(line[3])
        x_end = int(line[5])
        y_start = int(line[4])
        y_end = int(line[6])
        x_step = (x_end - x_start)/(len(word) + 1)

        sequence = int(line[2])
        if sequence == 1:
            line_number += 1
            char_number = 0

        # FIXME: spacing
        for i in range(len(word)+1):
            if i == len(word):
                c = ' '
                x = x_end
            else:
                c = word[i]
                x = x_start + x_step

            buffer_slice.append('MSG ' + str(timestamp) + ' REGION CHAR ' + str(char_number) + ' ' + str(line_number) + ' ' + c + ' ' + str(x_start) + ' ' + str(y_start) + ' ' + str(x) + ' ' + str(y_end) + '\n')
            buffer_slice.append('MSG ' + str(timestamp) + ' DELAY 1 MS' + '\n')
            x_start = x_start + x_step

            timestamp += 1
            char_number += 1

while True:
    # get the next line
    line = infile.readline()
    # stop looping at end of file
    if not line:
        break

    if freelines:
        buffer.append(line)
        freelines -= 1
        continue # skips remainder of this iteration

    ############################################
    ### METADATA, CALIBRATION, VALIDATION, ETC.
    ############################################

    # keep all blank lines
    if line == '':
        buffer.append(line)
    # keep all comments, which begin with **
    elif line[0:2] == '**':
        buffer.append(line)
    # keep the >>>> calibration header line thing
    elif line[0:4] == '>>>>':
        buffer.append(line)
    # keep display coords info (should be just once)
    elif 'MSG' in line and 'DISPLAY_COORDS' in line:
        buffer.append(line.replace('DISPLAY_COORDS', 'DISPLAY COORDS'))
    # keep calibration info
    elif 'MSG' in line and '!CAL' in line:
        buffer.append(line)
        # also keep the line(s) following these
        if 'eye check box' in line:
            freelines += 1
        elif 'href cal range' in line:
            freelines += 1
        elif 'Cal coeff' in line:
            freelines += 2
        elif 'Quadrant center' in line: # not sure why they needed new line for this
            freelines += 1
        elif 'Corner correction' in line:
            freelines += 4
    # keep validation info
    elif 'MSG' in line and 'VALIDATE' in line:
        buffer.append(line)
    # keep this stuff to i guess
    elif 'MSG' in line and 'ERROR MESSAGES LOST' in line:
        buffer.append(line)


    ############################################
    ### TRIALS #################################
    ############################################
    # NOTE: ordering of !MODE RECORD and START

    elif 'MSG' in line and 'TRIALID' in line:
        # TODO: rename trialid
        buffer.append(line)

        # TODO .ias stuff goes here
        buffer_holder_index = len(buffer)

        line = infile.readline()
        if not line:
            break

        # then read in the following info
        done = False
        while not done:
            if 'INPUT' in line:
                buffer.append(line)
            elif 'MSG' in line and (\
                    'DRIFTCORRECT' in line or \
                    'RECCFG' in line or \
                    'ELCLCFG' in line or \
                    'GAZE_COORDS' in line or \
                    'THRESHOLDS' in line or \
                    'ELCL_WINDOW_SIZES' in line or \
                    'CAMERA_LENS_FOCAL_LENGTH' in line or \
                    'PUPIL_DATA_TYPE' in line or \
                    'ELCL_PROC' in line or \
                    'ELCL_PCR_PARAM' in line):
                buffer.append(line)
            elif 'START' in line or \
                    'PRESCALER' in line or \
                    'VPRESCALER' in line or \
                    'PUPIL' in line or \
                    ('EVENTS' in line and 'GAZE' in line):
                buffer.append(line)
            elif 'MSG' in line and '!MODE RECORD' in line:
                buffer.append(line)
                done = True
            else: # error
                print "ERROR IN LINE: " + line
                exit(-1)

            line = infile.readline()
            if not line:
                break

        # then read in saccads, fizations, blinkings
        done = False
        while not done:
            #FIXME trying to just get the ones betwween secondarytask while reading limerick?
            if 'SFIX' in line or \
                    'EFIX' in line or \
                    'SSACC' in line or \
                    'ESACC' in line or \
                    'SBLINK' in line or \
                    'EBLINK' in line:
                buffer.append(line)

            elif 'BUTTON' in line:
                buffer.append(line)

            elif 'MSG' in line and 'end_trial' in line:
                buffer.append('ENDTRIALFORMATTING\n')
                done = True

            elif 'IAREA FILE' in line:
                timestamp = int(line.split()[1])
                ias_info = read_ias_word(line, timestamp)
                buffer[buffer_holder_index:buffer_holder_index] = ias_info

            line = infile.readline()
            if not line:
                break



    ############################################
    ### UNKNOWN STUFF, LOST INFOMORMATION ######
    ############################################

    else:
        if 'TRIAL_VAR' not in line:
            count += 1
            print line

write_to_outfile()
print count

infile.close()
