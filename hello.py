import tweepy
from data import *
import datetime


today = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)


# Post a tweet from Python
api.update_status("Okay I guess it is working. Let me make it unique. @pradeep_io, the date time is : " +today + "\n\n #gitshowcommit")
