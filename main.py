import csv
import os
import random
from datetime import datetime

from tweet_classifier import analyse_tweet_database, classify_tweet_database
from tweet_collector import collect_event_tweets
from tweet_plot import plot_collected_tweets_per_day, plot_tweets_classes_per_day, plot_tweets_sentiment_per_day, \
    plot_tweets_class_sentiment_per_day

print('after import')

DATABASE_PATH = './database/'


def collect_save_tweets(filename, since, until, results_per_day, location, location_radius):
    """
    Collects and saves tweets in a csv file inside the database folder.
    """
    if not os.path.exists(DATABASE_PATH):
        os.makedirs(DATABASE_PATH)
    with open(DATABASE_PATH + filename, 'w', newline='', encoding='utf8') as table:
        writer = csv.writer(table, delimiter=';')

        def on_some_tweets_collected(tweets):
            for tweet in tweets:
                writer.writerow([str(tweet.date), tweet.text.replace(';', ',')])

        collect_event_tweets(since, until, results_per_day, location, location_radius,
                             on_some_collected=on_some_tweets_collected, verbose=True)


def load_tweets_file(filename):
    """
    Reads the tweets in the received csv file name inside the database folder.
    """
    tweets = []
    with open(DATABASE_PATH + filename, 'r', newline='', encoding='utf8') as table:
        reader = csv.reader(table, delimiter=';')
        for i, row in enumerate(reader):
            clazz = row[2] if len(row) == 3 else None
            tweets.append((datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), row[1], clazz))
    return tweets


saved_tweets = load_tweets_file('aurora.csv')
# saved_tweets = load_tweets_file('london_bridge.csv')
saved_tweets_classes, classifier = classify_tweet_database(saved_tweets, verbose=True)
saved_tweets_sentiments = analyse_tweet_database(saved_tweets)

plot_collected_tweets_per_day(saved_tweets)
plot_tweets_classes_per_day(saved_tweets, saved_tweets_classes, {'0': 'other tweets', '1': 'bridge attack'})
plot_tweets_sentiment_per_day(saved_tweets, saved_tweets_sentiments)
plot_tweets_class_sentiment_per_day(saved_tweets, saved_tweets_classes, saved_tweets_sentiments,
                                    {'0': 'other tweets', '1': 'bridge attack'})
