'''
this function take the test dataframe processed by test_process function
and return a dictionary, the key of the dictionary is the sentence number. 
The value is the dataframe of each sentence
'''

def test_sep(test):
    delimit = [-1]
    for i in range(len(test)):
        if test['token'][i] == '.' and test['pos'][i] == '.':
            delimit.append(i)
    test_dict = {}
    for i in range(len(delimit)-1):
        test_dict[i] = test.iloc[delimit[i] + 1:delimit[i+1] + 1]
    return test_dict