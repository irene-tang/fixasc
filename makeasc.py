import sys

"""
inputs:
    subjx.asc
    IA_2.ias ... IA101.ias
"""

original_asc = sys.argv[1]
new_asc = sys.argv[2]
ia_2 = sys.argv[3]

buffer = []
header = False
cal1 = False

freelines = 0 # number of following lines to include with no questions asked

infile = open(original_asc, 'r')
line = ''

while True:
    line = infile.readline()

    # stop looping at end of file
    if not line:
        break

    if freelines:
        buffer.append(line)
        freelines -= 1
        continue # skips remainder of this iteration

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
    elif 'MSG' in line and 'TRIALID' in line:
        buffer.append(line)
        # .ias stuff goes here
        # can read in the following info
        done = False
        filler_index = 0
        while not done:
            line = infile.readline()
            if not line:
                break
            elif 'START' in line:
                # save a space for !MODE RECORD since it comes in the wrong spot
                filler_index = len(buffer)
                buffer.append('filler for !MODE RECORD')
                # keep the START line
                buffer.append(line)
                # read PRESCALAR
                line = infile.readline()
                if not line:
                    break
                buffer.append(line)
                # read VPRESCALALR
                line = infile.readline()
                if not line:
                    break
                buffer.append(line)
                # read PUPIL AREA
                line = infile.readline()
                if not line:
                    break
                buffer.append(line)
                # read EVENTS GAZE R/L RATE
                line = infile.readline()
                if not line:
                    break
                buffer.append(line)
                # read INPUT something
                line = infile.readline()
                if not line:
                    break
                buffer.append(line)
                # read !MODE RECORD and put it back up there in the filler where it belongs
                line = infile.readline()
                buffer[filler_index] = line
                # begin saccads, fizations, blinkings

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

    else:
        print line


with open(new_asc, 'w') as outfile:
    for x in buffer:
        outfile.write(x)

infile.close()
outfile.close()
