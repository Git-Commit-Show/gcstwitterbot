from config import *
import os.path
import json
from time import gmtime, strftime, sleep
from datetime import datetime
from send_mail import *
from settings import *


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
        '''
        Referenced in issue#974 and issue#617
        https://github.com/tweepy/tweepy/issues/617#issuecomment-142439777
        https://github.com/tweepy/tweepy/issues/974#issuecomment-493283899
        '''
        if hasattr(tweet, 'retweeted_status'):
            try:
                text = tweet.retweeted_status.extended_tweet["full_text"]
            except:
                text = tweet.retweeted_status.text
        else:
            try:
                text = tweet.extended_tweet["full_text"]
            except AttributeError:
                text = tweet.text

        #text = tweet.text
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            return

        print('-'*20)
        print("\n" + name + ' said ' + text + "\n")
        print('-'*20)

        if FAVORITE:
            if not tweet.favorited:
                try:
                    tweet.user.follow()
                    tweet.favorite()
                except tweepy.error.TweepError as e:
                    ErrorLog("[FAVORITE ERROR] " + str(e))
                    if MAIL:
                        sub = "[FAVORITE ERROR] {0}".format(name)
                        tweet_url = "https://twitter.com/{0}/status/{1}".format(
                            uname, tweet_id)
                        mess = tweet_url + "\n"
                        mess += str(e)
                        body = "{0} \n\nOccured at {1}".format(mess, timestr)
                        mail(sub, body)

        if FOLLOW: 
            if not tweet.user.following: 
                try:
                    tweet.user.follow()
                except tweepy.error.TweepError as e:
                    ErrorLog("[FOLLOW ERROR] " + str(e))
                    if MAIL:
                        sub = "[FOLLOW ERROR] {0}".format(name)
                        tweet_url = "https://twitter.com/{0}/status/{1}".format(
                            uname, tweet_id)
                        mess = tweet_url + "\n"
                        mess += str(e)
                        body = "{0} \n\nOccured at {1}".format(mess, timestr)
                        mail(sub, body)


        if RETWEET:
            if not tweet.retweeted:
                try:
                    tweet.retweet()
                except tweepy.error.TweepError as e:
                    ErrorLog("[RETWEET ERROR] " + str(e))
                    if MAIL:
                        sub = "[RETWEET ERROR] {0}".format(name)
                        tweet_url = "https://twitter.com/{0}/status/{1}".format(
                            uname, tweet_id)
                        mess = tweet_url + "\n"
                        mess += str(e)
                        body = "{0} \n\nOccured at {1}".format(mess, timestr)
                        mail(sub, body)

        log(name + ' said ' + text + "\n")

        # Twitter bot sleep time settings in seconds. Use large delays so that you account will not banned
        sleep(DELAY) # 300 seconds = 5 minutes

    def on_timeout(self):
        sub = "[TwCrawler] TIMEOUT Error"
        body = "Occured at {0}".format(timestr)
        mail(sub, body)
        return True

    def on_error(self, status_code):
        if MAIL:
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
            # verify = False disables the SSL Verification. Not at all suggested.
            # stream = tweepy.Stream(api.auth, tweets_listener, verify = False, timeout=600)
            stream = tweepy.Stream(api.auth, tweets_listener, timeout=600)
            # added async=True - opens a new thread and stops the stream from dying
            stream.filter(track=keywords, is_async=False)

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
    main(HASHTAG_LIST)
