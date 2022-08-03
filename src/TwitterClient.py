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

    def get_from_hashtag(self, hashtag: str, tweet_cap: int = 2000, fav_threshold: int = 20):
        for tweet in tweepy.Cursor(self.api.search_tweets, q=f'#{hashtag}').items(tweet_cap):
            if tweet.favorite_count >= fav_threshold:
                print(
                    f'{tweet.user.name} tweeted at {tweet.created_at} and tweet was liked {tweet.favorite_count} times')

    def get_user_sg(self, username: str):
        user = self.api.get_user(screen_name=username)
        print(
            f'{user.screen_name} has {user.followers_count} followers and follows {user.friends_count} people.')
        print(f'Has {user.favourites_count} fav accounts')
        print(f'Has tweeted : {user.statuses_count} times')

        friends = []
        for page in tweepy.Cursor(self.api.get_friends, screen_name=username,
                                  count=200).pages(10):
            for user in page:
                name = f"{user.id} - {user.name} (@{user.screen_name})"
                # print(name)
                friends.append(name)

        followers = []
        for page in tweepy.Cursor(self.api.get_followers, screen_name=username,
                                  count=200).pages(10):
            for user in page:
                name = f"{user.id} - {user.name} (@{user.screen_name})"
                followers.append(name)
            print(len(page))

        print('\n\nFriends : \n')
        for f in friends:
            print(f)
        print('\n\nFollowers : \n')
        for f in followers:
            print(f)
