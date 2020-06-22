import tweepy
from main import ErrorLog, log
import logging
from config import create_api
from time import gmtime, strftime, sleep
from datetime import datetime
import json
from send_mail import *
from settings import *
from ignore import *


now = datetime.now()
timestr = now.strftime("%Y-%m-%d %H:%M:%S")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, keywords, since_id):
    keyword = ""
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        name = tweet.user.name
        uname = tweet.user.screen_name
        tweet_id = tweet.id
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keys):
            if tweet_id in IGNORE.values():
                logger.warning("Skipping " + tweet.user.name)
            else:
                IGNORE.update(uname = tweet_id)
                logger.info("Replying to " + tweet.user.name)

                text = "@" + tweet.user.screen_name
                tweet_text = text + KEYWORDS[keyword]
                print(tweet_text)
            '''
            if not tweet.user.following:
                try:
                    tweet.user.follow()
                except tweepy.error.TweepError as e:
                    sub = "[ERROR] {0}".format(name)
                    tweet_url = "https://twitter.com/{0}/status/{1}".format(uname, tweet_id)
                    mess = tweet_url + "\n"
                    mess += str(e)
                    body = "{0} \n\nOccured at {1}".format(mess, timestr)
                    mail(sub, body)
                    ErrorLog("[AUTO ERROR]" + str(e))
            try:
                api.update_status(
                    status=tweet_text,
                    in_reply_to_status_id=tweet.id,
                )
            except tweepy.error.TweepError as e:
                sub = "[ERROR] {0}".format(name)
                tweet_url = "https://twitter.com/{0}/status/{1}".format(uname, tweet_id)
                mess = tweet_url + "\n"
                mess += str(e)
                body = "{0} \n\nOccured at {1}".format(mess, timestr)
                mail(sub, body)
                ErrorLog("[AUTO ERROR]" + str(e))
            '''
    return new_since_id


# We have to explicitly convert KEYWORDS.keys() into list. Default - dict_keys()
keys = list(KEYWORDS.keys())

def main():
    global keys
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, list(KEYWORDS.keys()), since_id)
        logger.info("Waiting...")
        sleep(60)

if __name__ == "__main__":
    main()
