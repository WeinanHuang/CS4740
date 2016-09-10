# read modules
import glob
import os
import re
import collections
import pandas as pd


headStr1 = 'writes'
headStr2 = 'wrote'
headStr3 = 'said'
headStr4 = 'Subject : Re : '
headStr5 = 'Subject : '
regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

Text = []

path = '/Users/haojiongwang/Desktop/CORNELL/cs4740/data_corrected/classification task/motorcycles/train_docs/*.txt'
files=glob.glob(path)
for file in files:
    f=open(file, 'r')
    line = f.read().replace('\n', '')

    # leave out head (Subject, Email Address, etc)
    if line.find(headStr1) != -1:
        ind = line.find(headStr1)
        data = line[(ind+len(headStr1)):]

    elif line.find(headStr2) != -1:
        ind = line.find(headStr2)
        data = line[(ind+len(headStr2)):]

    elif line.find(headStr3) != -1:
        ind = line.find(headStr3)
        data = line[(ind + len(headStr3)):]

    elif line.find(headStr4) != -1:
        ind = line.find(headStr4)
        data = line[(ind + len(headStr4)):]

    elif line.find(headStr5) != -1:
        ind = line.find(headStr5)
        data = line[(ind + len(headStr5)):]
    else:
        data = line


    data_clean = re.sub('[>]', '', data)
    #print file, '\n', data_clean, '\n'
    #pattern = re.match('-.+', data_clean)
    #data_clean = re.sub('[\|:)()#]', '', data_clean)

    idx = data_clean.find('- - -')



    if (data_clean.find('- - -') != -1 and len(data_clean[idx+1:]) <150):
        data_c1 = data_clean[0:idx+1]
        #print file, '\n','a', '\n'
    else:
        data_c1 = data_clean
    #print file, '\n', data_c1, '\n'

    #print file, '\n', data_c1, '\n'





    idx2 = data_c1.find('- -')

    if (data_c1.find('- -') != -1 and len(data_c1[idx2+1:]) <150):
        data_c2 = data_c1[0:idx2+1]
    else:
        data_c2 = data_c1

    print file, '\n', data_c2, '\n'


    '''
    idx = data_clean.find('= = =')

    if '= = =' in data_clean & len(data_clean[idx:]) < 150:
        print file, '\n', data_clean[idx:], '\n'





    #print file, '\n', data_clean, '\n'


    for email in re.findall(regex, data_clean):
        #data_clean = re.sub(email[0],'', data_clean)
        idx = data_clean.rfind(email[0])
        if len(data_clean[idx:] <150:
            data_clean

            print file, '\n', data_clean[idx:], '\n'

    '''

    # replace uneccesary notation
    rmList = '> " | # : - ) ( * : [ ] } {'
    rmList = rmList.split()
    for n in rmList:
        data = data.replace(n, '')

    # switch multiple blanks into single ones
    data_after = ' '.join(data_clean.split())

    #print file, '\n', data_clean, '\n'
    
    Text = Text + data


# create word types and their frequencies
vocabulary = list(set(Text.split(' ')))
uniGramFreq = collections.Counter(Text.split(' '))

biGramFreq = pd.DataFrame( [0]*(len(vocabulary) * len(vocabulary) ), index = vocabulary, columns = vocabulary)
