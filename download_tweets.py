#Download tweets and save it to a JSON file.

import datetime
import tweepy
import pickle
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time
 
consumer_key = 'redacted'
consumer_secret = 'redacted'
access_token = 'redacted'
access_secret = 'redacted'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


track_words_hillary = ["hillaryclinton","sheswithus","hillaryforpresident","hillary4president","imwithher","hillary","clinton","neverhillary","clinton16"]
track_words_donald = ["realdonaldtrump","trumpforpresident","trump4president","trumptaxes","trump","donaldtrump","trump16","makeamericagreatagain","trumptales","tcot","trumppence16","nevertrump","trumpthechump","dumptrump","maga","votetrump"]

track_words = track_words_hillary + track_words_donald + ["debate","debates","debates2016"] 

class Tweets_track(StreamListener):
    def on_data(self, data):
        try:
            with open("tweets.json", "a") as f:
                f.write(data)
                #time.sleep(1) 
                return True

        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    def on_error(self, status):
        print(status)
        return False


print("Start : ",datetime.datetime.now().time().replace(microsecond=0))


twitter_stream = Stream(auth, Tweets_track())
twitter_stream.filter(track=track_words)
print("----------done--------")
