from itertools import count
import json
import tweepy


class TwitterUser():
    def __init__(self, name, screen_name, user_id) -> None:
        self.name = name
        self.screen_name = screen_name
        self.id = user_id
        self.friends = []
        self.friend_ids = []
        self.followers = []


class TwitterClient():
    def __init__(self, cfg_path: str):
        if cfg_path == None:
            print("No file path specified. Using default 'config.json'")
            self.cfg_path = 'config.json'

        try:
            with open(self.cfg_path) as f:
                self.config = json.loads(f.read())

        except FileNotFoundError:
            print("No 'config.json' file found. Creating configuration file :")
            self.config = {"api_key": r"88heXiv5cIn5qiZEGDg6bTWl5",
                           "api_secret": r"b90Gz9F0E6rDGwx5F3jJXGagKAWQxqwpsSyWloow6bPyVmJPnK",
                           "bearer_token": r"AAAAAAAAAAAAAAAAAAAAAFH4eQEAAAAAm0pQpGaDOiKw62csnhVGHGZVl%2FM%3DMpqlTAK3CjnbygCWaPUNBm1z2KlvB9rUQLr9wJsvsd8PosPtCx",
                           "access_token": r"1524312708815937537-mqcR0exoVqiWMZOIf69xs9wrK71DxW",
                           "access_secret": r"kqQ8vnHmlLlGQkRwojSwq9o2iJyP1nR0IXj84JSFOtvEx",
                           "client_id": r"WnhsUlVCZndiMW1ma3dGa0Jma046MTpjaQ",
                           "client_secret": r"G6G5_IFCXHQyc2kKCYncxs9vhC2AikqU85AF_uhwN8_qkEJlPe"}

            with open(cfg_path, "w") as f:
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

    def get_user(self, screen_name) -> TwitterUser:
        usr = self.api.get_user(screen_name=screen_name)
        return TwitterUser(usr.name, usr.screen_name, usr.id)

    def get_user_friends(self, screen_name: str):
        friend_ids = list(self.api.get_friend_ids(
            screen_name=screen_name, count=5000))

        friend_ids = [friend_ids[i:i+100]
                      for i in range(0, len(friend_ids), 100)]
        friends_obj = []
        friends = []

        for uid_chunk in friend_ids:
            friends_obj += self.api.lookup_users(user_id=uid_chunk)

        for friend in friends_obj:
            friends.append(friend.screen_name)

        return (friends, friend_ids[0])

    def get_user_sg(self, screen_name: str):
        friends, _ = self.get_user_friends(screen_name=screen_name)
        sg = []
        for friend in friends:
            sg.append(self.get_user_friends(friend)[0])

        return sg

    def get_user_followers(self, screen_name: str):
        followers = []
        for page in tweepy.Cursor(self.api.get_followers, screen_name=screen_name,
                                  count=200).pages(10):
            for user in page:
                followers.append(TwitterUser(
                    user.name, user.screen_name, user.id))

        return followers
