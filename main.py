'''
convert files from
commonmark, docbook, docx, epub, haddock, html, json, latex, markdown,
markdown_github, markdown_mmd, markdown_phpextra, markdown_strict, mediawiki, native, odt, opml, org, rst, t2t, textile, twiki

'''


import urllib.request
#import pypandoc
import sys
import time
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import urllib.request
from bs4 import BeautifulSoup


stop_words = set(stopwords.words('english'))

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def valid_link_text(url,query_flag = 1):
    try:
        cleaned = urllib.request.urlopen(url)
    except urllib.error.URLError :
        print("404 : Page Not Found ")
        return False
    if query_flag == 1 :
        soup = BeautifulSoup(cleaned,"lxml")

        data = soup.findAll(text=True)
        result =  filter(visible,data)
        time.sleep(5)		# get_result
        return list(result)
    else:
        return True

def save_data(data,data_name=None,question_name=None,from_extension = None,to_extension = None,):
    if from_extension!=None:
        print("conv")

    elif to_extension!=None:
        number = data_name
        if question_name!=None:
            number = "blog"
        text_file = open("texts/"+"answer_words-"+number+to_extension,"w")
        text_file.write(question_name)
        text_file.write("\n")
        # ignore top 10 lines
        break_point = ["Sitemap:","Related Questions"]

        for line in data[10:] :
            if line in break_point:
                break               # setting temperory break-point
            words = word_tokenize(line)

            for word in words :
                if word not in stop_words:
                    content = re.sub('\s+', ' ', word)  # condense all whitespace
                    content = re.sub('[^A-Za-z ]+', '', content)  # remove non-alpha chars
                    text_file.write(str(content).lower())
                    text_file.write("\n")

        text_file.close()
    else:
        print(" Invalid conversion ! ")

def get_answer_blog():
    start_url = input("Enter answer / blog url :")

    text_data = valid_link_text(start_url)
    if text_data == False:
        return

    save_data(text_data,question_name=start_url,to_extension=".txt")

    print("grabbed answer / blog successfully")

def get_latest_questions(url):
    raw = urllib.request.urlopen(url)
    soup = BeautifulSoup(raw, "lxml")

    data = soup.findAll('span',{"class":"rendered_qtext"})
    result = filter(visible, data)
    time.sleep(2)       # get_result
    data  = list(result)
    question_bag = []
    for it in data:
        txt = str(it.text)
        txt.lower()
        if "?" in txt:
            txt = txt[:-1].replace(' ','-')             # get re here to refine
            question_bag.append("http://quora.com/"+txt)
    print("grabbed question_bag successfully ")
    return question_bag


def get_latest_answers():

    start_url= input("Enter profile link :")

    text_data = valid_link_text(start_url,query_flag=0)
    if text_data == False:
        return
    questions = get_latest_questions(start_url)
    size = len(questions)
    for question in range(size):
        validity = valid_link_text(questions[question])
        print(questions[question])
        print("got - #"+str(question+1))
        if validity != False:
            save_data(validity,data_name=str(question+1),to_extension=".txt",question_name=questions[question])
        else:
            print("Validate question_bag link index #"+str(question+1))
    print("grabbed answers successfully")


if __name__ == "__main__":
    if len(sys.argv)==2:
        if sys.argv[1] == "pick_profile":
            get_answer_blog()
        elif sys.argv[1] == "pick_answer":
            get_latest_answers()
    else:
        print("pick_profile - pick answers from profile")
        print("pick_answer - pick answer directly")
