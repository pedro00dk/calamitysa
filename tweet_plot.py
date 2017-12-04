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


def plot_tweets_sentiment_per_day(tweets_data, tweets_sentiments):
    """
    Plots the tweets classes per day in the database.
    """
    tweets_all_data = zip(tweets_data, tweets_sentiments)
    sentiments = [sentiment for sentiment in tweets_sentiments[0].keys() if sentiment not in ['compound', 'neu']]
    dates = {}
    for tweet_data in tweets_all_data:
        date = tweet_data[0][0].date()
        if date not in dates:
            dates[date] = [0, {sentiment: 0 for sentiment in sentiments}]
        dates[date][0] += 1
        for sentiment in sentiments:
            dates[date][1][sentiment] += tweet_data[1][sentiment]

    for date in dates:
        for sentiment in sentiments:
            dates[date][1][sentiment] /= dates[date][0]

    sorted_dates_sentiments = sorted(dates.items())

    plt.clf()

    indices = np.arange(len(sorted_dates_sentiments))

    for sentiment in sentiments:
        plt.plot(indices, [sents[1][sentiment] for date, sents in sorted_dates_sentiments], label=sentiment)

    plt.xlabel('Days')
    plt.ylabel('Sentiment means')
    plt.title('Tweets sentiments')
    plt.xticks(indices, [str(date) for date, classes in sorted_dates_sentiments], rotation='vertical')
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_tweets_class_sentiment_per_day(tweets_data, tweets_classes, tweets_sentiments, class_labels=None):
    """
    Plots the tweets classes per day in the database.
    """

    tweets_all_data = zip(tweets_data, tweets_classes, tweets_sentiments)

    classes = {clazz for clazz in tweets_classes}
    sentiments = [sentiment for sentiment in tweets_sentiments[0].keys() if sentiment not in ['compound', 'neu']]

    dates = {}
    for tweet_data in tweets_all_data:
        date = tweet_data[0][0].date()
        if date not in dates:
            dates[date] = {clazz: [0, {sentiment: 0 for sentiment in sentiments}] for clazz in classes}
        dates[date][tweet_data[1]][0] += 1
        for sentiment in sentiments:
            dates[date][tweet_data[1]][1][sentiment] += tweet_data[2][sentiment]

    for date in dates:
        for clazz in classes:
            for sentiment in sentiments:
                dates[date][clazz][1][sentiment] /= dates[date][clazz][0]

    sorted_dates_sentiments = sorted(dates.items())

    plt.clf()

    indices = np.arange(len(sorted_dates_sentiments))

    for clazz in classes:
        class_label = class_labels[clazz] if class_labels is not None else clazz
        for sentiment in sentiments:
            plt.plot(indices, [sents[clazz][1][sentiment] for date, sents in sorted_dates_sentiments],
                     label=class_label + ' ' + sentiment)

    plt.xlabel('Days')
    plt.ylabel('Sentiment means')
    plt.title('Tweets sentiments per class')
    plt.xticks(indices, [str(date) for date, classes in sorted_dates_sentiments], rotation='vertical')
    plt.legend()

    plt.tight_layout()
    plt.show()
