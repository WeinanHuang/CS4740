
# coding: utf-8

# In[81]:

from __future__ import division
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
        #print '**********************Bigram********************************\n'
        #print 100.0 * i / len(TextList),'\n',TextList[i], '\n', TextList[i + 1] , '\n'
        wd = TextList[i]
        wd1 = TextList[i+1]
        BiGram[wd][wd1] = BiGram[wd][wd1] + 1 


    return BiGram

'''
Input:   cleaned text string, shreshold k for unknow words
Output:  text list with <unk>, vocabulary list
'''
def FillInUnk (txtStr, k): 
    
    textList = txtStr.split()

    voc_all = {}
    for i in list(set(textList)):
        voc_all[i] = textList.count(i)

    unkList = []
    for wd in voc_all.keys():
        if voc_all[wd] <= k: 
            unkList.append(wd)
    
    for wd in unkList:
        textList = ['<unk>' if x == wd else x for x in textList ]
    
    vocList = list(set(textList))
    
    return(textList, vocList)

def txt_clean_for_test(filepath):
    test_str = {}
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
        #print file, '\n', data_after, '\n'
        test_str[re.findall(r'\d+',file[file.rfind("/"):])[0]] = data_after

        
        
    return test_str

def FillInUnk_Test (txtStr, vocList):
    
    txtList = txtStr.split()
    
    txtList = ['<unk>' if word not in vocList else word for word in txtList ]
    
    return(txtList)

'''
Input:  Vocabulary and BigramTable of given topic
Output: Nc of given topic
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
Input:  test file list, one topic BigramTable, corresponding Nc, threshold k
Output: Perplexity value for test file belongs to gien topic
'''
def CompPP (txtList, BigramTable, Nc, k):
    import numpy as np
    
    PP = 0
    N  = sum(Nc)
    
    for i in range(1,len(txtList)):    
        if txtList[i] not in BigramTable[txtList[i-1]].keys():
            p = 1. * Nc[1] / N

        elif BigramTable[txtList[i-1]][txtList[i]] <= k:
            c = BigramTable[txtList[i-1]][txtList[i]]
            cGT = 1. * (c + 1) * Nc[c+1] / Nc[c]
            p = 1. * cGT / sum(BigramTable[txtList[i]].values())

        else: 
            p = 1. * BigramTable[txtList[i-1]][txtList[i]] / sum(BigramTable[txtList[i-1]].values())
        PP = PP + (- np.log(p))
    
    PP = np.exp(PP/len(txtList))
    return(PP)


# In[82]:

work_dir = os.getcwd() + '/'
#please change the path to the data file
head = '/Users/haojiongwang/Desktop/CORNELL/cs4740/data_corrected/classification task/'
#head = work_dir + 'data_corrected/classification task/'
text_type = ['atheism', 'autos', 'graphics','medicine','motorcycles','religion','space']

tail = '/train_docs/*.txt'
clean_string = {'atheism':'', 'autos':'','graphics':'','medicine':'','motorcycles':'','religion':'','space':''}
head_test = '/Users/haojiongwang/Desktop/CORNELL/cs4740/data_corrected/classification task/test_for_classification//*.txt'

test_clean = txt_clean_for_test(head_test)

for i in text_type:
	path = head + i +tail
	print i
	clean_string[i] = txt_clean_for_pre(path)


# In[83]:

data_pre = {}
data_pre['text']={}
data_pre['bigram'] = {}
data_pre['vocabulary'] = {}
data_pre['Nc'] = {}

for i in text_type:
    print i
    data_pre['text'][i], data_pre['vocabulary'][i] = FillInUnk(clean_string[i], 1)
    data_pre['bigram'][i] = gen_BiGram(data_pre['text'][i], data_pre['vocabulary'][i])
    data_pre['Nc'][i] = gen_Nc(data_pre['vocabulary'][i],data_pre['bigram'][i])
    


# In[84]:

final_test_dic = {}
for i in range(len(test_clean)):
    final_test_dic[str(i)] = {}
    final_test_dic[str(i)]['Perplexity'] = {}
    for j in range(len(text_type)):
        final_test_dic[str(i)][text_type[j]] = {}
        final_test_dic[str(i)][text_type[j]]['text'] = FillInUnk_Test(test_clean[str(i)], data_pre['vocabulary'][text_type[j]])
        #print text_type[j], '\n', final_test_dic[str(i)][text_type[j]],'\n'
        
        text_file = final_test_dic[str(i)][text_type[j]]['text']
        bigram = data_pre['bigram'][text_type[j]]
        nc_num = data_pre['Nc'][text_type[j]]
        print CompPP(text_file,bigram,nc_num,1),'\n'
        
        final_test_dic[str(i)]['Perplexity'][text_type[j]]= CompPP(text_file,bigram,nc_num,1)




# In[85]:

res_list = []
for i in range(len(test_clean)):
    class_res =  min(final_test_dic[str(i)]['Perplexity'], key=final_test_dic[str(i)]['Perplexity'].get)
    res_list.append(class_res)


# In[48]:




# In[86]:

print res_list


# In[100]:

list_encode = [200]*len(res_list)
for i in range(len(res_list)):
    if res_list[i] == 'atheism':
        list_encode[i] = 0
        
    elif res_list[i] == 'autos':
        list_encode[i] = 1
        
    elif res_list[i] == 'graphics':
        list_encode[i] = 2
        
    elif res_list[i] == 'medicine':
        list_encode[i] = 3
        
    elif res_list[i] == 'motorcycles':
        list_encode[i] = 4
        
    elif res_list[i] == 'religion':
        list_encode[i] = 5
        
    elif res_list[i] == 'space':
        list_encode[i] = 6
            
        
        


# In[101]:

print len(list_encode)


# In[102]:

import pandas as pd
df1 = pd.DataFrame(list_encode)


# In[75]:




# In[103]:

df1.to_csv('/Users/haojiongwang/Desktop/CORNELL/cs4740/df1.csv')


# In[98]:

res_list = [300]*len(test_clean)
for i in range(len(test_clean)):
    cl = 'unknown'
    minCount = 10**4
    for j in text_type:
        unkCount = final_test_dic[str(i)][j]['text'].count('<unk>')
        if unkCount < minCount:
            cl = j
            minCount = unkCount
    res_list[i] = cl
 


# In[99]:

print res_list


# In[ ]:



