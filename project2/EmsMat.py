'''
Function: EmsMat()
Takes in rawMat, kind = 'pos'(default) or 'token'
Return Emission Matrix(in pandas DataFrame), token or pos depend on kind
'''
import pandas as pd

def EmsMat(rawMat, kind = 'pos'):
    col = list(set(rawMat[kind]))
    Mat = pd.DataFrame(0, index = ['B','I','O'], columns = col)
    print Mat.shape
    
    cue = list(rawMat['cue_re'])
    col = list(rawMat[kind])
    
    if (len(cue) != len(col)): 
        print('Different Lenght of %s and cue' % kind)
    print len(cue)
    
    for idx in range(len(cue)):
        Mat.loc[cue[idx], col[idx]] = Mat.loc[cue[idx], col[idx]] + 1;
    
    for rowId in Mat.index:
        rowSum = list(rawMat['cue_re']).count(rowId)
        print rowSum
        for colId in Mat.columns:
            Mat.loc[rowId, colId] = 1. * Mat.loc[rowId, colId] / rowSum
    
    return Mat