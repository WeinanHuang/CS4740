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

