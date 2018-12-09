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


# TODO: actually letter by letter
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

def check_args():
    """
    checks for correct command-line inputs
    returns file stuff from the command line inputs
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

    return (original_asc, new_asc, ias_folder)

def main():
    """
    Converts the .asc files produced by ExperimentBuilder into a format that can be
    parsed by UMass Eyetracking clean-up software
    """

    # check for correct command-line inputs, and initialize variables
    (original_asc, new_asc, ias_folder) = check_args()

    # open the input file, if possible
    try:
        infile = open(original_asc, 'r')
    except IOError:
        print("original_asc file not found or path is incorrect")
        exit(-1)

    # temporary buffer to store lines before writing them to new_asc file at the end
    buffer = []

    # number of following lines to include with no questions asked
    freelines = 0

    # the current line that is being examined
    line = ''

    ############################################
    ### METADATA, CALIBRATION, AND VALIDATION ##
    ############################################

    # get the conversion metadata
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if line.strip() == '**':
            done = True
            buffer.append(line)
        # keep all blank lines
        elif line == '':
            buffer.append(line)
        # keep all comments, which begin with **
        elif line[0:2] == '**':
            buffer.append(line)

    # get the few lines before calibration info
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and '!CAL' in line:
            done = True
            buffer.append(line)
        # keep display coords info (should be just once)
        elif 'MSG' in line and 'DISPLAY_COORDS' in line:
            buffer.append(line.replace('DISPLAY_COORDS', 'DISPLAY COORDS'))
        # TODO: retrace_interval versus framerarte
        elif 'RETRACE_INTERVAL' in line:
            pass
        # keep any input info
        elif 'INPUT' in line:
            buffer.append(line)

    # get the calibration and info
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and 'TRIALID' in line:
            done = True
            # do not append here, will deal with this line in the next section (which  is trials)
        # basically keep everything else in the calibration section, until the exit state is reached
        else:
            # buffer.append(line)
            pass

        # # keep the >>>> calibration header line
        # if line.strip()[0:4] == '>>>>':
            # buffer.append(line)

        # # keep calibration info
        # elif 'MSG' in line and '!CAL' in line:
        #     buffer.append(line)
        #     # also keep the line(s) following these
        #     if 'eye check box' in line:
        #         freelines += 1
        #     elif 'href cal range' in line:
        #         freelines += 1
        #     elif 'Cal coeff' in line:
        #         freelines += 2
        #     elif 'Quadrant center' in line: # not sure why they needed new line for this
        #         freelines += 1
        #     elif 'Corner correction' in line:
        #         freelines += 4
        # # keep validation info
        # elif 'MSG' in line and 'VALIDATE' in line:
        #     buffer.append(line)
        # # keep this stuff to i guess
        # elif 'MSG' in line and 'ERROR MESSAGES LOST' in line:
        #     buffer.append(line)
        # # keep drift correction info
        # elif 'MSG' in line and 'DRIFTCORRECT' in line:
        #     buffer.append(line)

    ############################################
    ### PRACTICE TRIALS ########################
    ############################################
    # first deal with the abandoned TRIALID from the current line
    current_trialid = line # TODO repair this for the first practice lim
    buffer.append(current_trialid)

    #TODO add practice ias info here

    # get camera info -- TODO possibly might need some re ordering of certain lines since they don't line up exactly
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit sate
        if 'MSG' in line and 'str("START PRACTICE LIMERICK' in line:
            done  = True
        # basically get everything up until the actual eye movement data
        else:
            buffer.append(line)
            # pass

    # read limerick 1 -- TODO need to look into segregating the limerick from the question
    # for now just keep all practice trial info, unparsed
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and 'str("END PRACTICE LIMERICKS AND BEGIN REAL TRIALS")' in line:
            done = True
            buffer.append(line)
        else:
            # buffer.append(line)
            pass

    ############################################
    ### REAL TRIALS ############################
    ############################################

    # declare variables here for scoping
    subtypeid = ''
    clashtype = ''
    secondarytask = ''
    iarea = ''
    old_trialid = ''
    buffer_holder_index_trialid = -1
    buffer_holder_index_ias = -1


    # skip the extra trial metadata info here
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and 'prepare_sequence' in line:
            done = True

    # parsing info for one trial
    # trigger: prepare_sequence
    # skip to where it says TRIALID number -- should just be the next line
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and 'TRIALID' in line:
            done = True
            old_trialid = line
            buffer_holder_index_trialid = len(buffer)
            print str(old_trialid) + "dd"
            print str(buffer_holder_index_trialid) + "AA"

        # placeholder index for the .ias stuff that will go here
        buffer_holder_index_ias = len(buffer)

    # read in camera info
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if '!MODE RECORD' in line:
            done = True
            buffer.append(line)
        else:
            buffer.append(line)

    # skip the dual-task instructions screen
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and 'SHOW LIMERICK' in line:
            done = True
        elif 'IAREA FILE' in line:
            iarea = line

    # get the eye-movements for viewing the limerick
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and 'STOP SECONDARY TASK' in line:
            done = True
            timestamp = str(line.split()[1])
            buffer.append('MSG ' + timestamp + ' DISPLAY OFF\n')
        # get eye movements
        elif 'SFIX' in line or \
                'EFIX' in line or \
                'SSACC' in line or \
                'ESACC' in line or \
                'SBLINK' in line or \
                'EBLINK' in line or \
                'BUTTON' in line:
            buffer.append(line)
        else: # error?
            print "NOT FOUND WHILE PARSING LIMERICK EYE-MOEMENTS: " + line

    # skip the dual-task end instructions screen (and the other trial metadata)
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'MSG' in line and 'SHOW FOLLOWUP QUESTION' in line:
            done = True

    # make new trial for the question
    # - add TRILID
    # - add camera info
    # add eye-movements
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'END' in line and 'EVENTS' in line and 'RES' in line:
            done = True
            buffer.append(line) # amend this by converting to TRIAL OK ? TODO
        # get eye movements
        elif 'SFIX' in line or \
                'EFIX' in line or \
                'SSACC' in line or \
                'ESACC' in line or \
                'SBLINK' in line or \
                'EBLINK' in line or \
                'BUTTON' in line:
            buffer.append(line)
        else: # error?
            print "NOT FOUND WHILE PARSING QUESTION EYE-MOEMENTS: " + line

    # parse rest for trial metadata
    done = False
    while not done:
        # get the next line
        line = infile.readline()
        # stop looping if the end of file is reached
        if not line:
            break

        # exit state
        if 'TRIAL_RESULT' in line:
            done = True
        if 'TRIAL_VAR' in line and 'subtypeid' in line:
            subtypeid = line.split()[-1]
        elif 'TRIAL_VAR' in line and 'clashtype' in line:
            clashtype = line.split()[-1]
        elif 'TRIAL_VAR' in line and 'secondarytask' in line:
            secondarytask = line.split()[-1]


    ############################################
    ### STUFF TO ADD OR TWEAK ##################
    ############################################
    # insert info from .ias file into the stored buffer_holder_index_ias
    timestamp = int(iarea.split()[1])
    ias_info = read_ias_word(iarea, timestamp, ias_folder)
    buffer[buffer_holder_index_ias:buffer_holder_index_ias] = ias_info

    #tweak the ID
    I = 'I' + str(subtypeid)
    D = 'D0'
    if clashtype == 'match' and secondarytask == 'tap':
        E = 'E1'
    elif clashtype == 'match' and secondarytask == 'this':
        E = 'E2'
    elif clashtype == 'clash' and secondarytask == 'tap':
        E = 'E3'
    elif clashtype == 'clash' and secondarytask == 'this':
        E = 'E4'
    elif clashtype == 'FILLLER':
        # NOTE the asc does indeed say filller with three L's
        E = 'E5'
        D = 'D1'
    else:
        print("something broken with tweaking TRIALID")
        exit(-1)

    EID = E + I + D
    new_id = old_trialid.rsplit(' ', 1)[0] + ' ' + EID + '\n'
    buffer[buffer_holder_index_trialid:buffer_holder_index_trialid] = new_id

    ############################################
    ### SAVE INFO BACK TO FILE #################
    ############################################

    # write the contents of the buffer to the output file
    write_to_outfile(new_asc, buffer)

    # close the input file
    infile.close()

# run main()
main()
