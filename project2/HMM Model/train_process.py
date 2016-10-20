# This file process the text into pandas dataframe and
# convert the CUE into I, B, O

import glob
import os
import re
import pandas as pd
filepath = 'C:\Users\Ziyan Liu\Desktop\Cornell\Study\cs4740\prj2\\nlp_project2_uncertainty\\nlp_project2_uncertainty\\train\\*.txt'

def train_process(filepath):

    token = []  # token column
    pos = []    # pos column
    cue = []    # original cue column
    cue_re = [] # cue column I, B, O

    # read in txt files
    files = glob.glob(filepath)
    for file in files:
        f = open(file, 'r')
        for line in f:
            if line[0:1] != '\n':
                text = line.split()
                token.append(text[0])
                pos.append(text[1])
                cue.append(text[2])
            else:
                pass


    # re-label CUE list
    for i in range(len(cue)):
        if cue[i][0:3] == 'CUE':
            if i == 0 or cue[i] != cue[i-1]:
                cue_re.append('B')
            elif cue[i] == cue[i-1]:
                cue_re.append('I')
        else:
            cue_re.append('O')

    # form pandas dataframe
    new_data = {'a': token, 'b': pos, 'c': cue, 'd': cue_re}
    columns = ['token', 'pos', 'cue', 'cue_re']
    result = pd.DataFrame(new_data)
    result.columns = columns
    result.to_csv('result.csv', mode = 'a', header = False, index = False)
    #print result.head(n = 5)

    return result

train_process(filepath)
