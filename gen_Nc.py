'''
Input:  Vocabulary and BigramTable of given topic
Output: Nc of given topic
'''
def gen_Nc(vocList, BigramTable):
    
    maxLocal = [0] * len(vocList)
    for i in range(len(vocList)):
        maxLocal[i] = max(BigramTable[vocList[i]].values())
    maxC = max(maxLocal)
    
    Nc = [0] * (maxC + 1)
    for word in vocList:
        for word2 in BigramTable[word].keys():
            Nc[BigramTable[word][word2]] += 1 
    
    return(Nc)