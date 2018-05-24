#!/usr/bin/env python
import os, json, io, time, urllib.request, urllib.error, urllib.parse
import tweepy

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
url = 'http://loremricksum.com/api/?paragraphs=1&quotes=1'

def runBot():
    quote = urllib.request.urlopen(url).read().decode('UTF-8')
    text = json.loads(quote)['data']
    tweet = json.dumps(text).strip("[]")
    api.update_status(tweet)

while True:
    try:    
        runBot()
    except tweepy.TweepError as e:
        print((e.reason))
    time.sleep(3600)

