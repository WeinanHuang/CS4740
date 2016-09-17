'''
Input:   cleaned text string, shreshold k for unknow words
Output:  text list with <unk>, vocabulary list
'''
def FillInUnk (txtStr, k): 
    
    textList = textStr.split()

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