import csv
import datetime
from dateutil.relativedelta import relativedelta

from tweet_collector import *

def collect_event_tweets(filepath, since, until, results_per_day=1000, location=None, location_radius=None, verbose=False):

    if verbose:
        print('collecting tweets of event per day')

    current_date = datetime.date(*(int(i) for i in since.split('-')))
    until_date = datetime.date(*(int(i) for i in until.split('-')))

    with open(filepath, 'w', newline='') as tweets_csv:
        spamwriter = csv.writer(tweets_csv, delimiter=';')

        while current_date != until_date:
            next_date = current_date + relativedelta(days=1)

            if verbose:
                print(f'current day: {str(current_date)}')

            args = QueryArgs(results=results_per_day, location=location, location_radius=location_radius, since=str(current_date), until=str(next_date))
            tweets = TweetAdvancedQuery().query(args, verbose=verbose)

            for tweet in tweets:
                spamwriter.writerow([str(current_date), tweet.text.replace(';', ',')])
            
            current_date = next_date


def main():
    collect_event_tweets('tweets/autora.csv', results_per_day=50, since='2012-07-18', until='2012-08-10', location='Denver, CO', location_radius=200, verbose=True)


if __name__ == '__main__':
    main()
