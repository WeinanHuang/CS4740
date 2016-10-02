import glob
import os
import re
import collections



def UncertainDict(filepath):
	
	# Initialization
	files=glob.glob(filepath)
	whole_word = []
	ambi_word = []

	for file in files:
	    f=open(file, 'r')
	    line = f.read().replace('\n', ' ')
	    data_after = ' '.join(line.split())
	    data_final = data_after.split()
	    whole_word.extend(data_final)
	     
	for i in range(len(whole_word)):
	    if ( 'CUE-' in whole_word[i]):
	        ambi_word.append(whole_word[i-2])

	ambi_word = filter(lambda a: a != '-', ambi_word)

	# Uncertain Word Dictionary
	uncertain_dict = {}
	wd_count = collections.Counter(ambi_word)
	for i in list(set(ambi_word)):
	    uncertain_dict[i] = wd_count[i]
	    
	# Sorted dictionry 
	for key, value in sorted(uncertain_dict.iteritems(), key=lambda (k,v): (v,k)):
	    print "%s: %s" % (key, value)

	return (uncertain_dict)


def LabelCue(filepath, UncertainDict):
	
	# Inintialization
	files=glob.glob(filepath)
	whole_word = []

	# Read in Test files, insert 'TBD' at the end of each line
	for file in files:
	    f=open(file, 'r')
	    line = f.read().replace('\n', ' TBD ')
	    data_after = ' '.join(line.split())
	    data_final = data_after.split()
	    whole_word.extend(data_final)

	# Remove consecutive 'TBD' brought by empty line between 2 sentences
	i = 0
	while (i < (len(whole_word) - 1)):
		if whole_word[i] == 'TBD' and whole_word[i + 1] == 'TBD':
			whole_word.pop(i)
		else:
			i = i + 1


    # Label with 'Cue' or '-' according to UncertainDict
	for i in range(0, len(whole_word) - 3, 3):
	    if (whole_word[i] in UncertainDict.keys()):
	    	whole_word[i+2] = 'Cue'
	    else:
	    	whole_word[i+2] = '-'

	return whole_word


trainfiles = '/Users/Raymond/Desktop/COURSE/Fall 2016/4740/project 2/nlp_project2_uncertainty/train/*.txt'
testfiles_private  = '/Users/Raymond/Desktop/COURSE/Fall 2016/4740/project 2/nlp_project2_uncertainty/test-private/*.txt'
testfiles_public   = '/Users/Raymond/Desktop/COURSE/Fall 2016/4740/project 2/nlp_project2_uncertainty/test-public/*.txt'

AmbiDict = UncertainDict(filepath = trainfiles)
LabeledList_private = LabelCue(filepath = testfiles_private, UncertainDict = AmbiDict)
#LabeledList_public = LabelCue(filepath = testfiles_public, UncertainDict = AmbiDict)

for i in range(0, len(LabeledList_private)-3, 3):
    print LabeledList_private[i], '\t', LabeledList_private[i+1], '\t', LabeledList_private[i+2], '\n'

#for i in range(0, len(LabeledList_public)-3, 3):
    #print LabeledList_public[i], '\t', LabeledList_public[i+1], '\t', LabeledList_public[i+2], '\n'
