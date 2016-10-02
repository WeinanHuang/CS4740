import glob
import os
import re
import collections
import nltk
import random
import numpy as np
import operator

'''
Take word list and vocabulary as input
based on the bigram model output the bigram frequency table
'''
def gen_TriGram(TextList,wd_base):
    BiGram = {}
    for wd in wd_base:
    	for wd1 in wd_base:    		
	        TriGram[wd] = {}
	        TriGram[wd][wd1] = {}
    for i in range(len(TextList) - 2):
        TriGram[TextList[i]][TextList[i + 1]][TextList[i + 2]] = 0

        
    for i in range(len(TextList) - 2):
        wd = TextList[i]
        wd1 = TextList[i+1]
        wd2 = TextList[i + 2]
        TriGram[wd][wd1][wd2] = TriGram[wd][wd1][wd2] + 1 


    return TriGram
