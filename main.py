import csv
import os
from datetime import datetime

from tweet_classifier import analyse_tweet_database, classify_tweet_database
from tweet_collector import collect_event_tweets
from tweet_plot import plot_tweets_per_day

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


# collect_save_tweets('aurora.csv', '2012-07-19', '2012-08-19', 5000, 'Denver, CO', location_radius=200)
saved_tweets = load_tweets_file('aurora.csv')

plot_tweets_per_day(saved_tweets)

saved_tweets_classes, classifier = classify_tweet_database(saved_tweets, verbose=True)
saved_tweets_sentiments = analyse_tweet_database(saved_tweets)
print(saved_tweets_classes)
print(saved_tweets_sentiments)
