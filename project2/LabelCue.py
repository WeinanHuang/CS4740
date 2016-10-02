import glob
import os
import re
import collections


def LabelCue(filepath, UncertainDict):
	
	# Inintialization
	files=glob.glob(filepath)
	whole_word = []

	for file in files:
	    f=open(file, 'r')
	    line = f.read().replace('\n', ' - ')
	    data_after = ' '.join(line.split())
	    data_final = data_after.split()
	    whole_word.extend(data_final)

	for i in range(len(whole_word)):
	    if (whole_word[i] in UncertainDict.keys()):
	    	whole_word[i+2] = 'Cue'

	return whole_word