'''
Function TranMat()
Takes in raw data(in pandas DataFrame)
Return Transition Matrix(in pandas DataFrame)
'''
import pandas as pd

def TranMat(rawMat):
    
    # generate Transition Matrix, B,I,O by B,I,O
    # cell (m,n) stands for the prob of m followed by n 
    Mat = pd.DataFrame(0, index = ['B','I','O'], columns = ['B','I','O'])
    cueStr = ''.join(list(rawMat['cue_re']))
    
    for idx in range(len(cueStr)-1):
        Mat.loc[cueStr[idx], cueStr[idx+1]] = Mat.loc[cueStr[idx], cueStr[idx+1]] + 1
    
    for rowId in Mat.index:
        for colId in Mat.columns:
            Mat.loc[rowId, colId] = 1. * Mat.loc[rowId, colId] / list(rawMat['cue_re']).count(rowId)

    return Mat