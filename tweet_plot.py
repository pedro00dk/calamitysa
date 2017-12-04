import matplotlib.pyplot as plt
import numpy as np


def plot_collected_tweets_per_day(tweets_data):
    """
    Plots the number of tweets per day in the database.
    """
    dates = {}
    for tweet_data in tweets_data:
        date = tweet_data[0].date()
        if date not in dates:
            dates[date] = 1
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


def plot_tweets_classes_per_day(tweets_data, tweets_classes, class_labels=None):
    """
    Plots the tweets classes per day in the database.
    """
    tweets_all_data = zip(tweets_data, tweets_classes)
    classes = {clazz for clazz in tweets_classes}
    dates = {}
    for tweet_data in tweets_all_data:
        date = tweet_data[0][0].date()
        if date not in dates:
            dates[date] = {clazz: 0 for clazz in classes}
        dates[date][tweet_data[1]] += 1

    sorted_dates_classes = sorted(dates.items())

    plt.clf()

    indices = np.arange(len(sorted_dates_classes))

    for clazz in sorted(classes):
        class_label = class_labels[clazz] if class_labels is not None else clazz
        plt.bar(indices, [classes[clazz] for date, classes in sorted_dates_classes], label=class_label)

    plt.xlabel('Days')
    plt.ylabel('Tweets')
    plt.title('Tweets classes')
    plt.xticks(indices, [str(date) for date, classes in sorted_dates_classes], rotation='vertical')
    plt.legend()

    plt.tight_layout()
    plt.show()
