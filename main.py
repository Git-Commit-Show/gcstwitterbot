from config import *
import os.path
import json
from time import gmtime, strftime, sleep
from datetime import datetime
from send_mail import *


# custom logger
bot_username = 'gitcommitshow'
logfile_name = bot_username + ".log"
errorfile_name = "errors.log"

now = datetime.now()
timestr = now.strftime("%Y-%m-%d %H:%M:%S")


def log(message):
    """Log message to logfile."""
    file_exists = os.path.isfile(logfile_name)
    if file_exists:
        with open(logfile_name, 'a+') as f:
            t = strftime("%d %b %Y %H:%M:%S", gmtime())
            f.write("\n" + t + " " + message)
    else:
        with open(logfile_name, 'a+') as f:
            t = strftime("%d %b %Y %H:%M:%S", gmtime())
            f.write("\n" + t + " " + message)


def ErrorLog(message):
    file_exists = os.path.isfile(logfile_name)
    if file_exists:
        with open(errorfile_name, 'a+') as f:
            t = strftime("%d %b %Y %H:%M:%S", gmtime())
            f.write("\n" + t + " " + message)
    else:
        with open(errorfile_name, 'a+') as f:
            t = strftime("%d %b %Y %H:%M:%S", gmtime())
            f.write("\n" + t + " " + message)


"""
# Log message to logfile.
path = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(path, errorfile_name), 'a+') as f:
    t = strftime("%d %b %Y %H:%M:%S", gmtime())
    f.write("\n" + t + " " + message)
"""


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        name = tweet.user.name
        uname = tweet.user.screen_name
        tweet_id = tweet.id
        text = tweet.text
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            return

        print(name + ' said ' + text + "\n")

        if not tweet.favorited:
            try:
                tweet.user.follow()
                tweet.favorite()
            except tweepy.error.TweepError as e:
                sub = "[FAVORITE ERROR] {0}".format(name)
                tweet_url = "https://twitter.com/{0}/status/{1}".format(
                    uname, tweet_id)
                mess = tweet_url + "\n"
                mess += str(e)
                body = "{0} \n\nOccured at {1}".format(mess, timestr)
                mail(sub, body)
                ErrorLog("[FAVORITE ERROR] " + str(e))

        if not tweet.retweeted:
            try:
                tweet.retweet()
            except tweepy.error.TweepError as e:
                sub = "[RETWEET ERROR] {0}".format(name)
                tweet_url = "https://twitter.com/{0}/status/{1}".format(
                    uname, tweet_id)
                mess = tweet_url + "\n"
                mess += str(e)
                body = "{0} \n\nOccured at {1}".format(mess, timestr)
                mail(sub, body)
                ErrorLog("[RETWEET ERROR] " + str(e))

        log(name + ' said ' + text + "\n")

    def on_timeout(self):
        sub = "[TwCrawler] TIMEOUT Error"
        body = "Occured at {0}".format(timestr)
        mail(sub, body)
        return True

    def on_error(self, status_code):
        if status_code == 104:
            code = int(status_code)
            sub = "[TwCrawler] TIMEOUT Error {0}".format(code)
            body = "Occured at {0}".format(timestr)
            mail(sub, body)
        else:
            code = int(status_code)
            sub = "[TwCrawler] Error {0}".format(code)
            body = "Occured at {0}".format(timestr)
            mail(sub, body)
        return True

    # def on_error(self, status):
    #    print("Error detected")


# lists the first 20 tweets in my timeline
def timeline():
    timeline = api.home_timeline()
    for tweet in timeline:
        name = tweet.user.name
        text = tweet.text

        log(name + ' said ' + text + "\n")


errorMsg = "Check logs"


def main(keywords):

    global errorMsg
    # initialize api
    api = create_api()
    # timeline()
    tweets_listener = MyStreamListener(api)
    while True:
        try:
            # stream = tweepy.Stream(api.auth, tweets_listener, verify = False, timeout=600)
            stream = tweepy.Stream(api.auth, tweets_listener, timeout=600)
            # added async=True - opens a new thread and stops the stream from dying
            stream.filter(track=keywords, is_async=False)
        except Exception as e:
            e = str(e)
            errorMsg = 'I just caught the exception {0}'.format(e)
            print(errorMsg)
            sub = "[TwCrawler] GitCommitShow Error"
            body = "Error {0} \n\nOccurred at {1}".format(errorMsg, timestr)
            mail(sub, body)
            sleep(15*60)
            continue


if __name__ == "__main__":
    main(["#gitcommitshow", "#GitCommitShow", "gitcommitshow", "gitcommit.show"])
