import nltk
import random
from nltk.corpus import movie_reviews, stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.classify import ClassifierI

from statistics import mode

import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

stop_words = set(stopwords.words("English"))
# adding unnecessary signs and symbols
for i in range(0,256):
    stop_words.add(chr(i))

# category( pos/neg )
documents = []

# pickle this shit
for category in movie_reviews.categories():
    for fileid in movie_reviews.fileids(category):
        word_list = list(movie_reviews.words(fileid))
        check_list = []
        for word in word_list:
            if word not in stop_words and not word.isdigit():
                check_list.append(word)
        documents.append((check_list,category))

# print(documents[0])

random.shuffle(documents)

all_words = []

for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())[:3000]


def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


# print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]

training_set = featuresets[:1900]
testing_set = featuresets[1900:]

classifier = nltk.NaiveBayesClassifier.train(training_set)

# classifier_f = open("naivebayes.pickle","rb")
# classifier = pickle.load(classifier_f)
# classifier_f.close()


print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
# classifier.show_most_informative_features(15)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set)) * 100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:",
      (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:",
      (nltk.classify.accuracy(SGDClassifier_classifier, testing_set)) * 100)

# SVC_classifier = SklearnClassifier(SVC())
# SVC_classifier.train(training_set)
# print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set)) * 100)


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self.classifiers = classifiers

    def classify(self, features):
        votes = []
        for cls in self.classifiers:
            v = cls.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for cls in self.classifiers:
            v = cls.classify(features)
            votes.append(v)
        choice = votes.count(mode(votes))
        confid = choice / len(votes)
        return confid


voted_classifier = VoteClassifier(classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier,
                                  SGDClassifier_classifier,
                                  LinearSVC_classifier,
                                  NuSVC_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set)) * 100)

print("Labeled test0 as : ",testing_set[0][1])
print("Classification test0 : ", voted_classifier.classify(testing_set[0][0]))
print("Confidence : ", voted_classifier.confidence(testing_set[0][0]))

print("Labeled test1 as : ",testing_set[1][1])
print("Classification test1: ", voted_classifier.classify(testing_set[1][0]))
print("Confidence : ", voted_classifier.confidence(testing_set[1][0]))

print("Labeled test2 as : ",testing_set[2][1])
print("Classification test2: ", voted_classifier.classify(testing_set[2][0]))
print("Confidence : ", voted_classifier.confidence(testing_set[2][0]))

print("Labeled test3 as : ",testing_set[3][1])
print("Classification test3: ", voted_classifier.classify(testing_set[3][0]))
print("Confidence : ", voted_classifier.confidence(testing_set[3][0]))
