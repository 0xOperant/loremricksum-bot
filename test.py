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

def getQuote():
    quote = urllib.request.urlopen(url).read().decode('UTF-8')
    text = json.loads(quote)['data']
    tweet = json.dumps(text).strip("[]")
    return tweet

def tweetQuote():
    msg = getQuote()
    api.update_status(msg)

def tweetReply(username, status_id):
    reply = getQuote()
    reply_status = "@%s %s" % (username, reply)
    api.update_status(status = reply_status, in_reply_to_status_id = status_id)

def favorite(status_id):
    api.create_favorite(status_id)

class BotStreamer(tweepy.StreamListener):

    def on_data(self, data):
        status = str(data)
        dmsg = json.loads(status)
        print(dmsg)
        if 'direct_message' in dmsg:
        print (dmsg['direct_message']['text'])


#    def on_status(self, status):
#        try:
#            username = status.user.screen_name
#            status_id = status.id
#            favorite(status_id)
#            tweetReply(username, status_id)
#        except tweepy.TweepError as e:
#            print((e.reason))
#            tweetReply(username, status_id)

myStreamListener = BotStreamer()

stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@loremricksumDev'], async=False)

#while True:
#    try:
#        tweetQuote()
#    except tweepy.TweepError as e:
#        print((e.reason))
#        tweetQuote()
#    time.sleep(3600)
