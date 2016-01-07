import tweepy, json, re, sys, collections, csv, os, nltk
import numpy as np
from senti_classifier import senti_classifier

#use the access token from the twitter
ckey = ''
csecret = ''
atoken = ''
asecret = ''

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

tweets = []

def warmUp():
	senti_classifier.polarity_scores(["Keeping you warm.","Please stay warm, please."])

def getScore(tweet):
	t = [tweet]
	pos_s, neg_s = senti_classifier.polarity_scores(t)
	if pos_s>neg_s:
		return "pos"
	elif pos_s==neg_s:
		return "nut"
	else:
		return "neg"

def preprocess(tweet):

	remove_hashtags = re.compile(r'#\w+\s?')
	remove_freinds = re.compile(r'@\w+\s?')
	remove_links = re.compile(r'http\w+\s?')
	remove_RT = re.compile(r'RT : ')

	tweet = remove_hashtags.sub('', tweet)
	tweet = remove_freinds.sub('',tweet)
	tweet = remove_links.sub('',tweet)
	# tweet = remove_RT.sub('',tweet)

	if 't.co' in tweet or 'RT : ' in tweet or tweet in tweets:
		return ''
	tweets.append(tweet)	
	return tweet

class MyStreamListener(tweepy.StreamListener):
	count = 1
	def on_status(self, status):
		global tweets
		tweet = preprocess((status.text).encode('ascii','ignore'))
		tweet = ' '.join(tweet.split())
		if len(tweet.split())>=5:
			tweets.append(tweet)
		MyStreamListener.count -= 1
		print tweet
		# exit()

	def on_error(self, status_code):
		print sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream

	def on_timeout(self):
		print sys.stderr, 'Timeout...'
		return True # Don't kill the stream

def getTweetsWithScore(topic, location, count):
	ret = []
	global tweets
	api = tweepy.API(auth)
	cursor = tweepy.Cursor(api.search,q=topic,lang='en').items(10)
# geocode=""+str(location['lng'])+","+str(location['lat'])+","+str(location['rad'])+""
	# twts = api.search(q=topic, count = 10, lang='en')
	for tweet in cursor:
		tweet = preprocess((tweet.text).encode('ascii','ignore'))
		tweet = ' '.join(tweet.split())
		if len(tweet.split())>=5:
			ret.append((tweet,getScore(tweet)))
	return ret