import os
import json
import tweepy
from creds import *
from time import gmtime, strftime


# logger

bot_username = 'gitcommitshow'
logfile_name = bot_username + ".log"
errorfile_name = "errors.log"

# Auth
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def ErrorLog(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, errorlogfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        uname = tweet.user.name
        text = tweet.text
        try:
            tweet.favorite()
            tweet.user.follow()
        except tweepy.error.TweepError as e:
            ErrorLog(e.message)
        log(uname + ' said ' + text + "\n")
        print(uname + ' said ' + text + "\n")

    '''
    def mentions(self, tweet):
        myMentions = api.mentions_timeline()
        for tweet in myMentions:
            try:
                tweet.favorite()
                tweet.user.follow()

            except tweepy.error.TweepError as e:
            ErrorLog(e.message)
    '''

    def on_error(self, status):
        print("Error detected")


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
