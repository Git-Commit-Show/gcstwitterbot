import tweepy
from main import ErrorLog, log
import logging
from config import create_api
from time import gmtime, strftime, sleep
from datetime import datetime
import json
import time
from send_mail import *


now = datetime.now()
timestr = now.strftime("%Y-%m-%d %H:%M:%S")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def main():
    api = create_api()
    search='#gitcommitshow'
    numTweets=1
    user = 'vimoveremacs'
    start_date = datetime(2020, 4, 20, 00, 00, 00)
    end_date = datetime(2020, 4, 26, 00, 00, 00)
    date_since = "2020-06-19"


    tweets_collected = tweepy.Cursor(api.search, q=search, lang='en', tweet_mode='extended', date=date_since).items(numTweets)
    for tweet in tweets_collected:
        print("\n")
        print("Tweeted At: {}\nUser: {}\nTweet Content: {}".
                format(tweet.created_at, tweet.user.screen_name, tweet.full_text))
        print("\n")
    '''
        try:
            # Liking a tweet with a specific search keyword in it
            tweet.favorite()
            logger.info("Tweet liked.")
            # retweeting a tweet with a specific keyword in it
            tweet.retweet()
            logger.info("Tweet retweeted. Waiting for 90 secs...")
            time.sleep(90)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
    '''
if __name__ == "__main__":
    main()
