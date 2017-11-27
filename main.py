import csv
import os

from event_collector import collect_event_tweets


DATABASE_PATH = './database/'


def collect_save_tweets(filename, since, until, results_per_day, location, location_radius):
    """
    Collects and saves tweets in a csv file
    """
    aurora_tweets = collect_event_tweets(since, until, results_per_day, location, location_radius, verbose=True)

    if not os.path.exists(DATABASE_PATH):
        os.makedirs(DATABASE_PATH)
    with open(DATABASE_PATH + filename, 'w', newline='') as table:
        spamwriter = csv.writer(table, delimiter=';')
        for tweet in aurora_tweets:
            spamwriter.writerow([str(tweet.date), tweet.text.replace(';', ',')])


collect_save_tweets('aurora.csv', '2012-07-19', '2012-08-19', 5, 'Denver, CO', location_radius=200)
