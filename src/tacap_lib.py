import tweepy
import json


class TwitterUser():
    def __init__(self, name, screen_name, user_id) -> None:
        self.name = name
        self.screen_name = screen_name
        self.id = user_id
        self.friends = []
        self.friend_ids = []
        self.followers = []


class TACapClient():

    def __init__(self, cfg_path: str = None):
        if cfg_path == None:
            print("No file path specified. Using default 'config.json'")
            self.cfg_path = 'config.json'

        try:
            with open(self.cfg_path) as f:
                self.config = json.loads(f.read())

        except FileNotFoundError:
            print("No 'config.json' file found. Creating configuration file :")
            self.config = {}
            self.config["api_key"] = input("api_key : ")
            self.config["api_secret"] = input("api_secret : ")
            self.config["access_token"] = input("access_token : ")
            self.config["access_secret"] = input("access_secret : ")

            with open(self.cfg_path, "w") as f:
                f.write(json.dumps(self.config))

        self.__authenticate()

    def __authenticate(self):
        self.auth = tweepy.OAuth1UserHandler(
            self.config['api_key'], self.config['api_secret'], self.config['access_token'], self.config['access_secret']
        )
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

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

    def get_user_followers(self, screen_name: str):
        followers = []
        for page in tweepy.Cursor(self.api.get_followers, screen_name=screen_name,
                                  count=200).pages(10):
            for user in page:
                followers.append(TwitterUser(
                    user.name, user.screen_name, user.id))

        return followers


"""
    def get_from_hashtag(self, hashtag: str, tweet_cap: int = 2000, fav_threshold: int = 20):
        for tweet in tweepy.Cursor(self.api.search_tweets, q=f'#{hashtag}').items(tweet_cap):
            if tweet.favorite_count >= fav_threshold:
                print(
                    f'{tweet.user.name} tweeted at {tweet.created_at} and tweet was liked {tweet.favorite_count} times')
"""
