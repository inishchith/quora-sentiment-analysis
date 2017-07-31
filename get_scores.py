
from nltk.corpus import stopwords
from nltk import word_tokenize
import os,glob




#def get_text():

scores={-5:[],-4:[],-3:[],-2:[],-1:[],1:[],2:[],3:[],4:[],5:[]}

def classify_test_scores():
    with open("AFINN-111.txt") as af :
        data = af.readlines()
    for score in data:
        parts = score.split()
        if len(parts):
            try:
                scores[int(parts[-1])].append(parts[0])
            except ValueError or KeyError:
                pass
    print(scores)


#def get_scores():


def start_process():
    file = open("analysis_report.md","w")
    # file.write("### Results \n\n")
    os.chdir("texts")
    list_of_answers = [file for file in glob.glob("*.txt")]


    for answers in list_of_answers:
        with open(answers) as f:
            content = f.readlines()
        print(content)
        # file.write(str(answers))





if __name__ == "__main__":
    #start_process()
    classify_test_scores()
    #get_scores()