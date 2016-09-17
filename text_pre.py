import glob
import os
import re
import collections
import nltk
import random
import numpy as np
import operator

#nltk.download()
#I used the nltk in the code, please download the package before running our code
# global variables
work_dir = os.getcwd() + '/'
#please change the path to the data file
head = '/Users/haojiongwang/Desktop/CORNELL/cs4740/data_corrected/classification task/'
#head = work_dir + 'data_corrected/classification task/'
text_type = ['atheism', 'autos', 'graphics','medicine','motorcycles','religion','space']

tail = '/train_docs/*.txt'

#path = [head + text_type[i] +tail for i in range(len(text_type))]

#this function is the do the text cleaning. 
#The input path is the path where text file was stored
#The output is the whole string for each topic
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
        
        #print file, '\n', line, '\n'
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
            #print file, '\n','a', '\n'
        else:
            data_c1 = data_clear_symbol
        
        #this is to clean the signture after - - 
        idx2 = data_c1.find('- -')

        if (data_c1.find('- -') != -1 and len(data_c1[idx2+1:]) <150):
            data_clear_sig = data_c1[0:idx2+1]
        else:
            data_clear_sig = data_c1

        #print file, '\n', data_c2, '\n'


        

        #delete all the email address
        for email in re.findall(regex, data_clear_sig):
            data_clear_sig = data_clear_sig.replace(email[0],'')


        #replace all the " ' " to space   
        data_clear_sig = data_clear_sig.replace(" ' ",'')
        #print file, '\n', data_clean, '\n'
        

        # replace uneccesary notation
        rmList = '> " | # : - ) ( * [ ] } { + = ^ __ ~ / \\'
        rmList = rmList.split()
        for n in rmList:
            data_clear_sig = data_clear_sig.replace(n, '')

        # switch multiple blanks into single ones
        data_postclean = ' '.join(data_clear_sig.split())

        #let all the string tart from letter and end with letter
        idx_head = re.search(r_head, data_postclean)
        #print file, '\n', data_after[idx_head.start() :], '\n'


        
        idx_gethead = idx_head.start()
        data_after = data_postclean[idx_gethead:]
        
        #print file, '\n', data_after, '\n'
        data_after = data_after.strip()

        Text = Text + ' ' + data_after
        
    return Text 

clean_string = {'atheism':'', 'autos':'','graphics':'','medicine':'','motorcycles':'','religion':'','space':''}

for i in text_type:
	path = head + i +tail
	print i
	clean_string[i] = txt_clean_for_pre(path)

'''
Input:   cleaned text string, shreshold k for unknow words
Output:  text list with <unk>, vocabulary list
'''
def FillInUnk (txtStr, k): 
    
    textList = txtStr.split()

    voc_all = {}
    for i in textList:
        voc_all[i] = textList.count(i)

    unkList = []
    for wd in voc_all.keys():
        if voc_all[wd] <= k: 
            unkList.append(wd)
    
    for wd in unkList:
        textList = ['<unk>' if x == wd else x for x in textList ]
    
    vocList = list(set(textList))
    
    return(textList, vocList)

'''
Take word list and vocabulary as input
based on the bigram model output the bigram frequency table
'''

def gen_BiGram(TextList,wd_base):
    BiGram = {}
    for wd in wd_base:
        BiGram[wd] = {}

    for i in range(len(TextList) - 1):
        BiGram[TextList[i]][TextList[i + 1]] = 0

        
    for i in range(len(TextList) - 1):
        print '**********************Bigram********************************\n'
        print 100.0 * i / len(TextList),'\n',TextList[i], '\n', TextList[i + 1] , '\n'
        wd = TextList[i]
        wd1 = TextList[i+1]
        BiGram[wd][wd1] = BiGram[wd][wd1] + 1 

    return BiGram


text, vocabulary = FillInUnk(clean_string['atheism'], 1)
fre_table = gen_BiGram(text, vocabulary)
print fre_table


