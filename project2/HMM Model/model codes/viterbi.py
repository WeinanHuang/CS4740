'''
takes in test file matrix, transition matrix, emission matrix and kind = 'pos' or 'token'
return the best cue sequence in Trace list: 0:'B', 1:'I', 2:'O'
'''
def viterbi(testMat, tranMat, emsMat, kind = 'pos'):
    
    testMat = testMat.reset_index()
    tranMat = tranMat.as_matrix()
    emsMat.index = range(3)
    
    # initialize 2 matrix to store score and best source idex
    scoreMat = np.zeros((3, len(testMat[kind])))
    BPTR_Mat = np.zeros((3, len(testMat[kind])))
   
    for i in range(3):
        scoreMat[i, 0] = emsMat.ix[i,0]
        BPTR_Mat[i, 0] = 0.0

    ncol = len(testMat[kind])

    for i in range(1,ncol):
        for nowCue in range(3):
            scoreMat[nowCue, i] = 0
            BPTR_Mat[nowCue, i]  = 0
            for prevCue in range(3):
                nowScore = scoreMat[prevCue, i-1] * tranMat[prevCue, nowCue] * emsMat.ix[nowCue,testMat[kind][i]]
                if (nowScore > scoreMat[nowCue, i]):
                    scoreMat[nowCue, i] = nowScore
                    BPTR_Mat[nowCue, i] = prevCue

    Trace = [3.0] * ncol
    Trace[ncol - 1] = np.argmax(scoreMat[:,ncol-1])
    for i in range(ncol-2,-1,-1):
        Trace[i] = BPTR_Mat[Trace[i+1], i+1]
    return Trace