import re
import csv
import nltk

def clean_tweet(tweet, stemmer):
	# Keep only letters on tweets
	tweet = re.sub('[^a-zA-Z]+', ' ', tweet)

	# Lower case letters
	tweet = tweet.lower()

	# Split tweet into list of words
	tweet = tweet.split(' ')

	# Remove empty values on beginning and end
	tweet = tweet[1:len(tweet) - 1]

	# Apply stemming to words
	tweet = [stemmer.stem(word) for word in tweet]

	return tweet

def filter_vocabulary(vocabulary, stopwords, stemmer):
	# Remove stopwords
	vocabulary = [word for word in vocabulary if word not in stopwords]

	# Apply stemming
	vocabulary = [stemmer.stem(word) for word in vocabulary]

	return vocabulary

def main():
	ENGLISH_STOPWORDS = {word for word in nltk.corpus.stopwords.words('english')}
	PORTER_STEMMER = nltk.stem.PorterStemmer()
	vocabulary = []

	tweets = []

	'''
	Read tweets from csv file
	'''
	with open('tweets/autora.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		tweets = [clean_tweet(str(row), PORTER_STEMMER) for row in spamreader]

	'''
	Create vocabulary based on tweets list
	'''
	for tweet in tweets:
		for word in tweet:
			if word not in vocabulary:
				vocabulary += [word]

	'''
	Filter vocabulary
	'''
	vocabulary = filter_vocabulary(vocabulary, ENGLISH_STOPWORDS, PORTER_STEMMER)

	'''
	Create a dict of word occurences for each tweet
		List of words depends on the vocabulary
	'''
	tweets_words_frequency = [{word: tweet.count(word) for word in vocabulary} for tweet in tweets]

if __name__ == '__main__':
    main()