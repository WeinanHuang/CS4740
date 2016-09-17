'''
Input:  test file text string, shreshold k, topic vocabulary list
Output: test file text string with <unk>
'''
def FillInUnk_Test (txtStr, vocList):
    
    txtList = txtStr.split()
    
    txtList = ['<unk>' if word not in vocList else word for word in txtList ]
    
    return(txtList)