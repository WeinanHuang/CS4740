
'''
Based on UniGram Count table, generate Nc List.

Input:  vocabulary list and UniGramTable for given topic
Output: Nc as a list
'''
def gen_Nc_Uni (vocList, UniGramTable):
    

    maxC = max(UniGramTable.values())
    
    Nc = [0] * (maxC + 1)
    for word in vocList:
        Nc[UniGramTable[word]] += 1 
    
    return(Nc)

