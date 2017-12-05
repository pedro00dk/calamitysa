import re

import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import precision_recall_fscore_support
# from sklearn.svm import SVC
# from sklearn.neural_network import MLPClassifier

RE_NUMBERS = re.compile(r'[0-9]+')
RE_NOT_LETTERS = re.compile(r'[^a-zA-Z]+')
RE_SPACES = re.compile(r'[^\S\f\t\n\r]+')

STOPWORDS = {word for word in nltk.corpus.stopwords.words('english')}
STEM = nltk.stem.PorterStemmer()


def classify_tweet_database(tweets_data, verbose=False):
    """
    Trains and classifies a tweet database, the database consists of a list of triples. Triples are composed by the
    tweet date, text and class, if the class is None, the tweet is not classified. The used classifier is a Multinomial
    Naive Bayes.

    This method returns a list of classes of all tweets (including the already classified tweets) and the best
    classifier of the cross validation.
    """
    print('start text processing')
    processed_tweets_data = []
    for tweet_data in tweets_data:
        tokens = RE_SPACES.split(RE_NOT_LETTERS.sub(' ', RE_NUMBERS.sub(' num ', tweet_data[1])))
        processed_tokens = [STEM.stem(token) for token in tokens if token not in STOPWORDS]
        wiped_text = ' '.join(processed_tokens)
        processed_tweets_data.append((tweet_data[0], wiped_text, tweet_data[2]))

    classified = [tweet_data for tweet_data in processed_tweets_data if tweet_data[2] is not None]
    if verbose:
        print(f'classified tweets: {len(classified)}')

    classified_texts = [tweet_data[1] for tweet_data in classified]
    tweet_vectorizer = CountVectorizer()
    tweet_vectorizer.fit(classified_texts)

    classified_instances = tweet_vectorizer.transform(classified_texts)
    classified_classes = np.array([tweet_data[2] for tweet_data in classified])
    if verbose:
        print(f'instance size: {classified_instances.shape}')

    folds = 5
    skf = StratifiedKFold(n_splits=folds, shuffle=True)
    if verbose:
        print(f'cross validation with {folds} folds')

    best_classifier = None
    best_classifier_score = 0
    for i, (train_indices, test_indices) in enumerate(skf.split(classified_instances, classified_classes)):

        if verbose:
            print(f'fold {i}')

        classifier = MultinomialNB()
        # classifier = SVC()
        # classifier = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=2000, validation_fraction=1 / (folds - 1))

        train_instances = classified_instances[train_indices]
        train_classes = classified_classes[train_indices]

        test_instances = classified_instances[test_indices]
        test_classes = classified_classes[test_indices]

        classifier.fit(train_instances, train_classes)
        score = classifier.score(test_instances, test_classes)

        test_classes_pred = classifier.predict(test_instances)

        prfs = precision_recall_fscore_support(test_classes, test_classes_pred, average='macro')
        print('p r f s  ' + str(prfs))

        if verbose:
            print(f'score: {score}')

        if score > best_classifier_score:
            best_classifier = classifier
            best_classifier_score = score

            if verbose:
                print('best')

    if verbose:
        print('classify all tweets with best classifier')

    tweets_texts = [tweet_data[1] for tweet_data in processed_tweets_data]
    tweets_instances = tweet_vectorizer.transform(tweets_texts)
    tweets_classes = best_classifier.predict(tweets_instances)

    return [tweets_classes[i] for i in range(len(processed_tweets_data))], best_classifier


def analyse_tweet_database(tweets_data):
    print('analysing tweet sentiment')
    sid = SentimentIntensityAnalyzer()
    polarity_scores = []
    for tweet_data in tweets_data:
        polarity_scores.append(sid.polarity_scores(tweet_data[1]))
    return polarity_scores
