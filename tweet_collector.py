import csv
import datetime
import json
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar

from dateutil.relativedelta import relativedelta
from pyquery import PyQuery


class Tweet:
    """
    Holds tweet information.
    """
    pass


class QueryArgs:
    """
    Twitter advanced search arguments.
    """

    def __init__(self, results=1, query=None, username=None, location=None, location_radius=None, since=None,
                 until=None, lang=None, top_tweets=None):
        self.results = results
        self.query = query
        self.username = username
        self.location = location
        self.location_radius = location_radius
        self.since = since
        self.until = until
        self.lang = lang
        self.top_tweets = top_tweets


class TweetAdvancedQuery:
    """
    Runs the search using http and json to recover the tweet information.
    """

    @staticmethod
    def query(args, proxy=None, verbose=False):
        """
        Runs the query with the received args and returns the collected tweets.
        """
        if verbose:
            print('Start collect')

        refresh_cursor = ''
        results = []
        cookie_jar = http.cookiejar.CookieJar()
        active = True

        while active:
            json = TweetAdvancedQuery._get_json_reponse(args, refresh_cursor, cookie_jar, proxy)
            if len(json['items_html'].strip()) == 0:
                break

            refresh_cursor = json['min_position']            
            tweets = PyQuery(json['items_html'])('div.js-stream-tweet')
            if len(tweets) == 0:
                break

            for tweet_html in tweets:
                tweet_pq = PyQuery(tweet_html)
                tweet = Tweet()
                tweet_username = tweet_pq('span.username.js-action-profile-name b').text()
                tweet_text = re.sub(r'\s+', ' ', tweet_pq('p.js-tweet-text').text().replace('# ', '#').replace('@ ', '@'))
                retweets = int(tweet_pq('span.ProfileTweet-action--retweet span.ProfileTweet-actionCount').attr('data-tweet-stat-count').replace(',', ''))
                favorites = int(tweet_pq('span.ProfileTweet-action--favorite span.ProfileTweet-actionCount').attr('data-tweet-stat-count').replace(',', ''))
                date_info = int(tweet_pq('small.time span.js-short-timestamp').attr('data-time'))
                tweet_id = tweet_pq.attr('data-tweet-tweet_id')
                permalink = tweet_pq.attr('data-permalink-path')
                tweet_user_id = int(tweet_pq('a.js-user-profile-link').attr('data-user-id'))
                geo_span = tweet_pq('span.Tweet-geo')
                geo = geo_span.attr('title') if len(geo_span) > 0 else ''
                urls = []
                for link in tweet_pq('a'):
                    try:
                        urls.append((link.attrib['data-expanded-url']))
                    except KeyError:
                        pass
                tweet.tweet_id = tweet_id
                tweet.permalink = f'https://twitter.com{permalink}'
                tweet.username = tweet_username
                tweet.text = tweet_text
                tweet.date = datetime.datetime.fromtimestamp(date_info)
                tweet.formatted_date = datetime.datetime.fromtimestamp(date_info).strftime('%a %b %d %X +0000 %Y')
                tweet.retweets = retweets
                tweet.favorites = favorites
                tweet.mentions = ' '.join(re.compile(r'(@\\w*)').findall(tweet.text))
                tweet.hashtags = ' '.join(re.compile(r'(#\\w*)').findall(tweet.text))
                tweet.geo = geo
                tweet.urls = ','.join(urls)
                tweet.user_id = tweet_user_id
                results.append(tweet)

                if args.results > 0 and len(results) >= args.results:
                    active = False
                    break

            if verbose:
                print(f'collected {len(results)} tweets')

        return results

    @staticmethod
    def _get_json_reponse(args, refresh_cursor, cookie_jar, proxy):
        """
        Collects the twitter query response.
        """
        url_get_data = ''
        if args.username is not None:
            url_get_data += f' from:{args.username}'
        if args.since is not None:
            url_get_data += f' since:{args.since}'
        if args.until is not None:
            url_get_data += f' until:{args.until}'
        if args.location is not None:
            url_get_data += f' near:{args.location}'
            if args.location_radius is not None:
                url_get_data += f' within:{args.location_radius}mi'
        if args.query is not None:
            url_get_data += f' {args.query}'
        url_lang = f'lang={args.lang}&' if args.lang  is not None else ''

        url = 'https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s'
        url = url % (urllib.parse.quote(url_get_data), url_lang, refresh_cursor)

        headers = [
            ('Host', 'twitter.com'),
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'),
            ('Accept', 'application/json, text/javascript, */*; q=0.01'),
            ('Accept-Language', 'de,en-US;q=0.7,en;q=0.3'),
            ('X-Requested-With', 'XMLHttpRequest'),
            ('Referer', url),
            ('Connection', 'keep-alive')
        ]

        if proxy:
            opener = urllib.request.build_opener(
                urllib.request.ProxyHandler({'http': proxy, 'https': proxy}),
                urllib.request.HTTPCookieProcessor(cookie_jar))
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            jsonResponse = response.read()
        except:
            raise ConnectionError(f'Twitter weird response. Try to see on browser: https://twitter.com/search?q={urllib.parse.quote(url_get_data)}&src=typd')

        dataJson = json.loads(jsonResponse.decode())
        return dataJson


def collect_event_tweets(since, until, results_per_day=1000, location=None, location_radius=None,
                         on_some_collected=None, verbose=False):
    """
    Helps the tweet collect by getting they per day in a received time interval.
    """
    if verbose:
        print('collecting tweets of event per day')

    tweets = []
    current_date = datetime.date(*(int(i) for i in since.split('-')))
    until_date = datetime.date(*(int(i) for i in until.split('-')))

    while current_date != until_date:
        next_date = current_date + relativedelta(days=1)
        if verbose:
            print(f'current day: {str(current_date)}')

        args = QueryArgs(
            results=results_per_day,
            location=location,
            location_radius=location_radius,
            since=str(current_date),
            until=str(next_date))

        try:
            current_day_tweets = TweetAdvancedQuery().query(args, verbose=verbose)
        except ConnectionError as e:
            print(e)
            print(f'error while collecting tweets of day {current_date}')
            continue

        tweets.extend(current_day_tweets)
        if on_some_collected is not None:
            on_some_collected(current_day_tweets)

        current_date = next_date

    return tweets


def test():
    """
    Tests the current file elements.
    """
    print(f'testing {__file__}')
    print('Testing TweetAdvancedQuery class')
    args = QueryArgs(query='christmas', results=50, since='2016-12-01', until='2017-01-01')
    tweets = TweetAdvancedQuery().query(args, verbose=True)
    print('finished')

    print('Testing collect_event_tweets method')
    tweets = collect_event_tweets(results_per_day=30, since='2017-07-18', until='2017-07-23', location='Denver, CO',
                                  location_radius=200, verbose=True)
    print('tweets texts:')
    for tweet in tweets:
        print(tweet.text)
    print('finished')


if __name__ == '__main__':
    test()
