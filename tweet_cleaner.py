import re
import csv
import nltk

def clean_tweet(tweet):
	return re.sub('[^a-zA-Z]+', ' ', tweet).lower()

def main():
	vocabulary = []
	tweets = []

	'''
	Read tweets from csv file
	also keep only low case letters on tweets
	'''
	with open('tweets/autora.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
		i = 0
		for row in spamreader:
			cleaned_tweet = clean_tweet(str(row))
			tweets += [cleaned_tweet[1:len(cleaned_tweet) - 1]]

	'''
	Create vocabulary based on tweets list
	'''
	for tweet in tweets:
		tweet_words = tweet.split(' ')
		for word in tweet_words:
			if word not in vocabulary:
				vocabulary += [word]

	'''
	Remove uninteresting words in vocabulary
	'''
	ENGLISH_STOPWORDS = {word for word in nltk.corpus.stopwords.words('english')}
	vocabulary = [word for word in vocabulary if word not in ENGLISH_STOPWORDS]

if __name__ == '__main__':
    main()