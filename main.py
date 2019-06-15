import tweepy
from data import *
import datetime
import logging
from time import sleep


# timestamp
today = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")

logging.basicConfig(filename='app.log', filemode='a+', format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')


# give auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# searches hashtags
search_tags = ('#GitCommitShow', '#gitcommitshow', 'gitcommitshow', 'gitcommitshow', 'gitcommit.show') 
# search = '#GitCommitShow OR #gitcommitshow OR gitcommitshow OR gitcommit.show'

all_tweets = tweepy.Cursor(api.search,
                q=search_tags,
                since='2019-05-01',
                lang="en").items(1000)


for tweet in all_tweets:
    try:
        print('Tweet by: @' + tweet.user.screen_name)
        
        #  Retweet the tweet
        tweet.retweet()
        print('Retweeted the tweet')
        sleep(5)

        # Favorite the tweet
        tweet.favorite()
        print('Favorited the tweet')

        # Follow the user who tweeted
        if not tweet.user.following:
            tweet.user.follow()
            print('Followed the user')

        
        api.retweet(tweet.id)
        api.create_favorite(tweet.id)
        api.create_friendship(tweet.user.id)


    except tweepy.TweepError as e:
        logging.warning(e.reason)
        print(e.reason)

    except StopIteration:
        break
