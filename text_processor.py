import csv
import nltk
import re
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

RE_NUMBERS = re.compile(r'[0-9]+')
RE_NOT_LETTERS = re.compile(r'[^a-zA-Z]+')
RE_SPACES = re.compile(r'[^\S\f\t\n\r]+')

STOPWORDS = {word for word in nltk.corpus.stopwords.words('english')}
STEMMER = nltk.stem.PorterStemmer()


def clean_text(text):
    """
    Transform all numbers in the ' NUM ' text, removes non letters characters, stopwords, apply
    stemming in all restant words.
    """
    text = RE_NUMBERS.sub(' NUM ', text)
    text = RE_NOT_LETTERS.sub(' ', text)
    text = RE_SPACES.sub(' ', text)
    words = text.lower().strip().split(' ')
    words = [STEMMER.stem(word) for word in words if word not in STOPWORDS]
    return words


def build_vocabulary(words_list):
    """
    Builds the indexed vocabulary of the received words list.
    """
    words_set = {word for words in words_list for word in words}
    words_index = {word: index for index, word in enumerate(words_set)}
    return words_index


def build_instance(words, vocabulary):
    """
    Creates the instance of the received words based in the vocabulary.
    """
    instance = [0] * len(vocabulary)
    for word in words:
        if word in vocabulary:
            instance[vocabulary[word]] = 1
    return instance


def test():
    '''
    Tests the current file elements.
    '''
    # print(f'testing {__file__}')
    tweets = [
        "Program Manager / Senior Project Manager - iTech Solutions - Greenwood Village, CO http:// jobcircle.com/z11237008 #jobcircle #jobs",
        "I'm at Gibby's (Aurora, CO ) http:// 4sq.com/LyUT4E",
        "I'm at Georgetown Lunatic Asylum (Georgetown, CO ) http:// 4sq.com/Q8kJye",
        "I'm at Whole Foods Market (Lakewood, CO ) w/ 3 others http:// 4sq.com/P1CR7W",
        "I'm at Olde Town Arvada (Arvada, CO ) http:// 4sq.com/SIpxsO",
        "Fourmile Fire survivors to share experience, advice with Larimer County - http:// bit.ly/Pjrs7f #FortCollins #Colorado",
        "I'm at Total Escape Games (Broomfield, CO ) http:// 4sq.com/M9HvkD",
        "I'm at MAD Greens - Inspired Eats (Downtown/16th Street Mall) (Denver, CO ) http:// 4sq.com/Mtd5KJ",
        "I'm at Independent Records & Video (Denver, CO ) http:// 4sq.com/NAfnZm",
        "Adults set to step out in 'Dance Found' at Ballet Nouveau Colorado in Broomfield - http:// bit.ly/MJ7WwD #Broomfield #Colorado",
        "I'm at Yard House (Lone Tree, Co ) http:// 4sq.com/Lt41mS"]

    clean_tweets = [clean_text(tweet) for tweet in tweets]
    vocabulary = build_vocabulary(clean_tweets)
    instances = [build_instance(clean_tweet, vocabulary) for clean_tweet in clean_tweets]

    # print(f'vocabulary size: {len(vocabulary)}')
    print()

    print('tweet - clean - instance | comparison')
    for i in range(len(tweets)):
        print(tweets[i])
        print(clean_tweets[i])
        print(''.join(str(exists) for exists in instances[i]))
        print()

def test_2():
    rows = []
    with open('database/aurora.csv', newline='', encoding='utf-8') as csvfile:
        for row in csvfile.readlines():
            rows += [row.split(';')]

    # Cleaning tweets
    # if tweet is labeled, remove '\r\n'
    tweets = []
    for row in rows:
        if len(row) == 3:
            tweets += [[row[0], ' '.join(clean_text(row[1])), row[2].replace('\r\n','')]]
        elif len(row) == 2:
            tweets += [[row[0], ' '.join(clean_text(row[1]))]]
        else:
            tweets += [[row[0], '']]
    # tweets_text = [tweet[1] for tweet in tweets]

    tweets_training_set = [tweet for tweet in tweets if len(tweet) == 3]
    tweets_training_set_text = [tweet[1] for tweet in tweets_training_set]
    tweets_training_set_target = [tweet[2] for tweet in tweets_training_set]
    print('Tweets\' set size: ' + str(len(tweets)))

    # Bag of words
    count_vect = CountVectorizer()
    x_train_counts = count_vect.fit_transform(tweets_training_set_text)
    print(x_train_counts.shape)

    # Machine Learning
    print('Training Naive Bayes (NB) classifier on training data.')
    clf = MultinomialNB().fit(x_train_counts, tweets_training_set_target)

    # Building a pipeline: We can write less code and do all of the above, by building a pipeline as follows:
    # The names ‘vect’ and ‘clf’ are arbitrary but will be used later.
    # We will be using the 'text_clf' going forward.
    print('Building pipeline')
    text_clf = Pipeline([('vect', CountVectorizer()), ('clf', MultinomialNB())])
    text_clf = text_clf.fit(tweets_training_set_text, tweets_training_set_target)

    # Performance of NB Classifier (on training set)
    # Por enquanto testando no conjunto de treino hehe
    print('Checking accuracy')
    predicted = text_clf.predict(tweets_training_set_text)
    acc = np.mean(predicted == tweets_training_set_target)
    print('acc: ' + str(acc))

if __name__ == '__main__':
    # test()
    test_2()
