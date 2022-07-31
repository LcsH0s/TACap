import json
import tweepy


class TwitterClient():
    def __init__(self, cfg_path='../cfg/config.json'):
        self.cfg_path = cfg_path
        with open(cfg_path) as f:
            self.config = json.loads(f.read())

    def authenticate(self):
        self.auth = tweepy.OAuth1UserHandler(
            self.config['api_key'], self.config['api_secret'], self.config['access_token'], self.config['access_secret']
        )
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def get_from_hashtag(self, hashtag: str, tweet_cap: int, fav_threshold: int):
        for _, tweet in zip(range(tweet_cap), tweepy.Cursor(self.api.search_tweets, q=f'#{hashtag}').items()):
            if tweet.favorite_count >= fav_threshold:
                print(
                    f'{tweet.user.name} tweeted at {tweet.created_at} and tweet was liked {tweet.favorite_count} times')
