import csv
import nltk
import re


RE_NUMBERS = re.compile(r'[0-9]+')
RE_NOT_LETTERS = re.compile(r'[^a-zA-Z]+')
RE_SPACES = re.compile(r'[^\S\f\t\n\r]+')

STOPWORDS = {word for word in nltk.corpus.stopwords.words('english')}
STEMMER = nltk.stem.PorterStemmer()


def clean_text(text):
    """
    Transform all numbers in the ' NUM ' text, removes non letters characters, stopwords, apply
    stemming in all restant words.
    """
    text = RE_NUMBERS.sub(' NUM ', text)
    text = RE_NOT_LETTERS.sub(' ', text)
    text = RE_SPACES.sub(' ', text)
    words = text.lower().strip().split(' ')
    words = [STEMMER.stem(word) for word in words if word not in STOPWORDS]
    return words


def build_vocabulary(words_list):
    """
    Builds the indexed vocabulary of the received words list.
    """
    words_set = {word for words in words_list for word in words}
    words_index = {word: index for index, word in enumerate(words_set)}
    return words_index


def build_instance(words, vocabulary):
    """
    Creates the instance of the received words based in the vocabulary.
    """
    instance = [0] * len(vocabulary)
    for word in words:
        if word in vocabulary:
            instance[vocabulary[word]] = 1
    return instance


def test():
    '''
    Tests the current file elements.
    '''
    print(f'testing {__file__}')
    tweets = [
        "Program Manager / Senior Project Manager - iTech Solutions - Greenwood Village, CO http:// jobcircle.com/z11237008 #jobcircle #jobs",
        "I'm at Gibby's (Aurora, CO ) http:// 4sq.com/LyUT4E",
        "I'm at Georgetown Lunatic Asylum (Georgetown, CO ) http:// 4sq.com/Q8kJye",
        "I'm at Whole Foods Market (Lakewood, CO ) w/ 3 others http:// 4sq.com/P1CR7W",
        "I'm at Olde Town Arvada (Arvada, CO ) http:// 4sq.com/SIpxsO",
        "Fourmile Fire survivors to share experience, advice with Larimer County - http:// bit.ly/Pjrs7f #FortCollins #Colorado",
        "I'm at Total Escape Games (Broomfield, CO ) http:// 4sq.com/M9HvkD",
        "I'm at MAD Greens - Inspired Eats (Downtown/16th Street Mall) (Denver, CO ) http:// 4sq.com/Mtd5KJ",
        "I'm at Independent Records & Video (Denver, CO ) http:// 4sq.com/NAfnZm",
        "Adults set to step out in 'Dance Found' at Ballet Nouveau Colorado in Broomfield - http:// bit.ly/MJ7WwD #Broomfield #Colorado",
        "I'm at Yard House (Lone Tree, Co ) http:// 4sq.com/Lt41mS"]

    clean_tweets = [clean_text(tweet) for tweet in tweets]
    vocabulary = build_vocabulary(clean_tweets)
    instances = [build_instance(clean_tweet, vocabulary) for clean_tweet in clean_tweets]

    print(f'vocabulary size: {len(vocabulary)}')
    print()

    print('tweet - clean - instance | comparison')
    for i in range(len(tweets)):
        print(tweets[i])
        print(clean_tweets[i])
        print(''.join(str(exists) for exists in instances[i]))
        print()


if __name__ == '__main__':
    test()
