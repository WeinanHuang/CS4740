import glob
import os
import re
import collections



def UncertainDict(filepath):
    
    # Initialization
    files=glob.glob(filepath)
    whole_word = []
    ambi_word = []

    for file in files:
        f=open(file, 'r')
        line = f.read().replace('\n', ' ')
        data_after = ' '.join(line.split())
        data_final = data_after.split()
        whole_word.extend(data_final)
        
    for i in range(len(whole_word)):
        if ( 'CUE-' in whole_word[i]):
            ambi_word.append(whole_word[i-2])

    ambi_word = filter(lambda a: a != '-', ambi_word)

    # Uncertain Word Dictionary
    uncertain_dict = {}
    wd_count = collections.Counter(ambi_word)
    for i in list(set(ambi_word)):
        uncertain_dict[i] = wd_count[i]
        
    # Sorted dictionry 
    #for key, value in sorted(uncertain_dict.iteritems(), key=lambda (k,v): (v,k)):
        #print "%s: %s" % (key, value)

    return (uncertain_dict)


def LabelCue(filepath, UncertainDict):

    # Inintialization
    files=glob.glob(filepath)
    whole_word = []
    # Read in Test files, insert 'TBD' at the end of each line
    for file in files:
        f=open(file, 'r')
        line = f.read().replace('\n', ' TBD ')
        data_after = ' '.join(line.split())
        data_final = data_after.split()
        whole_word.extend(data_final)

    # Remove consecutive 'TBD' with End of Sentence 'EOS'
    i = 0
    while (i < (len(whole_word) - 1)):
        if whole_word[i] == 'TBD' and whole_word[i + 1] == 'TBD':
            whole_word[i+1] = 'EOS'
        else:
            i = i + 1


    # Label with 'Cue' or '-' according to UncertainDict
    i = 0
    while (i < (len(whole_word)-3)):
        if (whole_word[i] in UncertainDict.keys()):
            whole_word[i+2] = 'Cue'
        else:
            whole_word[i+2] = '-'
        
        if (whole_word[i+3] == 'EOS'):
            i = i + 4
        else:
            i = i + 3
    
    # Generate token level output list
    tokenOutput = []
    tokenNum = 0
    i = 0
    print 'start token output building\n'
    while (i < len(whole_word)):
        if whole_word[i] == 'EOS':
            i = i + 1
        elif (whole_word[i] in UncertainDict.keys()):
            tokenOutput.append(tokenNum)
            tokenNum = tokenNum + 1
            i = i + 3
        else:
            tokenNum = tokenNum + 1
            i = i + 3
    print 'end token output building\n'
    
    
    # Generate sentence level output list
    sentenceOutput = []
    sentenceHead = 0
    sentenceEnd  = 0
    sentenceIdx  = 0
    count = 0
    print 'start sentence output building\n'
    
    while (sentenceHead < len(whole_word) and count < 50000):
        count = count + 1
        sentenceEnd = whole_word[(sentenceHead):].index('EOS') + sentenceHead
        ambi = False
        
        for i in range(sentenceHead, sentenceEnd, 3):
            if whole_word[i] in UncertainDict.keys():
                ambi = True
                break
        if ambi:
            sentenceOutput.append(sentenceIdx)
            
        sentenceHead = sentenceEnd + 1
        sentenceIdx  = sentenceIdx + 1
        
    print count
    print 'end sentence output building\n'  
    
        
    return whole_word, tokenOutput, sentenceOutput



trainfiles = '/Users/Raymond/Desktop/COURSE/Fall 2016/4740/project 2/nlp_project2_uncertainty/train/*.txt'
testfiles_private  = '/Users/Raymond/Desktop/COURSE/Fall 2016/4740/project 2/nlp_project2_uncertainty/test-private/*.txt'
testfiles_public   = '/Users/Raymond/Desktop/COURSE/Fall 2016/4740/project 2/nlp_project2_uncertainty/test-public/*.txt'

AmbiDict = UncertainDict(filepath = trainfiles)
result_private = LabelCue(filepath = testfiles_private, UncertainDict = AmbiDict)
result_public = LabelCue(filepath = testfiles_public, UncertainDict = AmbiDict)


tokenPub = ''
flag = True
for i in range(0,len(result_public[1]) - 1):
    if i == 0 or flag:
        tokenPub = tokenPub + str(result_public[1][i])
        flag = False
        
    else:
        if (result_public[1][i+1] != result_public[1][i] + 1):
            tokenPub = tokenPub + '-' + str(result_public[1][i]) + ' '
            flag = True
            
tokenPri = ''
flag = True
for i in range(0,len(result_private[1]) - 1):
    if i == 0 or flag:
        tokenPri = tokenPri + str(result_private[1][i])
        flag = False
        
    else:
        if (result_private[1][i+1] != result_private[1][i] + 1):
            tokenPri = tokenPri + '-' + str(result_private[1][i]) + ' '
            flag = True
tokenTxT = open("Basline_token.txt", "w")
tokenTxT.write("Type,Spans\n")
tokenTxT.write("CUE-public,%s\n" % tokenPub)
tokenTxT.write("CUE-private,%s" % tokenPri)
tokenTxT.close()



senPub = ' '.join(str(result_public[2]).strip('[]').split(', '))
senPri = ' '.join(str(result_private[2]).strip('[]').split(', '))
sentenceTxT = open("Basline_sentence.txt", "w")
sentenceTxT.write("Type,Indices\n")
sentenceTxT.write("SENTENCE-public,%s\n" % senPub)
sentenceTxT.write("SENTENCE-private,%s" % senPri)
sentenceTxT.close()
