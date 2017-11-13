from tweet_collector import collect_tweet_by_ids

tweets_ids = []
with open('dataset\\aurora_overall.csv') as table:
    table.readline()
    for line in table:
        tweets_ids.append(line.split(',')[1])
tweets = collect_tweet_by_ids('consumer_access_keys.txt', tweets_ids, verbose=True)
print()