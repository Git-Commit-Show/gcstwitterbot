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
    search='gitcommitshow'
    numTweets=1000

    for tweet in tweepy.Cursor(api.search,search).items(numTweets):
        try:
            print('Tweet Liked')
            # Liking a tweet with a specific search keyword in it
            tweet.favorite()
            logger.info("Liked. Waiting...")
            # retweeting a tweet with a specific keyword in it
            tweet.retweet()
            logger.info("Retweeted. Waiting...")
            time.sleep(90)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

if __name__ == "__main__":
    main()
