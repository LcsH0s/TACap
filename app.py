import tweepy
import json

# API keyws that yous saved earlier
with open('config.json') as f:
    config = json.loads(f.read())


auth = tweepy.OAuth1UserHandler(
    config['api_key'], config['api_secret'], config['access_token'], config['access_secret']
)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(f"{tweet.author.name} : {tweet.text}\n")
