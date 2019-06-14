import tweepy
from data import *
import datetime
import pandas as pd


# timestamp
today = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")


# give auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


'''
# collect my tweets
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
'''

# tweets some text. 
#api.update_status("Okay I guess it is working. Let me make it unique. @pradeep_io, the date time is : " +today + "\n\n #gitcommitshow")


# searches hashtags
search_tags = '#GitCommitShow OR #gitcommitshow OR gitcommitshow OR gitcommit.show -from:gitcommitshow'

all_tweets = tweepy.Cursor(api.search,
                q=search_tags,
                lang="en").items()

#my_name = ["gitcommitshow"]
#others = [tweet for tweet in all_tweets if tweet.user.screen_name not in my_name]

for tweet in all_tweets:
    try:
        print("Operating on " +tweet.user.screen_name)
        api.retweet(tweet.id)
        api.create_favorite(tweet.id)
        api.create_friendship(tweet.user.id)
    except tweepy.error.TweepError:
        print("oh no. i need to skip it. \nskipping the tweet: " +str(tweet.id) +" by: " +str(tweet.user.screen_name) +'\n')
        pass


'''
users = [[tweet.user.id, tweet.user.screen_name, tweet.text] for tweet in tweets]

tweet_table = pd.DataFrame(data=users,
                    columns=['user_id', "user_name", "tweets"])


print(tweet_table)
'''
