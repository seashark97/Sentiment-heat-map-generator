import string
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from sklearn.externals import joblib

def negate_gram(document):
    doclist = document.split()
    review = []
    negated = False
    for n in range(len(doclist)):
        if doclist[n] == 'not' and not negated and len(doclist)>n+1:
            review.append(doclist[n]+'_'+doclist[n+1])
            negated = True
        elif not negated:
            review.append(doclist[n])
        elif negated:
            negated = False
    return ' '.join(review)

stemmer = PorterStemmer()

Vectorizer = joblib.load('Saved_Steps/Vectorizer.pkl')
Selector = joblib.load('Saved_Steps/Selector.pkl')
Classifier = joblib.load('Saved_Steps/Classifier.pkl')

def classify_tweet(tweet):
    s = filter(lambda x: x in string.printable, tweet)
    stemmed = ''

    for word in word_tokenize(s):
        stemmed +=  stemmer.stem(word) + ' '
    stemmed = negate_gram(stemmed)
    x = Vectorizer.transform([stemmed])
    x = Selector.transform(x)
    return Classifier.predict(x)[0]