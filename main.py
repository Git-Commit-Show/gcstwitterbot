import os
import json
import tweepy
from creds import *
from time import gmtime, strftime


# logger

bot_username = 'gitcommitshow'
logfile_name = bot_username + ".log"

# Auth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

"""
try:
    api.create_friendship("vimoveremacs")

except tweepy.error.TweepError as e:
    log(e.message)

else:
    log("Tweeted: " + text)
"""

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        uname = tweet.user.name
        text = tweet.text
        log(uname + ' said ' + text + "\n")
        print(uname + ' said ' + text + "\n")
    def on_error(self, status):
        print("Error detected")


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def timeline():
    timeline = api.home_timeline()
    for tweet in timeline:
        uname = tweet.user.name
        text = tweet.text

        log(uname + ' said ' + text + "\n")

if __name__ == "__main__":
    #timeline()
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=["#gitcommitshow", "#GitCommitShow", "gitcommitshow", "gitcommit.show"])
