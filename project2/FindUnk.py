'''
find unk tokens or pos in train data set
return rawMat with unk and vocList
'''
def FindUnk (rawMat, k, kind = 'pos'): 
    
    txtList = list(rawMat[kind])

    voc_all = {}
    voc_unk = []
    for i in list(set(txtList)):
        voc_all[i] = txtList.count(i)
    
    for word in voc_all.keys():
        if voc_all[word] <= k:
            voc_unk.append(word)
    print len(voc_unk)
    txtList = ['<unk>' if x in voc_unk else x for x in txtList ]
    rawMat[kind] = txtList
    
    vocList = list(set(txtList))
    
    return(rawMat, vocList)