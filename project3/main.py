from question_extract import Question_Extract
from find_answer import Find_Answer


def main():
    for Q_ID in range(89, 321):
        print Q_ID
        File_Path = 'C:\Users\Ziyan Liu\Desktop\Cornell\Study\cs4740\prj3\\question.txt'
        WList = Question_Extract(Q_ID, File_Path)
        Answers = Find_Answer(Q_ID, WList)

        #print Answers

        with open('answer.txt', 'a') as f:
            f.write(Answers[0]+'\n')
            f.write(Answers[1]+'\n')
            f.write(Answers[2]+'\n')
            f.write(Answers[3]+'\n')
            f.write(Answers[4]+'\n')

    return None


main()
