'''
Input:   cleaned text string, shreshold k for unknow words
Output:  text list with <unk>, vocabulary list
'''
def FillInUnk (txtStr, k): 
    
    txtList = txtStr.split()

    voc_all = {}
    for i in txtList:
        voc_all[i] = txtList.count(i)

    unkList = []
    for word in voc_all.keys():
        if voc_all[word] <= k: 
            unkList.append(word)
    
    for word in unkList:
        txtList = ['<unk>' if x == word else x for x in txtList ]
    
    vocList = list(set(txtList))
    
    return(txtList, vocList)