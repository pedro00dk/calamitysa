import urllib.request, urllib.error, urllib.parse, json, re, datetime, sys, http.cookiejar
from pyquery import PyQuery


class Tweet:
	pass


class QueryArgs:
	def __init__(self, results=1, query=None, username=None, location=None, location_radius=None, since=None, until=None, lang=None, top_tweets=None):
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

	@staticmethod
	def query(args, proxy=None, verbose=False):

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
				for link in tweet_pq("a"):
					try:
						urls.append((link.attrib['data-expanded-url']))
					except KeyError:
						pass

				tweet.tweet_id = tweet_id
				tweet.permalink = 'https://twitter.com' + permalink
				tweet.username = tweet_username
				
				tweet.text = tweet_text
				tweet.date = datetime.datetime.fromtimestamp(date_info)
				tweet.formatted_date = datetime.datetime.fromtimestamp(date_info).strftime("%a %b %d %X +0000 %Y")
				tweet.retweets = retweets
				tweet.favorites = favorites
				tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
				tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
				tweet.geo = geo
				tweet.urls = ",".join(urls)
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
		url = 'https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s'
		
		url_get_data = ''
		if args.username is not None:
			url_get_data += ' from:' + args.username
			
		if args.since is not None:
			url_get_data += ' since:' + args.since
			
		if args.until is not None:
			url_get_data += ' until:' + args.until
			
		if args.location is not None:
			url_get_data += ' near:' + args.location
			if args.location_radius is not None:
				url_get_data += ' within:' + str(args.location_radius) + 'mi'

		if args.query is not None:
			url_get_data += ' ' + args.query

		if args.lang  is not None:
			url_lang = 'lang=' + args.lang + '&'
		else:
			url_lang = ''
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
			opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}), urllib2.HTTPCookieProcessor(cookie_jar))
		else:
			opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
		opener.addheaders = headers

		try:
			response = opener.open(url)
			jsonResponse = response.read()
		except:
			print('Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd' % urllib.parse.quote(url_get_data))
			print('Unexpected error: ', sys.exc_info()[0])
			sys.exit()
			return

		dataJson = json.loads(jsonResponse.decode())

		return dataJson


def main():
    args = QueryArgs(results=10, since='2012-07-01', until='2012-07-02', location='Denver, CO', location_radius=200)
    tweets = TweetAdvancedQuery().query(args, verbose=True)
    print(len(tweets))


if __name__ == '__main__':
    main()
