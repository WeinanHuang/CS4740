'''
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