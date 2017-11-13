import math
import tweepy

def collect_tweet_by_ids(credentials_file, tweets_ids, verbose=False):

    # accessing credentials
    with open(credentials_file) as keys:
        consumer_key = keys.readline().strip()
        consumer_secret = keys.readline().strip()
        access_key = keys.readline().strip()
        access_secret = keys.readline().strip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    tweet_count = len(tweets_ids)
    if verbose:
        print(f'tweet count: {tweet_count}')
    tweets = []
    try:
        # tweeter lookup limit (100 tweets)
        for i in range(math.ceil(tweet_count / 100)):
            frm, to = end_loc = i * 100, min((i + 1) * 100, tweet_count)
            if verbose:
                print(f'collecting ({frm}) -> ({to - 1})')
            tweets.extend(api.statuses_lookup(tweets_ids[frm : to]))

    except tweepy.TweepError:
        print('error while collecting tweets, retuning the successful collected tweets')

    return tweets
