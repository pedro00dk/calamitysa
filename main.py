import csv
import os
import text_processor

from datetime import datetime
from tweet_collector import collect_event_tweets
from sklearn.naive_bayes import MultinomialNB


DATABASE_PATH = './database/'


def collect_save_tweets(filename, since, until, results_per_day, location, location_radius):
    """
    Collects and saves tweets in a csv file inside the database folder.
    """
    if not os.path.exists(DATABASE_PATH):
        os.makedirs(DATABASE_PATH)
    with open(DATABASE_PATH + filename, 'w', newline='', encoding='utf8') as table:
        spamwriter = csv.writer(table, delimiter=';')
        def on_some_tweets_collected(tweets):
            for tweet in tweets:
                spamwriter.writerow([str(tweet.date), tweet.text.replace(';', ',')])
        
        aurora_tweets = collect_event_tweets(since, until, results_per_day, location, location_radius,
        on_some_collected=on_some_tweets_collected, verbose=True)


def load_tweets_file(filename):
    """
    Reads the tweets in the received csv file name inside the database folder.
    """
    tweets = []
    with open(DATABASE_PATH + filename, 'r', newline='', encoding='utf8') as table:
        spamreader = csv.reader(table, delimiter=';')
        for i, row in enumerate(spamreader):
            clazz = row[2] if len(row) == 3 else None
            tweets.append((datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'), row[1], clazz))
    return tweets


#collect_save_tweets('aurora.csv', '2012-07-19', '2012-08-19', 5000, 'Denver, CO', location_radius=200)
tweets = load_tweets_file('aurora.csv')

classified_tweets = [tweet for tweet in tweets if tweet[2] is not None]
wiped_classified_tweets = [(tweet[0], text_processor.wipe_doc(tweet[1]), tweet[2]) for tweet in classified_tweets]

vocabulary = text_processor.generate_vocabulary(tweet[1] for tweet in wiped_classified_tweets)

tweets_instances = [text_processor.build_instance(tweet[1], vocabulary) for tweet in wiped_classified_tweets]
tweets_classes = [tweet[2] for tweet in wiped_classified_tweets]
