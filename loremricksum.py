#!/usr/bin/env python
import os, json, io, tweepy, time, urllib2

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def runBot():
    quote = urllib2.urlopen('http://loremricksum.com/api/?paragraphs=1&quotes=1')
    text = json.load(quote)['data']
    tweet = json.dumps(text).strip("[]")
    api.update_status(tweet)

while True:
    try:    
        runBot()
    except tweepy.TweepError as e:
        print(e.reason)
    time.sleep(3600)

