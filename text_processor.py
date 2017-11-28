import csv
import nltk
import re

import numpy as np


RE_NUMBERS = re.compile(r'[0-9]+')
RE_NOT_LETTERS = re.compile(r'[^a-zA-Z]+')
RE_SPACES = re.compile(r'[^\S\f\t\n\r]+')

STOPWORDS = {word for word in nltk.corpus.stopwords.words('english')}
STEMMER = nltk.stem.PorterStemmer()


def wipe_doc(doc):
    """
    Wipes the received document string, removing non letters characters and stopwords, transforms
    numbers in 'NUM' str and applies stemming in remaining words.
    """
    doc = RE_NUMBERS.sub(' NUM ', doc)
    doc = RE_NOT_LETTERS.sub(' ', doc)
    doc = RE_SPACES.sub(' ', doc)
    words = doc.lower().strip().split(' ')
    words = [STEMMER.stem(word) for word in words if word not in STOPWORDS]
    return words


def generate_vocabulary(wiped_corpus):
    """
    Creates the indexed vocabulary of the received corpus.
    """
    words = {word for doc in wiped_corpus for word in doc}
    vocabulary = {word: i for i, word in enumerate(words)}
    return vocabulary


def build_instance(wiped_doc, vocabulary):
    """
    Builds the numpy instance of the doc based on the vocabulary.
    """
    instance = np.zeros(len(vocabulary), dtype=np.int8)
    for word in wiped_doc:
        if word in vocabulary:
            instance[vocabulary[word]] = 1
    return instance


def corpus_to_instances(corpus):
    """
    Generates numpy instances for corpus documents.
    """
    wiped_corpus = [wipe_doc(doc) for doc in corpus]
    vocabulary = generate_vocabulary(wiped_corpus)
    return [build_instance(wiped_doc, vocabulary) for wiped_doc in wiped_corpus]


def test():
    '''
    Tests the current file elements.
    '''
    print(f'testing {__file__}')
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

    wiped_tweets = [wipe_doc(tweet) for tweet in tweets]
    vocabulary = generate_vocabulary(wiped_tweets)
    instances = [build_instance(clean_tweet, vocabulary) for clean_tweet in wiped_tweets]

    print(f'vocabulary size: {len(vocabulary)}')
    print()

    print('tweet - clean - instance | comparison')
    for i in range(len(tweets)):
        print(tweets[i])
        print(wiped_tweets[i])
        print(''.join(str(exists) for exists in instances[i]))
        print()

    print('running with all in one method')
    print(corpus_to_instances(tweets))


if __name__ == '__main__':
    test()
