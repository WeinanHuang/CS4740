
'''
Based on cleaned training text list, generate UniGram Count Table.

Input:  word list and vocabulary
Output: the Unigram count table
'''
def gen_UniGram(TextList,wd_base):
    
    UniGram = {}
    for wd in wd_base:
        UniGram[wd] = TextList.count(wd)

    return(UniGram)

