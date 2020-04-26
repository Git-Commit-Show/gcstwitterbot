from config import *
import json
from time import gmtime, strftime
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
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def ErrorLog(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, errorfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        uname = tweet.user.name
        text = tweet.text
        if tweet.in_reply_to_status_id is not None or \
                            tweet.user.id == self.me.id:
            return

        print(uname + ' said ' + text + "\n")

        if not tweet.favorited:
            try:
                tweet.user.follow()
                tweet.favorite()
            except tweepy.error.TweepError as e:
                sub = "[FAVORITE ERROR] {0} {1}".format(uid, uname)
                mess = str(e)
                body = "{0} \n\nOccured at {1}".format(mess, timestr)
                mail(sub, body)
                ErrorLog("[FAVORITE ERROR] " + e.message)

        if not tweet.retweeted:
            try:
                tweet.retweet()
            except tweepy.error.TweepError as e:
                sub = "[RETWEET ERROR] {0} {1}".format(uid, uname)
                mess = str(e)
                body = "{0} \n\nOccured at {1}".format(mess, timestr)
                mail(sub, body)
                ErrorLog("[RETWEET ERROR] " + e.message)


        log(uname + ' said ' + text + "\n")

    def on_timeout(self):
        mail("[TIMEOUT] GitCommitShow timeout","Timeout at %s" % (timestr))
        return True


    def on_error(self,status_code):
        if status_code ==104:
            mail("[TwCrawler]TIMEOUT Error","Error code: %i at %s" % (int(status_code),timestr))
        return True

    #def on_error(self, status):
    #    print("Error detected")


# lists the first 20 tweets in my timeline
def timeline():
    timeline = api.home_timeline()
    for tweet in timeline:
        uname = tweet.user.name
        text = tweet.text

        log(uname + ' said ' + text + "\n")


def main(keywords):

    # initialize api
    api = create_api()
    #timeline()
    tweets_listener = MyStreamListener(api)
    try:
        stream = tweepy.Stream(api.auth, tweets_listener, timeout=600)
        stream.filter(track= keywords)
    except IOError as e:
        mail("[TwCrawler] GitCommitShow error","Error code: %i at %s" % (int(status_code),timestr))
        print('I just caught the exception: %s' % (e))




if __name__ == "__main__":
    main(["#gitcommitshow", "#GitCommitShow", "gitcommitshow", "gitcommit.show"])
