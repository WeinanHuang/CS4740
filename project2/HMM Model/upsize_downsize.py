
delimit = [-1]
for i in range(len(train)):
    if train['token'][i] == '.' and train['pos'][i] == '.':
        delimit.append(i)

import random
df = pd.DataFrame()
df2 = pd.DataFrame()
for i in range(len(delimit)-1):
    if 'B' in train['cue_re'][delimit[i] + 1:delimit[i+1] + 1].values:
        df2 = train.iloc[delimit[i] + 1:delimit[i+1] + 1]
        df = pd.concat([df,pd.DataFrame(df2)], ignore_index=False)
        
    elif random.random() < 0.1:
        df2 = train.iloc[delimit[i] + 1:delimit[i+1] + 1]
        df = pd.concat([df,pd.DataFrame(df2)], ignore_index=False)
        
import numpy as np
num_uncertain = 0
num_certain = 0
df_certain = pd.DataFrame()
df_uncertain = pd.DataFrame()
delimit_uncertain = []
df2 = pd.DataFrame()
for i in range(len(delimit)-1):
    if 'B' in train['cue_re'][delimit[i] + 1:delimit[i+1] + 1].values:
        num_uncertain += 1
        df2 = train.iloc[delimit[i] + 1:delimit[i+1] + 1]
        df_uncertain = pd.concat([df_uncertain,pd.DataFrame(df2)], ignore_index=True)
        delimit_uncertain.append([delimit[i],delimit[i+1]])
    else:
        num_certain += 1
        df2 = train.iloc[delimit[i] + 1:delimit[i+1] + 1]
        df_certain = pd.concat([df_certain,pd.DataFrame(df2)], ignore_index=True)
print num_certain
print num_uncertain
df_certain = pd.concat([df_certain,df_uncertain], ignore_index=True)
print 'part good'
de_index = list(np.random.choice(len(delimit_uncertain),num_certain  - num_uncertain))
for i in de_index:
    df2 = train.iloc[delimit_uncertain[i][0]+1 : delimit_uncertain[i][1] + 1]
    df_certain = pd.concat([df_certain,pd.DataFrame(df2)], ignore_index=True)
    num_uncertain += 1
        
    
   