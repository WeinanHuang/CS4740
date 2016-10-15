# This file process the text in test set into pandas dataframe and

import glob
import os
import re
import pandas as pd
#filepath = 'C:\Users\Ziyan Liu\Desktop\Cornell\Study\cs4740\prj2\\nlp_project2_uncertainty\\nlp_project2_uncertainty\\test-public\\*.txt'
filepath = 'C:\Users\Ziyan Liu\Desktop\Cornell\Study\cs4740\prj2\\nlp_project2_uncertainty\\nlp_project2_uncertainty\\test-private\\*.txt'

def test_process(filepath):

    token = []
    pos = []

    # read in txt files
    files = glob.glob(filepath)
    for file in files:
        f = open(file, 'r')
        for line in f:
            if line[0:1] != '\n':
                text = line.split()
                token.append(text[0])
                pos.append(text[1])
            else:
                pass

    # form pandas dataframe
    new_data = {'a': token, 'b': pos}
    columns = ['token', 'pos']
    result = pd.DataFrame(new_data)
    result.columns = columns
    result.to_csv('result.csv', mode = 'a', header = False, index = False)
    #print result.head(n = 5)

    return result

test_process(filepath)
