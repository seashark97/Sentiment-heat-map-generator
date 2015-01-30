from TwitterAPI import *
import json

api = TwitterAPI('TgryGZYtIelDGOZjzvruZgfcu',
	'DB8FAS39zhpaiDbDmPXVPrWzEMQHv68P2uneWXchZ9t75jLt9e',
	'177326568-vSEMKL9LJZ8SN9ds1Xh9pIvImLSIeoQD9fChTJfs',
	'zIUzddDMyQzk8iATpQdmDok47ApVJjCgjwOzGebJG0bOr')

r = TwitterRestPager(api, 'search/tweets', {'q': '#JeSuisCharlie', 'lang': 'en', 'count': 100})
count = 0
with open('charlie_tweets.txt', 'w') as outfile:
		for tweet in r.get_iterator():
			if tweet['coordinates'] and tweet['coordinates'] != [0.0, 0.0]:
				json.dump(dict([
					('id', tweet['id_str']),
					('tweet_text', tweet['text']),
					('coordinates', tweet['coordinates']['coordinates'])
				]),
				outfile)
				count +=1
				print count