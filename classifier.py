import csv
import string
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn import svm
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.cross_validation import KFold, cross_val_score
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize

tweet_text = []
tweet_sentiment = []

unique_sentiments = {'positive':0, 'negative':1, 
            'neutral':2, 'objective':2, 'objective-OR-neutral':2}

print 'Sentiments are mapped as: %s \n\n' % (unique_sentiments,)

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
sent = {'positive':0, 'negative':0, 
            'neutral':0, 'objective':0, 'objective-OR-neutral':0}
length = 0
with open('tweeti-b-train.tsv','rb') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')

    for row in tsvin:
    	s = filter(lambda x: x in string.printable, row[3])
        stemmed = ''
        
        # for word in word_tokenize(s):
        #    	stemmed +=  stemmer.stem(word) + ' '
        stemmed = negate_gram(s)
        tweet_text.append(stemmed)
        tweet_sentiment.append(unique_sentiments[row[2]])
        sent[row[2]] += 1
        length += 1
with open('tweeti-b-test.tsv','rb') as tsvin:
    tsvin = csv.reader(tsvin, delimiter='\t')

    for row in tsvin:
    	s = filter(lambda x: x in string.printable, row[3])
        stemmed = ''
        
        # for word in word_tokenize(s):
        #    	stemmed +=  stemmer.stem(word) + ' '
        stemmed = negate_gram(s)
        tweet_text.append(stemmed)
        tweet_sentiment.append(unique_sentiments[row[2]])
        sent[row[2]] += 1
        length += 1
print sent
hv = HashingVectorizer(ngram_range=(1,3), binary=False, non_negative=True)
X = hv.fit_transform(tweet_text)

current_max = [0,0]
for n in range(0, 100000, 5000):
    selector = SelectKBest(chi2, k=n)
    X_reduced = selector.fit_transform(X, tweet_sentiment)
    clf = BernoulliNB()
    K_Fold = KFold(n=length, n_folds=19)
    cv_scores = cross_val_score(clf, X_reduced, tweet_sentiment, cv=K_Fold, n_jobs=1)
    average_score = sum(cv_scores)/19
    if average_score > current_max[0]:
        current_max[0]=average_score
        current_max[1]=n
    print 'Accuracy: %f    Number of features: %d' % (average_score, n)
print 'Best number of features: %d    Accuracy: %f' % (current_max[1], current_max[0])