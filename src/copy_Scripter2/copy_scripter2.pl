#82908 this version is modified to deal with Jane's display, in which there are multiple display change regions on multiple lines#



#this script reads in a tab-delimited file of sentences, #
#with item numbers, condition numbers, trialtype, #
#timeout, etc.#
#and outputs them in the format used for eyetrack script files.#
#the sentences should have a return (\n) at the end.#
#your questions should have trialtype 'question'#
#It has to be set up as follows:#
# condition	item	dependent	trialtype	correct response	timeout duration	sentence1	sentence2#

#note that the 'correct response' column should be empty for sentences (or you could put 'none'); it should have a value only#
#for questions#

#note that the 'sentence2' column should be empty unless the trial is a display change#
#note also that the 'sentence2' column needs to be marked with percent signs(%) as delimiters for#
#the display change region#

#the program asks you to give the x and y offsets in pixels#
#which are used to determine the x and y coordinates for the change region#
#you are also asked to specify how many pixels per character on your monitor#
#(the user has to figure this out beforehand).#
#if no display change, you can just hit return for these questions#




# print("Enter the name of your sentence file: ");
# $inputfile = <STDIN>;
$inputfile = "copy_Scripter2/input_to_scripter.txt";
chomp($inputfile);


# print("What is your x offset, in pixels?\n");
# print("(If you don't have any display change trials, just hit return.) ");
	# $xoff= <STDIN>;
	$xoff= "\n";
	chomp($xoff);

# print("What is your y offset, in pixels?\n");
# print("(If you don't have any display change trials, just hit return.) ");
	# $yoff= <STDIN>;
	$yoff= "\n";
	chomp($yoff);

# print("How many horizontal pixels per character (make sure to check with your font and your monitor)?\n");
# print("(If you don't have any display change trials, just hit return.) ");
	# $pixchar= <STDIN>;
	$pixchar= "\n";
	chomp($pixchar);

# print("How many vertical pixels per row(make sure to check with your font and your monitor)?\n");
# print("(If you don't have any display change trials, just hit return.) ");
	# $pixrow= <STDIN>;
	$pixrow= "\n";
	chomp($pixrow);

# print("Do you want to automatically generate sequences?y or n:");
# $sequence = <STDIN>;
$sequence = "\n";
chomp($sequence);

# print("Enter the name of your output file: ");
# $outputfile = <STDIN>;
$outputfile = "../data/scripter_output/output_from_scripter.script";
chomp($outputfile);

open(inputfile, $inputfile) or die("can't open file\n");
open(outputfile, ">$outputfile") or die("can't write to file\n");


while ($line = <inputfile>) {
	chomp($line);
	#this now splits the data based on tabs#
	@entries = split(/\t/,$line);
	#this defines the values of condition, item, sentence, etc.#
	#note that because perl starts counting array entries from zero,#
	#we have to subtract one from the column number entered above#
	$condition = $entries[0];
	$item = $entries[1];
	$dependent = $entries[2];
	$trialtype = $entries[3];
	$response = $entries[4];
	$timeout = $entries[5];
	$sentence1 = $entries[6];

#this next bit checks if there's a sentence 2,#
#and if there is, divides it at the delimiters#
#and uses the pixel info to assign x and y  coords#
	if (@entries > 7){
		$sentence2 = $entries[7];
		#here's the part that's new for Jane.#
		#first it takes sentence2 and splits it into lines#
		@targetlines = split(/\\n/,$sentence2);
		#then it assigns each line to a hash, called linenum#
		$i = 1;
		while($i <= @targetlines){
			$linenum{$i} = $targetlines[$i-1];
			$i++;
		}
		#this starts a counter for the display change regions
		$k = 1;

		#this part goes through the lines one at a time#
		#and finds the display change regions#
		#it assumes that the first region of any line is NOT#
		#a change region#
		$i = 1;
		while($i <= @targetlines){
			#this does the splitting#
			@targetparts = split(/%/,$linenum{$i});
			#this assigns each part of the line to a hash#
			$j = 1;
			while($j <= @targetparts){
				$region{$j} = $targetparts[$j-1];
				#this checks if it's a display change region#
				#only even numbered regions should be change regions#
				#then it figures out the x and y change coordinates for the region#
				if ($j%2 == 0){
					#this computes the combined lengths of all the regions#
					#prior to the region of interest#
					$start = 0;
					$m = 1;
					while ($m < $j){
						$start += length($region{$m});
						$m++;
					}
					#now we're figuring out the coordinates#
					$x1{$k} = $xoff + ($start*$pixchar);
					$x2{$k} = $x1{$k} + (length($region{$j})*$pixchar);
					#to figure out y1 you need to count the rows above#
					$y1{$k} = $yoff + (($i-1)*$pixrow);
					$y2{$k} = $y1{$k} + $pixrow;
					#this indexes the counter for the display change regions#
					$k++;
				}
				#this indexes the counter of the number of regions on a line#
				$j++;
			}
			#this indexes the row counter#
			$i++;
		}

		#this just gets rid of the delimiters for output in the script
		$sentence2=~s/%//g;
	}

	print(outputfile "trial E$condition","I$item","D$dependent\n");
	if ($trialtype eq "question") {
		print(outputfile "  button =\t\t$response\n");
	}
	print(outputfile "  gc_rect =\t\t(0 0 0 0)\n");
	print(outputfile "  inline =\t\t|$sentence1\n");
	if (@entries > 7){
		print(outputfile "  inline =\t\t|$sentence2\n");
	}
	print(outputfile "  max_display_time =\t$timeout\n");
	if (@entries > 7){
		print(outputfile "  region =\t\t");
		$m = $k;
		$k = 1;
		while ($k < $m){
		print (outputfile "($y1{$k} $x1{$k} $y2{$k} $x2{$k})");
		$k++;
		}
	print(outputfile "\n");
	}

	print(outputfile "  trial_type =\t\t$trialtype\n");
	print(outputfile "end E$condition","I$item","D$dependent\n\n");

}

close(inputfile);
close(outputfile);

open(inputfile, $inputfile) or die("can't open file\n");
open(outputfile, ">>$outputfile") or die("can't write to file\n");

#this is the part that does the sequences#
#first it determines if the trial is a question#
	if ($sequence eq "y"){
		while ($line = <inputfile>) {
			chomp($line);
			@entries = split(/\t/,$line);
			$condition = @entries[0];
			$item = @entries[1];
			$dependent = @entries[2];
			$trialtype = @entries[3];
				if ($trialtype eq "question") {
				#now it goes back through and finds all the sentence trials with the same item number#
				#note that now the sentence variables are, e.g., item2, while the question#
				#variables are just, e.g., item#
					open(secondfile, $inputfile);
					while ($line = <secondfile>) {
						chomp($line);
						@entries = split(/\t/,$line);
						$condition2 = @entries[0];
						$item2 = @entries[1];
						$dependent2 = @entries[2];
						$trialtype2 = @entries[3];
						if ($trialtype2 ne "question" and $item2 eq $item) {
							print(outputfile "sequence SE$condition2","I$item2\n");
							print(outputfile "  E$condition2","I$item2","D$dependent2\n");
							print(outputfile "  E$condition","I$item","D$dependent\n");
							print(outputfile "end SE$condition2","I$item2\n\n");
						}
					}
					close(secondfile);
				}
		}

	}
close(inputfile);
close(outputfile);
