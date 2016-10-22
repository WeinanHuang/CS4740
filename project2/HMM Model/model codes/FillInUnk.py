'''
based on vocList, replace test matrix with unk, 
return testMat
'''
def FillInUnk (filepath, vocList, kind = 'pos'):
    
    # read test files and store as testMat
    token = []  # token column
    pos = []    # pos column
    cue = []    # cue column, initialize to be all 'O'
    files = glob.glob(filepath)
    for file in files:
        f = open(file, 'r')
        for line in f:
            if line[0:1] != '\n':
                text = line.split()
                token.append(text[0])
                pos.append(text[1])
                cue.append('O')
            else:
                pass
    new_data = {'a': token, 'b': pos, 'c': cue}
    columns = ['token', 'pos', 'cue']
    testMat = pd.DataFrame(new_data)
    testMat.columns = columns
    print testMat.shape
    
    # fill in unk
    txtList = testMat[kind]
    txtList = ['<unk>' if x not in vocList else x for x in txtList]
    testMat[kind] = txtList
    
    return(testMat)