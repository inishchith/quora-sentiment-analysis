# from nltk.corpus import stopwords
# from nltk import word_tokenize
import os,glob
import matplotlib.pyplot as plt

scores={-5:[],-4:[],-3:[],-2:[],-1:[],1:[],2:[],3:[],4:[],5:[]}

def classify_test_scores():
    with open("AFINN-111.txt") as af :
        data = af.readlines()
    for score in data:
        parts = score.split()
        if len(parts)==2:
            try:
                scores[int(parts[-1])].append(parts[0][:])
            except ValueError or KeyError:
                pass

def get_scores(data):
    pos_sum ,pos_length,neg_sum ,neg_length = 0,0,0,0
    for word in data :
        for score in range(-5,6):
            if score!=0 and word[:-1] in scores[score]:
                if score>0:
                    pos_length+=1
                    pos_sum += score
                else:
                    neg_length+=1
                    neg_sum += score
    outoff_words_score = (neg_length+pos_length)*5
    print(pos_sum,pos_length,neg_sum,neg_length)
    percet_pos = (pos_sum*100)/outoff_words_score
    percet_neg = (abs(neg_sum)*100)/outoff_words_score
    percet_neut = 100 - (percet_neg+percet_pos)
    # print([percet_pos,percet_neg,percet_neut])
    return [percet_pos,percet_neg,percet_neut]


def plot_pie(sizes):
    explode = (0.1,0.0,0.0)
    labels = ["Positive","Negative","Netutral"]
    colors = ['yellowgreen','lightcoral', 'skyblue']
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, colors=colors,explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def start_process(blog=None):
    file = open("analysis_report.md","w")
    file.write("### Results \n\n")
    os.chdir("texts")
    list_of_answers = [file for file in glob.glob("*.txt")]

    for answers in list_of_answers:
        if "blog" in answers:
            with open(answers) as f:
                content = f.readlines()
            score = get_scores(content[1:])
            file.write(str("* ")+str(content[0])+"\n")
            file.write(str("> Positive : " + str(score[0]) + " % \n\n> Negative : " + str(score[1]) + "%\n\n> Neutral : " + str(score[2]))+" %\n")
            plot_pie(score)
            break
        else:
            with open(answers) as f:
                content = f.readlines()

            score = get_scores(content[1:])

            file.write(str(content[0])+"\n")
            file.write(str("> Positive : " + str(score[0]) + " % \n\n> Negative : " + str(score[1]) + "%\n\n> nNutral : " + str(score[2]))+" %\n")
    file.close()

if __name__ == "__main__":
    classify_test_scores()
    start_process(blog=True)