'''
This script aims to determine 2 hyper parameters in computing the Perplexity by Cross Validation.

Two hyper parameters to be determined:
1) threshold of unknown words;
2) upper roof of Good Turing adjustment.
'''
import glob
import os
import re
import collections
import nltk
import random
import numpy as np
import operator


'''
Clean training text.

Input:  file path contains where text file stored
Output: whole string for one topic
'''
def txt_clean_for_pre(filepath):
    #first set up some string to cut off the head of the e-mail
    headStr1 = 'writes :'
    headStr2 = 'wrote :'
    headStr3 = 'said :'
    headStr4 = 'Subject : Re : '
    headStr5 = 'Subject : '

    #this regular expression is set to capture the email address
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                        "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                        "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

    #this is to set a regular expression which will be used to capture the first occurance of letter
    r_head = re.compile("([a-zA-Z]+?)")

    Text = ''

    #read all the file now
    files=glob.glob(filepath)
    for file in files:
        f=open(file, 'r')
        line = f.read().replace('\n', '').lower()
        
        # leave out head (Subject, Email Address, etc)
        if line.rfind(headStr1) != -1:
            ind = line.rfind(headStr1)
            data = line[(ind+len(headStr1)):]

        elif line.rfind(headStr2) != -1:
            ind = line.rfind(headStr2)
            data = line[(ind+len(headStr2)):]

        elif line.rfind(headStr3) != -1:
            ind = line.rfind(headStr3)
            data = line[(ind + len(headStr3)):]

        elif line.rfind(headStr4) != -1:
            ind = line.rfind(headStr4)
            data = line[(ind + len(headStr4)):]

        elif line.rfind(headStr5) != -1:
            ind = line.rfind(headStr5)
            data = line[(ind + len(headStr5)):]

        else:
            data = line

        #clean the symbol >
        data_clear_symbol = re.sub('[>]', '', data)
        
        #this is to clean the signture after - - -
        idx = data_clear_symbol.find('- - -')

        if (data_clear_symbol.find('- - -') != -1 and len(data_clear_symbol[idx+1:]) <150):
            data_c1 = data_clear_symbol[0:idx+1]
        else:
            data_c1 = data_clear_symbol
        
        #this is to clean the signture after - - 
        idx2 = data_c1.find('- -')

        if (data_c1.find('- -') != -1 and len(data_c1[idx2+1:]) <150):
            data_clear_sig = data_c1[0:idx2+1]
        else:
            data_clear_sig = data_c1

        #delete all the email address
        for email in re.findall(regex, data_clear_sig):
            data_clear_sig = data_clear_sig.replace(email[0],'')

        #replace all the " ' " to space   
        data_clear_sig = data_clear_sig.replace(" ' ",'')

        # replace uneccesary notation
        rmList = '> " | # : - ) ( * [ ] } { + = ^ __ ~ / \\'
        rmList = rmList.split()
        for n in rmList:
            data_clear_sig = data_clear_sig.replace(n, '')

        # switch multiple blanks into single ones
        data_postclean = ' '.join(data_clear_sig.split())

        #let all the string tart from letter and end with letter
        idx_head = re.search(r_head, data_postclean)
        idx_gethead = idx_head.start()
        data_after = data_postclean[idx_gethead:]
        data_after = data_after.strip()
        Text = Text + ' ' + data_after
        
    return Text



'''
Fill in words with occurance <= k with <unk> in training texts

Input:   cleaned text string, shreshold k for unknow words
Output:  text list with <unk>, vocabulary list
'''
def FillInUnk (txtStr, k): 
    
    txtList = txtStr.split()

    voc_all = {}
    for i in list(set(txtList)):
        voc_all[i] = txtList.count(i)

    unkList = []
    for word in voc_all.keys():
        if voc_all[word] <= k: 
            unkList.append(word)
    
    for word in unkList:
        txtList = ['<unk>' if x == word else x for x in txtList ]
    
    vocList = list(set(txtList))
    
    return(txtList, vocList)



'''
Fill in words not in vocabulary with <unk> in test texts

Input:  test file text string, shreshold k, topic vocabulary list
Output: test file text string with <unk>
'''
def FillInUnk_Test (txtStr, vocList):
    
    txtList = txtStr.split()
    
    txtList = ['<unk>' if word not in vocList else word for word in txtList ]
    
    return(txtList)



'''
Based on cleaned training text list, generate BiGram Count Table.

Input:  word list and vocabulary
Output: the bigram count table
'''
def gen_BiGram(TextList,wd_base):
    BiGram = {}
    for wd in wd_base:
        BiGram[wd] = {}

    for i in range(len(TextList) - 1):
        BiGram[TextList[i]][TextList[i + 1]] = 0

        
    for i in range(len(TextList) - 1):
        #print '**********************Bigram********************************\n'
        #print 100.0 * i / len(TextList),'\n',TextList[i], '\n', TextList[i + 1] , '\n'
        wd = TextList[i]
        wd1 = TextList[i+1]
        BiGram[wd][wd1] = BiGram[wd][wd1] + 1 

    return(BiGram)



'''
Based on BiGram Count table, generate Nc List.

Input:  vocabulary list and BigramTable for given topic
Output: Nc as a list
'''
def gen_Nc (vocList, BigramTable):
    
    maxLocal = [0] * len(vocList)
    for i in range(len(vocList)):
        maxLocal[i] = max(BigramTable[vocList[i]].values())
    maxC = max(maxLocal)
    
    Nc = [0] * (maxC + 1)
    for word in vocList:
        for word2 in BigramTable[word].keys():
            Nc[BigramTable[word][word2]] += 1 
    
    return(Nc)



'''
Compute Perplexity.

Input:  test file list, one topic BigramTable, corresponding Nc, threshold k
Output: Perplexity value for test file belongs to gien topic
'''
def CompPP (txtList, BigramTable, Nc, k):
    import numpy as np
    
    PP = 0
    N  = len(txtList)
    
    for i in range(1,N):    
        if txtList[i] not in BigramTable[txtList[i-1]].keys():
            p = Nc[1] / N
        elif BigramTable[txtList[i-1]][txtList[i]] <= k:
            c = BigramTable[txtList[i-1]][txtList[i]]
            cGT = 1. * (c + 1) * Nc[c+1] / Nc[c]
            p = 1. * cGT / sum(BigramTable[txtList[i]].values())
        else: 
            p = 1. * BigramTable[txtList[i-1]][txtList[i]] / sum(BigramTable[txtList[i-1]].values())
        PP = PP + (- np.log(p))
    
    PP = np.exp(PP/N)
    return(PP)



'''
Cross Validation
'''

head = '/Users/Raymond/Desktop/COURSE/Fall 2016/4740/data_corrected/classification task/'
text_type = ['atheism', 'autos', 'graphics','medicine','motorcycles','religion','space']
tail = '/train_docs/*.txt'
clean_string = {'atheism':'', 'autos':'','graphics':'','medicine':'','motorcycles':'','religion':'','space':''}
for i in text_type:
    path = head + i +tail
    clean_string[i] = txt_clean_for_pre(path)


unkRange = range(0, 10)
GTRange  = range(0,5)
result   = np.ndarray(shape = (10,5))

for k_unk in unkRange:

