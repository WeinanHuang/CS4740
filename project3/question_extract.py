# This funciton extract key words in questions
def Question_Extract(Q_ID, File_Path):
    W_to_remove = ['the', 'a', 'what', 'where', 'how', 'who',
     "where's", "what's", "how's", "who's",
     "where're", "what're", "how're", "who're"]

    f = open(File_Path)
    # pos1: whether we have identified the part corresponding to the question
    # pos2: whether we have extract the question
    pos1 = False
    pos2 = False
    for line in f:
        if pos1:
            if line == '<desc> Description:\n':
                pos2 = True
                continue
            if pos2:
                qusetion = line
                pos1 = False
                pos2 = False

        if line == '<num> Number: ' + str(Q_ID) + '\n':
            pos1 = True
            continue

    # extract information from question
    WList = qusetion.split()
    WList[-1] = WList[-1][:-1] # remove question mark in the last token

    for i in WList:
        if i.lower() in W_to_remove:
            WList.remove(i)

    return WList

# test case
# File_Path = 'C:\Users\Ziyan Liu\Desktop\Cornell\Study\cs4740\prj3\\question.txt'
# Q_ID = 111
#
# a = Question_Extract(Q_ID, File_Path)
# print(a)
