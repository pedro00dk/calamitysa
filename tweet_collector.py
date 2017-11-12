import math
import tweepy

def collect_tweet_by_ids(credentials_file, tweets_ids):

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
    tweets = []
    try:
        # tweeter lookup limit (100 tweets)
        for i in range(math.ceil(tweet_count / 100)):
            end_loc = min((i + 1) * 100, tweet_count)
            tweets.extend(api.statuses_lookup(tweets_ids[i * 100 : end_loc]))

    except tweepy.TweepError:
        print('error while collecting tweets, retuning the successful collected tweets')
    return tweets
    
# tweets = collect_tweet_by_ids('consumer_access_keys.txt', ['929841309082439680'])
