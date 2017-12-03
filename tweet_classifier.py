import re

import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB

RE_NUMBERS = re.compile(r'[0-9]+')
RE_NOT_LETTERS = re.compile(r'[^a-zA-Z]+')
RE_SPACES = re.compile(r'[^\S\f\t\n\r]+')

STOPWORDS = {word for word in nltk.corpus.stopwords.words('english')}
STEM = nltk.stem.PorterStemmer()


def train_classify_database(tweets_data, verbose=False):
    """
    Trains and classifies a tweet database, the database consists of a list of triples. Triples are composed by the
    tweet date, text and class, if the class is None, the tweet is not classified. The used classifier is a Multinomial
    Naive Bayes.

    This method returns a list of classes of all tweets (including the already classified tweets) and the best
    classifier of the cross validation.
    """
    classified = [tweet_data for tweet_data in tweets_data if tweet_data[2] is not None]
    if verbose:
        print(f'classified tweets: {len(classified)}')

    classified_texts = [tweet_data[1] for tweet_data in classified]
    tweet_vectorizer = CountVectorizer(strip_accents='ascii', stop_words='english')
    tweet_vectorizer.fit(classified_texts)

    instances = tweet_vectorizer.transform(classified_texts)
    classes = np.array([tweet_data[2] for tweet_data in classified])
    if verbose:
        print(f'instance size: {instances.shape}')

    folds = 5
    skf = StratifiedKFold(n_splits=folds, shuffle=True)
    if verbose:
        print(f'cross validation with {folds} folds')

    best_classifier = None
    best_classifier_score = 0
    for i, (train_indices, test_indices) in enumerate(skf.split(instances, classes)):

        if verbose:
            print(f'fold {i}')

        classifier = MultinomialNB()

        train_instances = instances[train_indices]
        train_classes = classes[train_indices]

        test_instances = instances[test_indices]
        test_classes = classes[test_indices]

        classifier.fit(train_instances, train_classes)
        score = classifier.score(test_instances, test_classes)

        if verbose:
            print(f'score: {score}')

        if score > best_classifier_score:
            best_classifier = classifier
            best_classifier_score = score

            if verbose:
                print('best')

    if verbose:
        print('classify all tweets with best classifier')

    tweets_texts = [tweet_data[1] for tweet_data in tweets_data]
    tweets_instances = tweet_vectorizer.transform(tweets_texts)
    tweets_classes = best_classifier.predict(tweets_instances)

    return [tweets_classes[i] for i in range(len(tweets_data))], best_classifier
