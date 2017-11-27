import csv
import datetime

from dateutil.relativedelta import relativedelta
from tweet_collector import *


def collect_event_tweets(since, until, results_per_day=1000, location=None, location_radius=None,
                         verbose=False):
    """
    Helps the tweet collect by getting then per day in a received time interval.
    """
    if verbose:
        print('collecting tweets of event per day')

    tweets = []
    current_date = datetime.date(*(int(i) for i in since.split('-')))
    until_date = datetime.date(*(int(i) for i in until.split('-')))

    while current_date != until_date:
        next_date = current_date + relativedelta(days=1)
        if verbose:
            print(f'current day: {str(current_date)}')

        args = QueryArgs(
            results=results_per_day,
            location=location,
            location_radius=location_radius,
            since=str(current_date),
            until=str(next_date))

        current_day_tweets = TweetAdvancedQuery().query(args, verbose=verbose)
        tweets.extend(current_day_tweets)

        current_date = next_date

    return tweets


def test():
    '''
    Tests the current file elements.
    '''
    print(f'testing {__file__}')
    tweets = collect_event_tweets(results_per_day=30, since='2012-07-18', until='2012-07-23', location='Denver, CO',
                                  location_radius=200, verbose=True)
    print('tweets texts:')
    for tweet in tweets:
        print(tweet.text)


if __name__ == '__main__':
    test()
