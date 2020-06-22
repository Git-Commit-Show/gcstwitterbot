from config import create_api
from main import ErrorLog, log
from time import gmtime, strftime, sleep
from datetime import datetime
import json
from send_mail import *
from settings import KEYWORDS, FOLLOW, MAIL


now = datetime.now()
timestr = now.strftime("%Y-%m-%d %H:%M:%S")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, KEYWORDS, since_id):
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
        if any(keyword in tweet.text.lower() for keyword in KEYWORDS.keys()):
            logger.info("Answering to " + tweet.user.name)

            if FOLLOW:
                if not tweet.user.following:
                    try:
                        tweet.user.follow()
                    except tweepy.error.TweepError as e:
                        ErrorLog("[AUTO ERROR] Already Followed. " + str(e))
                        if MAIL:
                            sub = "[ERROR] {0}".format(name)
                            tweet_url = "https://twitter.com/{0}/status/{1}".format(uname, tweet_id)
                            mess = tweet_url + "\n"
                            mess += str(e)
                            body = "{0} \n\nOccured at {1}".format(mess, timestr)
                            mail(sub, body)

            tweet_handle = "@" + tweet.user.screen_name
            tweet_text = tweet_handle + " " + KEYWORDS[keyword]
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

    return new_since_id


errorMsg = "Check logs"


def main():
    global errorMsg
    api = create_api()
    since_id = 1
    while True:
        try:
            since_id = check_mentions(api, KEYWORDS, since_id)
            logger.info("Waiting...")
            sleep(30)

        except tweepy.error.TweepError as e:
            if 'Failed to send request:' in e.reason:
                print("Time out error caught.")
                sleep(180)
                continue


        except Exception as e:
            e = str(e)
            errorMsg = 'I just caught the exception {0}'.format(e)
            print(errorMsg)
            if MAIL:
                sub = "[TwCrawler] GitCommitShow Error"
                body = "Error {0} \n\nOccurred at {1}".format(errorMsg, timestr)
                mail(sub, body)

if __name__ == "__main__":
    main()
