import matplotlib.pyplot as plt
import numpy as np


def plot_tweets_per_day(tweets_data):
    """
    Plots the number of tweets per day in the database.
    """
    dates = {}
    for tweet_data in tweets_data:
        date = tweet_data[0].date()
        if date not in dates:
            dates[date] = 0
        else:
            dates[date] += 1

    sorted_dates_count = sorted(dates.items())

    plt.clf()

    indices = np.arange(len(sorted_dates_count))

    plt.bar(indices, [count for date, count in sorted_dates_count])
    plt.xlabel('Days')
    plt.ylabel('Tweets')
    plt.title('Collected tweets')
    plt.xticks(indices, [str(date) for date, count in sorted_dates_count], rotation='vertical')

    plt.tight_layout()
    plt.show()
