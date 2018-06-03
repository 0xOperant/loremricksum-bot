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

    def on_data(self, status):
        status = str(status)
        try:
            json_acceptable_string = status.replace('\\','')
            #string to dict
            status=json.loads(json_acceptable_string)
            if 'direct_message' in status.keys():
                print ('\n')
                print (status[u'direct_message'][u'sender_screen_name'] +' sent: '+ status[u'direct_message'][u'text'])
                message=str(status[u'direct_message'][u'text'])
                api.send_direct_message(screen_name=str(status[u'direct_message'][u'sender_screen_name']),text='Out of office now - will respond to you asap')
                print ('auto response submitted')
            else:
                #not direct message flow
                pass
        except:
            #not important flows - couldn't convert to json/not correct flow in stream
            pass
        return True


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
stream.filter(track=['@loremricksumDev'], async=True)

#while True:
#    try:
#        tweetQuote()
#    except tweepy.TweepError as e:
#        print((e.reason))
#        tweetQuote()
#    time.sleep(3600)
