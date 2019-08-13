# Limerick1 workspace

Technical elements of a cognitive psychology thesis work to be submitted to the [faculty](https://www.swarthmore.edu/psychology/faculty-staff) of the [Department of Psychology](https://www.swarthmore.edu/psychology) at [Swarthmore College](swarthmore.edu) in May 2019 in partial fulfillment for the degree of Bachelor of Arts.

## Table of Contents
* [Background / Abstract [draft]](#background-/-abstract)
* [In this repository](#in-this-repository)
* [Requirements](#requirements)
* [Usage](#usage)
	* [Step 1: Gather data](#step-1-gather-data)
	* [Step 2: Generate files necessary for analysis](#step-2-generate-files-necessary-for-analysis)
	* [Step 3: Set up parameters for data analysis](#step-3-set-up-parameters-for-data-analysis)
	* [Step 4: Acquire data analysis measures](#step-4-acquire-data-analysis-measures)
	* [Step 5: Edit data analysis measures format](#step-5-edit-data-analysis-measures-format)
	* [Step 6: Statistical analysis](#step-6-statistical-analysis)
* [Support and Contributing](#support-and-contributing)
	* [Troubleshooting FAQ](#troubleshooting-faq)
	* [Additional support](#additional-support)
* [Acknowledgements](#acknowledgements)
* [License](#license)
* [TODO](#todo)


# Background / Abstract
**_Occupation of Inner Speech in the Working Memory During Silent Reading:<br/>
Effects of Articulatory Suppression on Anticipated Lexical Stress_**

As we silently read words on a page, we use an “inner speech” that includes rhythm and inflections as if we are reading aloud. We also use an inner speech when performing non-reading tasks such as remembering verbal materials, problem solving, mental calculation, and decision making. Present research has not yet determined whether these two uses of inner speech occupy the same cognitive resources. This paper presents findings from an eye-tracking study designed to explore whether the inner speech of silent reading occupies the same resources in working memory as other mental tasks. In the first part of the experiment, participants read stress-alternating homographs (e.g., PREsent, preSENT) embedded in limericks, which compelled them to initially expect the incorrect prosody of the homograph and thus encounter a reading cost. As they read, participants also performed articulatory suppression by repeating the word this aloud. The goal of this was to use the outer voice to occupy the relevant resources in working memory, thus rendering them unavailable to be used during silent reading—this allows us to see if those resources pertain to the inner voice of silent reading. Participants also completed the 18-item Varieties of Inner Speech Questionnaire (VISQ; McCarthy-Jones & Fernyhough, 2011), a self-assessment survey that assesses one’s relationship with inner speech. The goal of this was to see if participants who reported experiencing higher levels of inner speech in their everyday lives would be more susceptible to the reading costs prompted by articulatory suppression during rhythm-mismatching limericks. If the differences in reading costs between reading rhythm-matching and -mismatching limericks vanish while repeating this, and if participants who experience higher levels of inner speech are more affected by articulatory suppression, then this would show that these two inner voices occupy the same working memory resources. The study found some preliminary evidence that articulatory suppression can diminish the effect of stress clash on silent reading, as well as some preliminary indication that inner speech occupies working memory and that this machinery overlaps with the inner voice of the rehearsal component of the phonological loop.

Key words: inner speech, silent reading, working memory, phonological loop, articulatory suppression, eye movements

[Back to top](#limerick1-workspace)

# In this repository

* `src/` - source code
* `data/` - data
* `test/` - testing stuff, everything in here is archived stuff to be ignored
* a mountain of technical difficulties

See [project wiki](https://github.com/itang1/limerick1/wiki) for more details about contents.

[Back to top](#limerick1-workspace)

# Requirements

## Compatibility
This package works with Mac and Linux terminals.

It works with Windows, too, but this is difficult for a variety of reasons: Command Prompt uses different commands than the ones described in the usage instructions below, when you do something wrong whilst running eyedry it crashes without showing you the error message, and retrieving files from Bash is difficult. If necessary though, there's at least one workaround for Windows through using the [VisualStudio Code IDE](https://code.visualstudio.com) + [GitHub Desktop](https://desktop.github.com) bash shell.

TL;DR: Best to use macOS or Linux.

## Required programs

* [python3.4+](https://www.python.org/downloads/)
* [perl](https://www.perl.org/get.html)
* [R](https://www.r-project.org)
* [GCC compiler for C](https://gcc.gnu.org/releases.html) (or substitute with another compiler)

TODO: autogen

[Back to top](#limerick1-workspace)

# Usage

## Step 1: Gather data
1. **Create the experiment in ExperimentBuilder.**
	* Ideally, we would have create it using the UMass eyetracking experiment template to avoid the technical struggles of getting to data analysis, but we could not with this particular experiment because this experiment has a secondary task component that isn't supported by the UMass setup.
2. **Run participants.**
	* Experimenter script, debriefing, participant log, pre-registration, etc. are located in the `EyeTrackingLabAdmin/Limerick1/` shared Drive folder.
	* Information about how stuff was run and where files are located can be found in the Experimenter Script.
3. **Convert data files from EDF to ASC**
	* Each participant's data will be located on the Host computer in e.g. `Desktop/Exeriments/LimerickProsodyDeployed/LimerickProsodyA/results/subject0/`
	* In that folder, there should be an .edf file titled e.g. `subject0.edf`. Double-click on that .edf file to generate an .asc file.
		* There's some EDF to ASC converter software installed on the Host computer that allows it to do that. Double-clicking an EDF file on your personal computer won't do anything if you don't have that software installed.
4. **Gather original ASC files and AOI folders**
	* Once the .asc file has been generated, copy it onto a thumbdrive or something and place it into this package's `data/original_asc/` folder.
	* Also copy each of the eight Areas of Interest (AOI) folders into this package's `data/original_asc/` folder, so that it contains `A_aoi/`, `B_aoi/`, `C_aoi/`, `D_aoi/`, `RevA_aoi/`, `RevB_aoi/`, `RevC_aoi/`, `RevD_aoi/`.
5. **Match participants with their list**
	* This experiment used a Latin Square design. Participants saw one of eight possible lists. Analysis will require knowing which list each participant saw.
	* In `src/make_new_asc/lists.py` is a dictionary mapping lists to participants who saw that list. The eight lists are A, B, C, D, RevA, RevB, RevC, RevD.

[Back to top](#limerick1-workspace)

## Step 2: Generate files necessary for analysis
From within the `/src` directory, run:
```
python3 runall.py
```

All input variables are already written into the respective scripts (but see above section for where to modify things during future use). This single script executes the following all at once in this order:

* Deletes all subfolders (and their contents) except for original_asc/ and eyedry/, and then recreates them as empty folders for a fresh start
* make_new_asc.py
* copy_question_acc.py
* remove_participants_question_acc.py
* copy_Scripter2.pl
* copy_make_cnt.py
* copy_fix_align_v0p92.R
* copy_Robodoc.py

[Back to top](#limerick1-workspace)

## Step 3: Set up parameters for data analysis

1. From within `src/eyedry/`, compile eyedry: (ignore any warnings)
```
gcc eyedry.c -o eyedry
```
 NOTE: this only needs to be done once, ever

2. From within `src/`, run the executable that we just created: (ignore any warnings)
```
./eyedry/eyedry
```

3. Eyedry will ask a series of questions. For details of what each question is asking, see the eyelab manual. A copy of the manual is located in `EyeTrackingLabAdmin/UMassEyetrack/eyelabmanual.pdf`. We answered as follows:

<!-- generated with the aid of https://www.tablesgenerator.com/markdown_tables -->

| Question | Answer | Explanation and Comments |
|----:|:----:|----|
| What is the output trace file name? | `../data/eyedry/trace_1.txt` | This does not affect functionality. |
| Type an identifying string to print out | trying to get data on [date and time] | This does not affect functionality. |
| What is the maximum number of fixations on an item | [press return] | Using default |
| Type name of file containing control info (CR if none) | `eyedry/limerick1.ctl`, or press return and re-generate it as follows: | this .ctl file can be saved and re-used |
| Debug level | 0 | |
| Does the question after a sentence have the same COND and ITEM number as the sentences and fall on the next line? | n | |
| Do you want to eliminate trials on the basis of errors to questions? | n | |
| What is the smallest numbered experimental item? | 1 | |
| What is the largest numbered experimental item? | 40 | |
| How many regions maximum? | 7 | |
| What is the smallest condition number (after any exception adjustment)? | 1 | |
| What is the largest condition number (after any exception adjustment)? | 4 | |
| How many subconditions maximum for any one item? | 4 | We didn't exactly have subconditions, but it breaks otherwise. |
| What field is the condition number in? | 2 | According to `HowToReadRoboDocOutput.txt` |
| What field is the item number in? | 3 | According to `HowToReadRoboDocOutput.txt` |
| What field is the number-of-fixations number in | 6 | according to `HowToReadRoboDocOutput.txt` (note that this is different from what's suggested in the aged eyetrackingmanual.pdf) |
| What field do the data start in? | 7 | According to `HowToReadRoboDocOutput.txt` (note that this is different from what's suggested in the aged eyetrackingmanual.pdf) |
| Longest fixation time, msec (truncate if above) | 800 | Same as Breen and Clifton (2011) |
| Shortest fixation time, msec (discard if below) | 80 | Same as Breen and Clifton (2011) |
| What is the screen width in characters? | 160 | Approximately but we didn't use fix-width font |
| What is the maximum number of lines of text? | 5 | |
| Do you want to permit regions to wrap around end of a line? | n | |
| Did your .sen/.stm file have blank lines between lines of text? | y | No idea, we don't even have .sen/.stm files |
| Do you want to analyze just some of your trials (eg 1st half)? | n | |
| Do you want to analyze just the first N trials in each condition? | n | |
| Following the questions, it will ask to confirm the values that were just entered. | Double-check them and correct errors if necessary by entering the number of the value to change (instructions are on the screen). Then [press return] to continue. | |
| What file name do you want to save these values as (CR if none)? | `eyedry/limerick1.ctl` or [press return]| This will only be asked if you did not enter a .ctl file above or if you changed one of its values. This does not affect functionality. |
| What is the name of file that lists data files? | `../data/robodoc/files_processed.lst` | |
| Any exceptions file? | n | |
| ~~Control~~ Count (.CNT) file name? | `../data/scripter/output_from_scripter.cnt` | Typo, it's supposed to be "count file" not "control file." |


After answering these questions, the next that should appear is a "Which analysis?" list of possible analyses that can be performed. Continue to the next step.

[Back to top](#limerick1-workspace)

## Step 4: Acquire data analysis measures

### 4.1. Overview of analysis (just read, nothing to do here)

* **Prior to analysis:** (following Breen and Clifton, 2011)
	* Eliminated participants who scored below 2.5 standard deviations below the median on the "is this limerick dirty" comprehension questions (standard practice).
		* This was done when we ran `remove_participants_question_acc.py` as part of `runall.py`
	* Eye movement data was cleaned of track losses, blinks, and long fixations over 800ms using EyeDoctor.
		* We cleaned track losses and blinks when we ran Robodoc.
		* We cleaned long fixations when we passed in parameters to EyeDoctor in the previous step.
	* Short fixations (<80ms) were incorporated into the nearest neighboring fixation within three characters, otherwise deleted.
		* We cleaned short fixations when we passed in parameters to EyeDoctor in the previous step.
	* Long fixations (>800ms) were deleted
		* We cleaned long fixations when we passed in parameters to EyeDoctor in the previous step.
	* Trials with blinks or track losses on the critical word were eliminated
		* We eliminated trials with blinks or track losses when we ran Robodoc.

* **Analysis of standard eyetracking measures:** (following Breen and Clifton, 2011; see also Rayner, 1998; Rayner et al.,1989)
	* **First-pass time** - sum of all fixations made from first entering to first leaving a region, eliminating trials on which no such fixations occurred.
	* **Go-past time** - sum of all fixation durations made from first entering a region to first leaving it to the right.
	* **Probability of fixating in a region** - no description provided.
	* **Probability of regressing out of a region given that it was fixated during the first pass** - no description provided.
	* **First fixation duration for critical Region 3** - no description provided
		* Due to non-significance, Breen and Clifton (2011) did not report these data.

[Back to top](#limerick1-workspace)

### 4.2. Generate data analysis files (instructions here)
Each of the following measures will be obtained within the terminal starting from the "Which analysis?" prompt. Completion of each measure will return you to this prompt. Answer the questions as follows.

WARNING: Sometimes the program segfaults and crashes for various unknown reasons.

**Shortcuts:**
* [4.2.A. First-pass time](#42a-first-pass-time)
* [4.2.B. Go-past time](#42b-go-past-time)
* [4.2.C. Probability of fixating a region](#42c-probability-of-fixating-a-region)
* [4.2.D. Probability of regressing out of a region](#42d-probability-of-regressing-out-of-a-region)
* [4.2.E. First fixation duration](#42e-first-fixation-duration)
* [4.2.F. Fin.](#42f-fin)

[Back to top](#limerick1-workspace)

#### **4.2.A. First-pass time**

| Question | Answer | Explanation and Comments |
|----:|:----:|----|
| Which analysis? | 2 | |
| Type an identifying string to print out | First pass time | This doesn't affect functionality. |
| Throw away zero fixation values? | n | We will take care of zero-fixations later through the awk script |
| Do you want to CULMINATE or AVERAGE multiple fixations in a region? | c | |
| RAW times, MS/char, or DEVIATION from regression | r | |
| Conditionalize on presence/absence of regression in critical region? | n | |
| Conditionalize on presence/absence of fixation in critical region? | n | |
| What is the upper summed cutoff for first pass time? | [press return] | Use default 2000 |
| Conditionalize on position of last fixation before each region? | n | |
| File of item X subject combinations | `firstPassIXS` | We will base our analysis on this file. |
| Do you want ALL trials written, or just trials with Observations? | a | |
| Do you want Wide output (all regions in one row) or Narrow (one row per region)? | w | |
| Subject by subject file, one condition per line (not systat) | `firstPassSXS` | We won't base our analysis on this file, but might as well save it. |
| Subject by subject file, formatted for Systat | [press return] | We don't want this file. |
| Item by item file, one condition per line (not systat) | `firstPassIXI` | We won't base our analysis on this file, but might as well save it. |
| Item by item file, formatted for Systat | [press return] | We don't want this file. |
| Do you want information about long and short times printed? | n | WARNING: "y" is a possible source of segfault. |
| Do you want a typeout of the item-by-item data? | n | WARNING: "y" is a possible source of segfault. |

[Back to top](#limerick1-workspace)

#### **4.2.B. Go-past time**
| Question | Answer | Explanation and Comments |
|----:|:----:|----|
| Which analysis? | 13 | |
| Type an identifying string to print out | Go-past time | This doesn't affect functionality. |
| Throw away zero fixation values? | y | |
| Do you want to CULMINATE or AVERAGE multiple fixations in a region? | c | |
| Do you want to keep RAW times or convert to MSEC/CHAR?| r | |
| Which analysis | 1 | There are three options here. We want sum of all time from first entering region to first going past. |
| File of item X subject combinations | `goPastIXS` | We will base our analysis on this file. |
| Do you want ALL trials written, or just trials with Observations? | a | |
| Do you want Wide output (all regions in one row) or Narrow (one row per region)? | w | |
| Subject by subject file, one condition per line (not systat) | `goPastSXS` | We won't base our analysis on this file, but might as well save it. |
| Subject by subject file, formatted for Systat | [press return] | We don't want this file. |
| Item by item file, one condition per line (not systat) | `goPastIXI` | We won't base our analysis on this file, but might as well save it.|
| Item by item file, formatted for Systat | [press return] | We don't want this file. |
| Do you want information about long and short times printed? | n | WARNING: "y" is a possible source of segfault. |
| Do you want a typeout of the item-by-item data? | n | WARNING: "y" is a possible source of segfault. |

[Back to top](#limerick1-workspace)

#### **4.2.C. Probability of fixating a region**
| Question | Answer | Explanation and Comments |
|----:|:----:|----|
| Which analysis? | 6 | |
| Type an identifying string to print out | Probability of fixating in a region | This doesn't affect functionality. |
| Which analysis: | 1 | Probability of one or more fixations |
| Conditionalize on position of last fixation before each region? | n | |
| File of item X subject combinations | `probFixationIXS` | We will base our analysis on this file. |
| Do you want ALL trials written, or just trials with Observations? | a | |
| Do you want Wide output (all regions in one row) or Narrow (one row per region)? | w | |
| Subject by subject file, one condition per line (not systat) | `probFixationSXS` | We won't base our analysis on this file, but might as well save it. |
| Subject by subject file, formatted for Systat | [press return] | We don't want this file. |
| Item by item file, one condition per line (not systat) | [`probFixationIXI` | We won't base our analysis on this file, but might as well save it. |
| Item by item file, formatted for Systat | [press return] | We don't want this file. |
| Do you want information about long and short times printed? | n | WARNING: "y" is a possible source of segfault. |
| Do you want a typeout of the item-by-item data? | n | WARNING: "y" is a possible source of segfault. |

[Back to top](#limerick1-workspace)

#### **4.2.D. Probability of regressing out of a region**
| Question | Answer | Explanation and Comments |
|----:|:----:|----|
| Which analysis? | 4 | |
| Type an identifying string to print out | Probability of regresing out of a region | This doesn't affect functionality. |
| File of item X subject combinations | `probRegressionIXS` | We will base our analysis on this file. |
| Do you want ALL trials written, or just trials with Observations? | a | |
| Do you want Wide output (all regions in one row) or Narrow (one row per region)? | w | |
| Subject by subject file, one condition per line (not systat) | `probRegressionSXS` | We won't base our analysis on this file, but might as well save it. |
| Subject by subject file, formatted for Systat | [press return] | We don't want this file. |
| Item by item file, one condition per line (not systat) | `probRegressionIXI` | We won't base our analysis on this file, but might as well save it. |
| Item by item file, formatted for Systat | [press return] | We don't want this file. |
| Do you want information about long and short times printed? | n | WARNING: "y" is a possible source of segfault. |
| Do you want a typeout of the item-by-item data? | n | WARNING: "y" is a possible source of segfault. |

[Back to top](#limerick1-workspace)

#### **4.2.E. First fixation duration**
| Question | Answer | Explanation and Comments |
|----:|:----:|----|
| Which analysis? | 1 | |
| Type an identifying string to print out | First fixation duration | This doesn't affect functionality. |
| Which analysis: | 3 | Initial one of multiple fixations |
| Do you want to keep RAW times or convert to MSEC/CHAR? | r | |
| Conditionalize on presence/absense of regression in critical region? | n | |
| Conditionalize on presence/absense of fixation in critical region? | n | |
| Conditionalize on position of last fixation before each region? | n | |
| File of item X subject combinations | `firstFixationIXS` | We will base our analysis on this file. |
| Do you want ALL trials written, or just trials with Observations? | a | |
| Do you want Wide output (all regions in one row) or Narrow (one row per region)? | w | |
| Subject by subject file, one condition per line (not systat) | `firstFixationSXS` | We won't base our analysis on this file, but might as well save it. |
| Subject by subject file, formatted for Systat | [press return] | We don't want this file |
| Item by item file, one condition per line (not systat) | `firstFixationIXI` | We won't base our analysis on this file, but might as well save it. |
| Item by item file, formatted for Systat | [press return] | We don't want this file |
| Do you want information about long and short times printed? | n | WARNING: "y" is a possible source of segfault. |
| Do you want a typeout of the item-by-item data? | n | WARNING: "y" is a possible source of segfault. |

[Back to top](#limerick1-workspace)

#### **4.2.F. Fin.**

Press 0 to Quit.

Move all of those generated files into `../data/eyedry/originals/`.

NOTE: the trace file (e.g. `../data/eyedry/trace_limerick1.txt`) contains a record of everything that was performed with EyeDry just now.


[Back to top](#limerick1-workspace)

### 4.3. Check that the analyses measures are actully adequate
Sample a few trials from the analyses files to compare "by hand" with the video viewer in ExperimentBuilder. Play the participants' eye movements for those trials at 25% of the speed, and see if they seem to correspond with the purported firstPass duration, goPast duration, probabilityFixation, probabilityRegression, etc.

To match the participants' measures in the analyses files back together with their eye-movement videos in ExperimenterBuilder, consider the following:
* The subject numbers (second column) in each of the IXS measures files (e.g. `firstPassIXS`) respectively correspond to participants in the `data/robodoc/files_processed.lst` file.
* The sequence number (first column) in each of the IXS measures files (e.g. `firstPassIXS`) correspond with the DataViewer TrialID with this relationship:
	```
	dataviewer_trialid = (sequence_number + 1) / 2 + 1
	```
	* Math was done to discover this relationship.
	* NOTE: The TRIALID from the original .asc file and the TRIALID from the DataViewer for the same limerick trial are apparently off-by-one. The .asc file starts counting at 0, while Dataviewer starts counting at 1.

* Double-check: The item number (third column) in each of the IXS measures files (e.g. `firstPassIXS` should correspond exactly with the TRIALID number in the original .asc file. Check the limerick from the .asc for that trial against the one for that sequence in `src/scripter/input_to_scripter`; they should be the same limerick.
* Triple-check: The condition number should match against the original .asc.
* Can also take a look at RPlots.pdf

[Back to top](#limerick1-workspace)

## Step 5: Edit data analysis measures format
From within `/src`, run:
```
python3 edit_cond.py
```

This replaces missing values with 0 and replaces condition numbers with their word descriptions (e.g. 1 => match_tap) for each of five IXS measures files.

It also repairs the unexplainable error where some random lines in the measures files contained a zero condition value but a non-zero sequence value; for these, it replaces the sequence value wtih 0.

The edited files become stored into `data/eyedry/edited_originals` per the script.

## Step 6: Statistical Analysis

### Run through Stat
#### NOT EXCLUDING ZERO FIXATIONS:
From within `data/eyedry/edited_originals`, run:

FOR REGION 2
```
awk -F"," '$4~/_/{print $2,$4,$6}' firstPassIXS_edited | tr "_" " "| ../anova subj clashtype secondtask time
```

FOR REGION 3
```
awk -F"," '$4~/_/{print $2,$4,$7}' firstPassIXS_edited | tr "_" " "| ../anova subj clashtype secondtask time
```

etc. for each of the measures:
* firstPassIXS_edited
* firstFixIXS_edited
* goPastIXS_edited
* probRegression
* probFixation

#### EXCLUDING ZERO FIXATIONS:
FOR REGION 2
```
awk -F"," '$4~/_/ && $7!=0{print $2,$4,$7}' firstPassIXS_edited | tr "_" " "| ../anova subj clashtype secondtask time
```

FOR REGION 3
```
awk -F"," '$4~/_/ && $7!=0{print $2,$4,$7}' firstPassIXS_edited | tr "_" " "| ../anova subj clashtype secondtask time
```

#### UNBALANCED GRID DUE TO EXCLUDING ZERO FIXATIONS:

### Graphs
* Copy measures from terminal into excel (perhaps with the aid of a text-to-TSV converter such as https://www.browserling.com/tools/text-to-tsv)

* Make graphs

# Support and Contributing

## Troubleshooting FAQ

* Help I lost a data file.
	* Copies of every .edf should be stored on the Source computer.
* Help my participant is looking at the blue dot but it's not triggering.
	* Recalibration can be performed between blocks at each break point, but unfortunately we are not able to perform mid-block recalibration :( In the meantime just guide the participant's gaze to find the trigger point, and remind them again to refrain from moving. Some damage repair can hopefully be absolved when we run `fixAlign.R` on the ascii files.

## Additional support
* If anything is buggy or unclear, please open an issue or pull request, or contact ~~itang1@swarthmore.edu~~ itang1@alum.swarthmore.edu.
* This repo is no longer actively being maintained as of June 2019.

[Back to top](#limerick1-workspace)

## Future work
* Limerick2

# Acknowledgements
Thanks to Professor [Dan Grodner](https://www.swarthmore.edu/psychology/faculty-staff) for enormous guidance and so much invested time over the years; to Professors [Dan Grodner](https://www.swarthmore.edu/psychology/faculty-staff) and [Nathan Sanders](http://sanders.phonologist.org) for setting up the experiment; to Drs. [Mara Breen](https://www.mtholyoke.edu/~mbreen/) and [Charles Clifton](http://www.umass.edu/pbs/people/charles-clifton) for providing the [stimuli](https://www.mtholyoke.edu/~mbreen/pubs/LimericksItems.pdf) and [research](https://www.mtholyoke.edu/~mbreen/pubs/BreenClifton_JML_2011.pdf) on which this study was based; to Drs. [Charles Clifton](http://www.umass.edu/pbs/people/charles-clifton), [Adrian Staub](https://www.umass.edu/pbs/people/adrian-staub), [Andrew Cohen](https://www.umass.edu/pbs/people/andrew-cohen), [Jesse Harris](https://linguistics.ucla.edu/person/jesse-harris/), and [colleagues](http://blogs.umass.edu/eyelab/people/) for creating and maintaining the [eyetracking analysis software](http://blogs.umass.edu/eyelab/software/) that we relied on; to the alumni and current students practicing research in the [Swarthmore Psycholinguistics Lab](https://www.swarthmore.edu/psychology/labs); to the [Swarthmore Department of Psychology](https://www.swarthmore.edu/psychology) for sponsoring the experiment; and to the undergraduate students at [Swarthmore College](https://www.swarthmore.edu) who participated in the study.

[Back to top](#limerick1-workspace)

# License
[MIT License](LICENSE)

(c) Copyright 2019 Swarthmore Psycholinguistics Lab etc.

This project was created for non-monetary educational purposes only (please don't sue me)

[Back to top](#limerick1-workspace)
