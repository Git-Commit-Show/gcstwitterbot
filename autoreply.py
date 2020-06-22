import tweepy
from main import ErrorLog, log
import logging
from config import create_api
from time import gmtime, strftime, sleep
from datetime import datetime
import json
from send_mail import *
from settings import *


now = datetime.now()
timestr = now.strftime("%Y-%m-%d %H:%M:%S")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
keyword = "no"

def check_mentions(api, keywords, since_id):
    global keyword
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
        for keyword in keywords:
            if keyword in tweet.text.lower():
                print("Found keyword: " + keyword)
                reply = KEYWORDS[keyword]
                print("Found Reply:    " + reply)
                logger.info("Answering to " + tweet.user.name)
                text = "@" + tweet.user.screen_name
                tweet_text = text + " " + reply
                try:
                    api.update_status(
                        status=tweet_text,
                        in_reply_to_status_id=tweet.id,
                    )
                except tweepy.error.TweepError as e:
                    ErrorLog("[AUTO ERROR]" + str(e))
                    if MAIL:
                        sub = "[ERROR] {0}".format(name)
                        tweet_url = "https://twitter.com/{0}/status/{1}".format(uname, tweet_id)
                        mess = tweet_url + "\n"
                        mess += str(e)
                        body = "{0} \n\nOccured at {1}".format(mess, timestr)
                        mail(sub, body)

                if FOLLOW:
                    if not tweet.user.following:
                        try:
                            tweet.user.follow()
                        except tweepy.error.TweepError as e:
                            ErrorLog("[AUTO ERROR]" + str(e))
                            if MAIL:
                                sub = "[ERROR] {0}".format(name)
                                tweet_url = "https://twitter.com/{0}/status/{1}".format(uname, tweet_id)
                                mess = tweet_url + "\n"
                                mess += str(e)
                                body = "{0} \n\nOccured at {1}".format(mess, timestr)
                                mail(sub, body)

    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["#remind", "#feedback"], since_id)
        logger.info("Waiting...")
        sleep(60)

if __name__ == "__main__":
    main()
