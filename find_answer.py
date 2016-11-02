# This function finds answer based on extracted information of the questions
import glob
import os

def Find_Answer(Q_ID, WList):

    # arrange documents texts
    Doc_Path = "C:\Users\Ziyan Liu\Desktop\Cornell\Study\cs4740\prj3\doc_dev\\" + str(Q_ID) + '\\*'
    Texts = []
    GotIt = False

    for fileName in glob.glob(Doc_Path):
        with open(fileName, 'r') as file:
            lines = file.read()
            texts = lines.split()

            # find where the key word is
            for i in texts:
                if i in WList:
                    pos = texts.index(i)
                    first_answer = texts[1] + ' ' + texts[3] + ' ' + ' '.join(texts[pos:pos+3]) + ' (for top-ranked guess)'
                    second_answer = texts[1] + ' ' + texts[3] + ' ' + ' '.join(texts[pos-3:pos]) + ' (for second guess)'
                    third_answer = texts[1] + ' ' + texts[3] + ' ' + ' '.join(texts[pos:pos+5]) + ' (for third guess)'
                    fourth_answer = texts[1] + ' ' + texts[3] + ' ' + ' '.join(texts[pos-5:pos]) + ' (for fourth guess)'
                    fifth_answer = texts[1] + ' ' + texts[3] + ' ' + ' '.join(texts[pos-3:pos+3]) + ' (for fifth guess)'
                    GotIt = True
                    break

            if GotIt:
                break

    if not GotIt:
        second_answer = texts[1] + ' ' + texts[3] + ' ' + 'nil' + ' (for second guess)'
        third_answer = texts[1] + ' ' + texts[3] + ' ' + 'nil' + ' (for third guess)'
        fourth_answer = texts[1] + ' ' + texts[3] + ' ' + 'nil' + ' (for fourth guess)'
        first_answer = texts[1] + ' ' + texts[3] + ' ' + 'nil' + ' (for top-ranked guess)'
        fifth_answer = texts[1] + ' ' + texts[3] + ' ' + 'nil' + ' (for fifth guess)'

    return first_answer, second_answer, third_answer, fourth_answer, fifth_answer
