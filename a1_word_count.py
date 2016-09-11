# read modules
import glob
import os
import re
import collections
#import pandas as pd

def txt_clean(filepath):
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
        
        #print file, '\n', data_clean, '\n'
        #pattern = re.match('-.+', data_clean)
        #data_clean = re.sub('[\|:)()#]', '', data_clean)

        #this is to clean the signture after - - -

        idx = data.find('- - -')



        if (data.find('- - -') != -1 and len(data[idx+1:]) <150):
            data_c1 = data[0:idx+1]
            #print file, '\n','a', '\n'
        else:
            data_c1 = data
        
        #this is to clean the signture after - - 
        idx2 = data_c1.find('- -')

        if (data_c1.find('- -') != -1 and len(data_c1[idx2+1:]) <150):
            data_c2 = data_c1[0:idx2+1]
        else:
            data_c2 = data_c1

        #print file, '\n', data_c2, '\n'


        '''
        idx = data_clean.find('= = =')

        if '= = =' in data_clean & len(data_clean[idx:]) < 150:
            print file, '\n', data_clean[idx:], '\n'





        #print file, '\n', data_clean, '\n'
        '''

        #delete all the email address
        data_clean = data_c2
        for email in re.findall(regex, data_c2):
            #data_clean = re.sub(email[0],'', data_c2)
            data_clean = data_c2.replace(email[0],'')


        #replace all the " ' " to space   
        data_clean = data_clean.replace(" ' ",'')
        #print file, '\n', data_clean, '\n'
        

        # replace uneccesary notation
        rmList = '< > " | # : - ) ( * [ ] } { + = ^ _ ~'
        rmList = rmList.split()
        for n in rmList:
            data_clean = data_clean.replace(n, '')

        # switch multiple blanks into single ones
        data_after = ' '.join(data_clean.split())

        #let all the string tart from letter and end with letter
        idx_head = re.search(r_head, data_after)
        #print file, '\n', data_after[idx_head.start() :], '\n'


        '''
        idx_gethead = idx_head.start()
        data_after = data_after[idx_gethead:]
        
        print file, '\n', data_after, '\n'
        data_after = data_after.strip()

        '''

        #replace all the ...
        data_after = data_after.replace('...', '')
        #print file, '\n', data_after, '\n'

        #start to set boundary
        boundList = [' ? ', ' ! ', ' . ', ' ; ']
        for i in boundList:

            data_after = data_after.replace(i,' <s> ' )


        #get rid of small residual in the email
        if data_after.rfind(' <s> ') != -1 and len(data_after[data_after.rfind(' <s> '):]) <30:
            data_after = data_after[0:data_after.rfind(' <s> ')]

        #set boundary in the end of each string
        data_after = data_after.rstrip(".!?")

        data_fin = data_after + ' <s> ' 

        #get a string for all the email in the folder
        Text = Text + data_fin
        Text = ' '.join(Text.split())

    return Text


# create word types and their frequencies



path = '/Users/Raymond/Downloads/data_corrected/classification task/space/train_docs/*.txt'


Text = txt_clean(path)
TextList = Text.split(' ')
#TextListLen = len(TextList)
#TextList = TextList[:(TextListLen/5)]

wd_base = list(set(TextList))

print 'There are',len(wd_base), 'different words in total.', '\n'


# UniGram
#wd_freq = collections.Counter(TextList)
wd_freq = {}
for wd in wd_base:
    wd_freq[wd] = 1.0 * Text.count(wd) / len(Text.split(' '))

print 'UniGram of words:\n'
print wd_freq, '\n'
print '**************************************************************\n'


# BiGram
print 'BiGram of words:\n'
mat = {}
for wd in wd_base:
    wdFreq = TextList.count(wd)
    mat[wd] = {}
    for wd1 in wd_base:
        mat[wd][wd1] = 1. * TextList.count(wd + ' ' + wd1) / wdFreq

print '**************************************************************\n'

'''
# sentence generation using uni-gram
sentence = ''
# generate first word
p = 0
rand_num = random.uniform(0, 1)

for key, value in wd_freq.iteritems():
    p = p + value
    if rand_num < p:
        prev_word = key
        sentence = sentence + prev_word
        break

while prev_word != '<s>':
    for key, value in wd_freq.iteritems():
        p = p + value
        if rand_num < p:
            prev_word = key
            sentence = sentence + prev_word
            break
'''

# sentence generation using bi-gram
sentence = ''
# generate first word
p = 0
rand_num = random.uniform(0, 1)

for key, value in mat['<s>'].iteritems():
    p = p + value
    if rand_num < p:
        prev_word = key
        sentence = sentence + prev_word
        break

# generate sequence
t = 0
while prev_word != '<s>':
    # t = t + 1
    # if t > 20:
    #     break
    rand_num = random.uniform(0, 1)
    word_dict = mat[prev_word]
    p = 0
    for key, value in word_dict.iteritems():
        #print key, ' ', value
        p = p + value
        if rand_num < p:
            sentence = sentence + ' ' + key
            prev_word = key
            break

print 'sentense:' + sentence





