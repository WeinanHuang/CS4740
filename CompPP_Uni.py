
'''
Compute Perplexity.

Input:  test file list, one topic UniGramTable, corresponding Nc, threshold k
Output: Perplexity value for test file belongs to gien topic
'''
def CompPP_Uni (txtList, UniGramTable, Nc, k):
    
    PP = 0
    N  = len(txtList)
    
    for i in range(1,N):    
        if UniGramTable[txtList[i]] <= k:
            c = UniGramTable[txtList[i]]
            cGT = 1. * (c + 1) * Nc[c+1] / Nc[c]
            p = 1. * cGT / N
        else: 
            p = 1. * UniGramTable[txtList[i]] / N
        PP = PP + (- np.log(p))
    
    PP = np.exp(PP/N)
    return(PP)

