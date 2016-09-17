import glob
import os
import re
import collections
import nltk
import random
import pylab as pl
import numpy as np
import operator
import matplotlib.pyplot as plt
#nltk.download()
#I used the nltk in the code, please download the package before running our code
# global variables
work_dir = os.getcwd() + '/'
#please change the path to the data file
head = '/Users/haojiongwang/Desktop/CORNELL/cs4740/data_corrected/classification task/'
#head = work_dir + 'data_corrected/classification task/'
text_type = ['atheism', 'autos', 'graphics','medicine','motorcycles','religion','space']

tail = '/train_docs/*.txt'

path = [head + text_type[i] +tail for i in range(len(text_type))]

#this function is the do the text cleaning. 
#The input path is the path where text file was stored
#The output is the whole string for each topic
def txt_clean(filepath):
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
        
        print file, '\n', data_after, '\n'
        data_after = data_after.strip()

        

        #replace all the ...
        #data_after = data_after.replace('...', '')
        #print file, '\n', data_after, '\n'
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sen_list = ['<s> ' + s for s in sent_detector.tokenize(data_after.strip())]
        sen_str = ' '.join(sen_list)
        #print file, '\n', sen_str,'\n'
        
        
        #get a string for all the email in the folder
        Text = Text + ' ' + sen_str
    return Text + ' <s> '

#this function is to generate sentence built on language model
#the input is dictionary from previous step ie probability of unigram and conditional probability bigram
#the output is the sentence
def Sen_generation(UniGram, BiGram, num_sen):
    sentence_bilist = ''
    sentence_unilist = ''
    for j in range(num_sen):
        # sentence generation using uni-gram
        sentence = ''
        # generate first word
        p = 0
        rand_num = random.uniform(0, 1)

        for key, value in UniGram.iteritems():
            p = p + value
            if rand_num < p:
                prev_word = key
                sentence = sentence + prev_word
                break

        while prev_word != '<s>':
            rand_num = random.uniform(0, 1)
            p = 0
            for key, value in UniGram.iteritems():
                p = p + value
                if rand_num < p:
                    prev_word = key
                    sentence = sentence + ' ' + prev_word
                    break
        sentence_unilist = sentence_unilist + sentence + '\n'
        

    # sentence generation using bi-gram
    for j in range(num_sen):
        sentence = ''
        # generate first word
        p = 0
        rand_num = random.uniform(0, 1)

        for key, value in BiGram['<s>'].iteritems():
            p = p + value
            if rand_num < p:
                prev_word = key
                sentence = sentence  + prev_word
                print i, ' ', prev_word, '\n'
                break

        # generate sequence
        t = 0
        while prev_word != '<s>':
            # t = t + 1
            # if t > 20:
            #     break
            rand_num = random.uniform(0, 1)
            word_dict = BiGram[prev_word]
            p = 0
            for key, value in word_dict.iteritems():
                #print key, ' ', value
                p = p + value
                if rand_num < p:
                    sentence = sentence + ' ' + key 
                    prev_word = key
                    break

        #print 'sentense:' + sentence
        sentence_bilist = sentence_bilist + sentence + '\n'
    return sentence_unilist, sentence_bilist

# create word types and their frequencies

sen_unigram = ''
sen_bigram = ''

for i in range(len(path)):
    
    sen_bigram = sen_bigram + ' ' + text_type[i] + '\n'
    sen_unigram = sen_unigram + ' ' + text_type[i] + '\n'
    
    Text = txt_clean(path[i])
    TextList = Text.split(' ')
    #TextListLen = len(TextList)
    #TextList = TextList[:(TextListLen/5)]
 
    wd_base = list(set(TextList))
    print 'There are',len(wd_base), 'different words in total.', '\n'
    
    wd_count = collections.Counter(TextList)
    
    # UniGram
    UniGram = {}
    text_len = len(Text.split(' '))
    for wd in wd_base:
        print '*********************Unigram*******************************\n'
        #print i,'\n',wd, '\n'
        UniGram[wd] = 1.0 * wd_count[wd] / text_len

    #print 'UniGram of words:\n'
    #print wd_freq, '\n'
    #print '*************************Unigram******************************\n'
    
    
    # BiGram
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

    for Key in BiGram.keys():
        for key, value in BiGram[Key].items():
            BiGram[Key][key] = 1. * value / wd_count[Key]
    
    # output probability table
    TableFile = open('BiGram Probability Table.txt', 'w')

    for Key1 in BiGram.keys():
        
        TableFile.write('Probability Table for ' + Key1 + ' :\n')
        
        for Key2 in BiGram[Key1].keys():
            line = Key1 + '\t' + Key2 + '\t' + '>>>>>>>>>>>>>>>>>>' + '\t' + str(BiGram[Key1][Key2]) + '\n'
            TableFile.write(line)
        
        print '\n'
    
    TableFile.close()
    
    #sentence generatin with unigram and bigram
    sen_unilist, sen_bilist  = Sen_generation(UniGram, BiGram, 100)
    sen_unigram = sen_unigram + sen_unilist
    sen_bigram = sen_bigram + sen_bilist

#write the file
text_file = open("bifile.txt", "w")

text_file.write(sen_bigram)

text_file.close()

text_file = open("unifile.txt", "w")

text_file.write(sen_unigram)

text_file.close()

m = 30 # m words with highest frequencis

# visualize words with high frequencies in generated sentences
def FreqVisual(s, m):

    sfile = work_dir  + s + 'file.txt'
    sf = open(sfile, 'r')
    sline = sf.read().replace('\n', '')
    data = sline.split()

    # freqency counts
    f_count = collections.Counter(data)
    sorted_f_count = sorted(f_count.items(), key = operator.itemgetter(1))
    sorted_f_count = sorted_f_count[-30:]
    print sorted_f_count
    freq = []
    word = []
    for i in range(len(sorted_f_count) ):
        freq.append(sorted_f_count[i][1])
        word.append(sorted_f_count[i][0])

    # plot histogram
    X = np.arange(len(freq))

    fig = plt.figure(figsize = (16, 9))
    ax1 = fig.add_subplot(111)
    ax1.bar(X, freq, align = 'center', width = 0.5)
    ax1.set_xticks(range(m))
    ymax = max(f_count.values()) + 1
    ax1.set_xticklabels(word, fontsize = 13)
    ax1.set_ylim(0, ymax)
    ax1.set_xlabel('Word Type', fontsize = 15)
    ax1.set_ylabel('Frequency', fontsize = 15)
    ax1.set_title( s.title() + 'Gram', fontsize = 22 )
    fig.savefig(s.title() + 'Gram')

s = 'bi'
FreqVisual(s, m)
s = 'uni'
FreqVisual(s, m)
