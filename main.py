from config import *
import json
from time import gmtime, strftime


# custom logger
bot_username = 'gitcommitshow'
logfile_name = bot_username + ".log"
errorfile_name = "errors.log"


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def ErrorLog(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, errorlogfile_name), 'a+') as f:
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
                ErrorLog("[FAVORITE ERROR] " + e.message)

        if not tweet.retweeted:
            try:
                tweet.retweet()
            except tweepy.error.TweepError as e:
                ErrorLog("[RETWEET ERROR] " + e.message)


        log(uname + ' said ' + text + "\n")
    '''
    def mentions(self, tweet):
        myMentions = api.mentions_timeline()
        for tweet in myMentions:
            try:
                tweet.favorite()
                tweet.user.follow()

            except tweepy.error.TweepError as e:
            ErrorLog(e.message)
    '''

    def on_error(self, status):
        print("Error detected")


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
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track= keywords)



if __name__ == "__main__":
    main(["#gitcommitshow", "#GitCommitShow", "gitcommitshow", "gitcommit.show"])
