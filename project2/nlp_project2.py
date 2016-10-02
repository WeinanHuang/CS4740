import glob
import os
import re
import collections
import pandas as pd
whole_word = []
path = '/Users/haojiongwang/Desktop/CORNELL/cs4740/project2/nlp_project2_uncertainty/train/*.txt'
files=glob.glob(path)
for file in files:
    f=open(file, 'r')
    line = f.read().replace('\n', ' ')
    data_after = ' '.join(line.split())
    data_final = data_after.split()
    whole_word.extend(data_final)
     
    




ambi_word = []
for i in range(len(whole_word)):
    if ( 'CUE-' in whole_word[i]):
        ambi_word.append(whole_word[i-2])




#this is to get the uncertain dictionary
uncertain_dict = {}
wd_count = collections.Counter(ambi_word)
for i in list(set(ambi_word)):
    uncertain_dict[i] = wd_count[i]
    

#this is to get the sorted dictionry 
for key, value in sorted(uncertain_dict.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)



