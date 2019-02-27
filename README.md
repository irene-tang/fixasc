# limerick1 workspace

thesis work

# workflow and details
1. makeasc - reformats our data files into something that's compatible with the UMASS software
	installation: python/python3
2. question_acc
		variables in the script: at the top, INPUT_FOLDER and OUTPUT_FOLDER
3. scripter2
		variabls in the script:  $input and $output
4. make_cnt
		variables in the script: OUTPUT_FOLDER, input_file, delim_char, lowest_cond, highest_cond
5. fix_align
	installation: R
	parameters: check out all of them (see CohenBRM.pdf for details), especially asc_files, fa_dir, start_flag
	added a line at the end that calls fix_align() function, and ran the script through the terminal (Rscript copy_fix_align.R)
	this takes a while
	tip: do not save  plots  as .tiff, it takes up all of the hard drive space
6. robodoc
		variables in the script: output_folder, input_foldr
		line 1020 onwards: fixing the things listed in files_processed.lst, exclude.lst, and keep.lst, since they are incorrect
7. dataanal
	ANALASC.doc seems to be the README equivalent for the folder
	there are a bunch of programs in this folder. we only want to use eyedry -- so see eyedry_doc.doc in particular
	make note of what answers to the questions (this will be saved in the trace  file), see EyeLab manual for how to answer the questions
