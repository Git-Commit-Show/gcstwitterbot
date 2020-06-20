# GitCommitShow Twitter Bot using Python


The official Twitter Bot for [Git Commit Show](https://www.gitcommit.show)


A Python built twitter retweet bot using Tweepy. Searches the database from a certain time period and also works on real time data to favorite, follow and retweet tweets based on hashtag/s. It also has functions to interact with the people if a certain keyword is used. It can be used for automation and marketing purposes.

## What You Need

-   [Tweepy](http://www.tweepy.org/)  - An easy-to-use Python library for accessing the Twitter API.

    `pip install tweepy`
> There is a `requirements.txt` file if you want to use a virtual environment.

-	Make a [Twitter Developer Account](https://developer.twitter.com/en).
-   Make sure you fully understand  [Twitter's Rules on Automation](https://support.twitter.com/articles/76915). Play nice. Don't spam!

## Instructions

-   Create a new directory to contain all of your retweet bot files.

	`mkdir twitter-bot`

-   Create a new  [Twitter Application](https://apps.twitter.com/app/new). This is where you'll generate your keys, tokens, and secrets.
-   Fill in your keys, tokens, and secrets in a .env file and add it in the .gitignore file so that others cannot watch it.
-   Change the settings in settings.py to tweak the bot to your liking.
	`LIKE = True`
	`FOLLOW = False`

-   The example demonstrates multiple hashtag value, but you can tweak the code to search hashtags as per your liking.

-   Run the main.py script.

	`python main.py`   
	`python autoreply.py`   


