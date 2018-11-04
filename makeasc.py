import sys

def write_to_outfile(new_asc, buffer):
    """
    Writes the contentes of the buffer list into the new_asc output file
    """
    with open(new_asc, 'w') as outfile:
        for x in buffer:
            outfile.write(x)
    outfile.close()

def read_ias_word(line, timestamp, ias_folder):
    """
    Reads the contentes of the .ias file word-by-word into a buffer
    """
    # format the path to the folder where the .ias files are stored
    line = ias_folder + line.split('/')[-1].strip()
    iasfile = open(line, 'r')

    # buffer to hold the lines before they get combined into
    buffer_slice = []
    # position of the current word on the current line
    word_number = 0
    # line number that the current word appears on
    line_number = 0

    # include this for each limerick
    buffer_slice.append('MSG ' + str(timestamp) + ' DISPLAY TEXT 1\n')

    while True:
        # get the next line
        line = iasfile.readline()

        # return the buffer when the end of the .ias file is reached
        if not line:
            return buffer_slice

        # decompose the line
        line = line.split()
        word = line[-1]
        x_start = int(line[3])
        x_end = int(line[5])
        y_start = int(line[4])
        y_end = int(line[6])
        sequence = int(line[2])

        # increment the line number when appropriate
        if sequence == 1:
            line_number += 1
            word_number = 0

        # add to buffer
        buffer_slice.append('MSG ' + str(timestamp) + ' REGION CHAR ' + str(word_number) + ' ' + str(line_number) + ' ' + word + ' ' + str(x_start) + ' ' + str(y_start) + ' ' + str(x_end) + ' ' + str(y_end) + '\n')
        buffer_slice.append('MSG ' + str(timestamp) + ' DELAY 1 MS' + '\n')

        # increment timestamp and word_number
        timestamp += 1
        word_number += 1

def read_ias_letter(line, timestamp, ias_folder):
    """
    Reads the contentes of the .ias file letter-by-letter into a buffer
    (This method is not currently being used)
    """
    # format the path to the folder where the .ias files are stored
    line = ias_folder + line.split('/')[-1].strip()
    iasfile = open(line, 'r')

    # buffer to hold the lines before they get combined into
    buffer_slice = []
    # position of the current character on the current line
    char_number = 0
    # line number that the current word appears on
    line_number = 0

    # include this for each limerick
    buffer_slice.append('MSG ' + str(timestamp) + ' DISPLAY TEXT 1\n')

    while True:
        # get the next line
        line = iasfile.readline()

        # return the buffer when the end of the .ias file is reached
        if not line:
            return buffer_slice

        # decompose the line
        line = line.split()
        word = line[-1]
        x_start = int(line[3])
        x_end = int(line[5])
        y_start = int(line[4])
        y_end = int(line[6])
        x_step = (x_end - x_start)/(len(word) + 1)
        sequence = int(line[2])

        # increment the line number when appropriate
        if sequence == 1:
            line_number += 1
            char_number = 0

        # FIXME: spacing
        # evenly slice up the given coordinates across each character
        for i in range(len(word)+1):
            if i == len(word):
                c = ' '
                x = x_end
            else:
                c = word[i]
                x = x_start + x_step

            # add to buffer
            buffer_slice.append('MSG ' + str(timestamp) + ' REGION CHAR ' + str(char_number) + ' ' + str(line_number) + ' ' + c + ' ' + str(x_start) + ' ' + str(y_start) + ' ' + str(x) + ' ' + str(y_end) + '\n')
            buffer_slice.append('MSG ' + str(timestamp) + ' DELAY 1 MS' + '\n')
            x_start = x_start + x_step

            # increment timestamp and char_number
            timestamp += 1
            char_number += 1

def main():
    """
    Converts the .asc files produced by ExperimentBuilder into a format that can be
    parsed by UMass Eyetracking clean-up software
    """
    # check for correct command-line inputs
    if len(sys.argv) != 4:
        print "usage: python makeasc.py [original_asc input] [new_asc output] [ias_folder]"
        exit(-1)

    # the original asc input file
    original_asc = sys.argv[1]
    # the desired asc output file
    new_asc = sys.argv[2]
    # the folder where .ias files are stored
    ias_folder = sys.argv[3]
    # open the input file
    infile = open(original_asc, 'r')

    # temporary buffer to store lines before writing them to new_asc file at the end
    buffer = []
    # number of following lines to include with no questions asked
    freelines = 0
    # the current line that is being examined
    line = ''

    # trash variables to count how many lines of unknown info we have thrown out
    count = 0
    lostcount = 0

    # info about the trial
    dirtytype = 0
    rhymetype = 0
    clashtype = 0

    while True:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # lines to include without question
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
        # keep the >>>> calibration header line
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
        # keep drift correction info
        elif 'MSG' in line and 'DRIFTCORRECT' in line:
            buffer.append(line)


        ############################################
        ### TRIALS #################################
        ############################################
        # NOTE: ordering of !MODE RECORD and START seems to be inconsistent sometimes
        # parsing info for one trail
        elif 'MSG' in line and 'TRIALID' in line:
            # TODO: rename trialid
            #include this line
            buffer_holder_index_trialid = len(buffer)
            print line
            # buffer.append(line)

            # placeholder index for the .ias stuff that will go here
            buffer_holder_index_ias = len(buffer)

            # get the next line
            line = infile.readline()
            # stop looping if the end of file is reached
            if not line:
                break

            # then read in camera info
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

                # get the next line
                line = infile.readline()
                # stop looping if the end of file is reached
                if not line:
                    break

            # then read in saccads, fixations, blinkings info
            done = False
            while not done:
                if 'SFIX' in line or \
                        'EFIX' in line or \
                        'SSACC' in line or \
                        'ESACC' in line or \
                        'SBLINK' in line or \
                        'EBLINK' in line:
                    buffer.append(line)

                elif 'BUTTON' in line:
                    buffer.append(line)

                # stop looping at the sight of this
                elif 'MSG' in line and 'end_trial' in line:
                    timestamp = str(line.split()[1])
                    buffer.append('MSG ' + timestamp + ' DISPLAY OFF\n')
                    done = True

                # insert info from .ias file into the stored buffer_holder_index_ias
                elif 'IAREA FILE' in line:
                    timestamp = int(line.split()[1])
                    ias_info = read_ias_word(line, timestamp, ias_folder)
                    buffer[buffer_holder_index_ias:buffer_holder_index_ias] = ias_info

                # get the next line
                line = infile.readline()
                # stop looking if the end of the file is reached
                if not line:
                    break

        ############################################
        ### FOLLOWUP ###############################
        ############################################
        # parsing info for the followup question
        elif 'MSG' in line and 'SHOW FOLLOWUP QUESTION' in line:
            # include this line
            buffer.append(line)

            done = False
            while not done:
                # get the next line
                line = infile.readline()
                # stop looking if the end of the file is reached
                if not line:
                    break
                # stop looping at the sight of this
                if 'END' in line and 'EVENTS' in line and 'RES' in line:
                    done = True
                # include the current line
                buffer.append(line)

        ############################################
        ### UNKNOWN STUFF, LOST INFOMORMATION ######
        ############################################

        # convert this line to TRIAL OK
        elif 'MSG' in line and 'TRIAL_RESULT' in line and '0' in line:
            timestamp = str(line.split()[1])
            buffer.append('MSG ' + timestamp + ' TRIAL OK\n')

        # revisit TRIALID for this kind of trial naming convention
        # elif 'MSG' in line and 'TRIAL_VAR' in line and 'DirtyType' in line:
            # print "DirtyType" # NOTE testing
            # skip

        elif 'MSG' in line and 'TRIAL_VAR' in line and 'RhymeType' in line:
        #     # NOTE testing
            new_trialid = 'DNEWTRIALID\n'
            print buffer[buffer_holder_index_trialid]
            buffer[buffer_holder_index_trialid:buffer_holder_index_trialid] = new_trialid
            print buffer[buffer_holder_index_trialid]

        # stuff that gets thrown out by this script
        else:
            if 'TRIAL_VAR' not in line and \
                'TRIAL_RESULT' not in line and \
                'BUTTON' not in line and \
                'SFIX' not in line and \
                'EFIX' not in line and \
                'SSACC' not in line and \
                'ESACC' not in line and \
                'prepare_sequence' not in line:
                count += 1
                print line
            else:
                lostcount += 1

    # write the contents of the buffer to the output file
    write_to_outfile(new_asc, buffer)
    # print the trash variables to count how many lines of unknow info we threw out
    print count
    print lostcount
    # close the input file
    infile.close()

# run main()
main()
