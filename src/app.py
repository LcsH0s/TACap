import tweepy
import json

from TwitterClient import TwitterClient

# API keyws that yous saved earlier

tw = TwitterClient()
tw.authenticate()
tw.get_from_hashtag("olympicgames")