import os
import statistics # requires python 3.4+

# the min stdev from the median that we're going to tolerate
MIN_DEV = 2.5
QUEST_SUM_FILEPATH = "../data/question_acc/QuestSum.txt"

# list of lines in the file, excluding the header line
lines = open(QUEST_SUM_FILEPATH, "r").readlines()[1:]

# dictionary mapping participant's data filepath (str) : their question accuracy (int)
question_acc_dict = {}
for line in lines:
    # split the components of the line into a list
    participant_info = line.split()
    # add to dictionary
    question_acc_dict[participant_info[0]] = int(participant_info[2])

# list of percent accuracies (in no particular order)
percent_accuracies_list = question_acc_dict.values()

# calculate the median
median_acc = statistics.median(percent_accuracies_list)

# calculate the standard deviation
stdev = statistics.stdev(percent_accuracies_list)

# remove participants who scored 2.5+ stdev's below the median
for participant, score in question_acc_dict.items():
    if score < median_acc - stdev * MIN_DEV:
        os.remove(participant)
        print("Excluded " + participant + " from analysis based on question accuracy score")
