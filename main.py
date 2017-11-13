from tweet_collector import collect_tweet_by_ids

dataset_folder = 'dataset'
datasets_format = 'csv'
datasets = [
    'aurora_overall', 'aurora_targeted',
    'ebro_overall', 'ebro_targeted',
    'isaac_overall', 'isaac_targeted']

tweets_folder ='tweets'
for dataset in datasets:
    tweets_ids = []
    with open(f'{dataset_folder}/{dataset}.{datasets_format}') as table:
        table.readline()
        for line in table:
            tweets_ids.append(line.split(',')[1])
    tweets_ids = [*{*tweets_ids}]
    tweets = collect_tweet_by_ids('consumer_access_keys.txt', tweets_ids, verbose=True)
    with open(f'{tweets_folder}/{dataset}.txt', 'w', encoding='utf-8') as texts:
        for index, tweet in enumerate(tweets):

            texts.write(f'{index}:\n{tweet.text}\n\n')
