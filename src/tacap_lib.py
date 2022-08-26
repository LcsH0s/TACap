from multiprocessing.sharedctypes import Value
import tweepy
import json
import os
import pickle

import pygraphviz as pgv


class TwitterUser():
    def __init__(self, name, screen_name, user_id) -> None:
        self.name = name
        self.screen_name = screen_name
        self.id = user_id
        self.friends_dict = {}
        self.followers_dict = {}


class TACapClient():

    def __init__(self, cfg_path: str = None, eco_mode: bool = False):
        self.eco_mode = eco_mode
        self.id_dict = {}

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

        self.__load_id_dict()
        self.__authenticate()

    def __authenticate(self):
        self.auth = tweepy.OAuth1UserHandler(
            self.config['api_key'], self.config['api_secret'], self.config['access_token'], self.config['access_secret']
        )
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def get_user(self, screen_name: str) -> TwitterUser:
        """
        Fetches the info about a specified Twitter user and stores it inside a TwitterUser object

        Args:
            screen_name (str): Name of the user

        Returns:
            TwitterUser: object containing the username, screen_name and id of the user
        """
        try:
            usr = self.api.get_user(screen_name=screen_name)
            return TwitterUser(usr.name, usr.screen_name, usr.id)
        except tweepy.errors.NotFound as nf:
            raise ValueError(
                f"user with screen_name '{screen_name}' not found") from nf

    def get_user_friends(self, screen_name: str) -> dict:
        friend_ids = list(self.api.get_friend_ids(
            screen_name=screen_name, count=5000))

        friends_dict = {}
        for uid in friend_ids:
            if uid in self.id_dict.keys():
                friends_dict[uid] = self.id_dict[uid]
            else:
                friends_dict[uid] = None

        friend_ids_to_lookup = [
            uid for uid in friend_ids if uid not in self.id_dict.keys()]

        friend_ids_to_lookup = [friend_ids_to_lookup[i:i+100]
                                for i in range(0, len(friend_ids_to_lookup), 100)]
        friends_obj = []

        for uid_chunk in friend_ids_to_lookup:
            friends_obj += self.api.lookup_users(user_id=uid_chunk)

        for friend in friends_obj:
            friends_dict[friend.id] = friend.screen_name

        return friends_dict

    def get_user_followers(self, screen_name: str) -> list:
        follower_ids = list(self.api.get_follower_ids(
            screen_name=screen_name, count=5000))

        followers_dict = {}
        for uid in follower_ids:
            if uid in self.id_dict.keys():
                followers_dict[uid] = self.id_dict[uid]
            else:
                followers_dict[uid] = None

        follower_ids_to_lookup = [
            uid for uid in follower_ids if uid not in self.id_dict.keys()]

        follower_ids_to_lookup = [follower_ids_to_lookup[i:i+100]
                                  for i in range(0, len(follower_ids_to_lookup), 100)]
        followers_obj = []

        for uid_chunk in follower_ids_to_lookup:
            followers_obj += self.api.lookup_users(user_id=uid_chunk)

        for follower in followers_obj:
            followers_dict[follower.id] = follower.screen_name

        return followers_dict

    def __compute_social_graph(self, screen_name: str) -> dict:
        self.social_graph_dict = {
            'inward': [], 'outward': [], 'both': []}

        self.current_user = self.get_user(screen_name)
        self.current_user.friends_dict = self.get_user_friends(
            self.current_user.name)
        self.current_user.followers_dict = self.get_user_followers(
            self.current_user.name)

        self.__compute_id_dict()

        for f in [x for x in self.current_user.friends_dict.keys() if x not in self.current_user.followers_dict.keys()]:
            self.social_graph_dict['outward'].append(
                (f, self.current_user.friends_dict[f]))

        for f in [x for x in self.current_user.followers_dict.keys() if x not in self.current_user.friends_dict.keys()]:
            self.social_graph_dict['inward'].append(
                (f, self.current_user.followers_dict[f]))

        for f in [x for x in self.current_user.followers_dict.keys() if x in self.current_user.friends_dict.keys()]:
            self.social_graph_dict['both'].append(
                (f, self.current_user.friends_dict[f]))

        return self.social_graph_dict

    def __compute_id_dict(self):
        self.id_dict[self.current_user.id] = self.current_user.screen_name
        for u in zip(self.current_user.friends_dict.keys(), self.current_user.friends_dict.values()):
            self.id_dict[u[0]] = u[1]

        for u in zip(self.current_user.followers_dict.keys(), self.current_user.followers_dict.values()):
            self.id_dict[u[0]] = u[1]

        if self.eco_mode:
            self.__save_id_dict()

    def draw_social_graph(self, screen_name: str = None, mode: str = 'id', filename: str = None, import_path: str = None, format: str = 'json') -> None:
        """_summary_

        Args:
            screen_name (str): @ name of the user whose social graph you want to draw
            mode (str, optional): whether the ids or usernames or both will be displayed on the final graph. Defaults to 'id'.
        """
        if import_path == None:
            if screen_name == None:
                raise ValueError('Screen name cannot be empty')

            self.__compute_social_graph(screen_name=screen_name)

        else:
            self.load_graph_dict(format=format, filepath=import_path)

        G = pgv.AGraph(strict=False, directed=True, splines="curved")

        if mode == 'username':
            for f in self.social_graph_dict['outward']:
                G.add_edge(self.current_user.name, f[1], color='green')
            for f in self.social_graph_dict['inward']:
                G.add_edge(f[1], self.current_user.name, color='red')
            for f in self.social_graph_dict['both']:
                G.add_edge(self.current_user.name, f[1], color='blue')
                G.add_edge(f[1], self.current_user.name, color='blue')

        elif mode == 'id':
            for f in self.social_graph_dict['outward']:
                G.add_edge(self.current_user.name, f[0], color='green')
            for f in self.social_graph_dict['inward']:
                G.add_edge(f[0], self.current_user.name, color='red')
            for f in self.social_graph_dict['both']:
                G.add_edge(self.current_user.name, f[0], color='blue')
                G.add_edge(f[0], self.current_user.name, color='blue')

        elif mode == 'both':
            for f in self.social_graph_dict['outward']:
                G.add_edge(f"{self.current_user.name} | {self.current_user.id}",
                           f"{f[0]} | {f[1]}", color='green')
            for f in self.social_graph_dict['inward']:
                G.add_edge(f"{f[0]} | {f[1]}",
                           f"{self.current_user.name} | {self.current_user.id}", color='red')
            for f in self.social_graph_dict['both']:
                G.add_edge(f"{self.current_user.name} | {self.current_user.id}",
                           f"{f[0]} | {f[1]}", color='blue')
                G.add_edge(f"{f[0]} | {f[1]}",
                           f"{self.current_user.name} | {self.current_user.id}", color='blue')

        else:
            raise (ValueError(
                "argument 'mode' must be set to either 'id' or 'username', the default being 'id'"))

        G.edge_attr["color"] = "black"
        G.node_attr["color"] = "blue"
        G.node_attr["shape"] = "box"

        if filename == None:
            G.draw("%s's social graph.pdf" %
                   self.current_user.name, prog="circo")
        else:
            G.draw(filename, prog="circo")

        return self.social_graph_dict

    def __save_id_dict(self):
        try:
            with open(self.config["id_dict_path"], 'rb') as f:
                b = pickle.load(f)
            if self.id_dict != b:
                with open(self.config["id_dict_path"], 'wb') as f:
                    pickle.dump(self.id_dict, f, pickle.HIGHEST_PROTOCOL)

        except EOFError:
            with open(self.config["id_dict_path"], 'wb') as f:
                pickle.dump(self.id_dict, f, pickle.HIGHEST_PROTOCOL)

    def __load_id_dict(self):
        self.config['id_dict_path'] = os.getcwd() + '/logs/id_dict.pickle'

        if (not os.path.exists(self.config['id_dict_path'])) and self.eco_mode:
            os.makedirs(os.getcwd() + '/logs/', exist_ok=True)
            open(self.config["id_dict_path"], 'wb')

        elif os.path.exists(self.config['id_dict_path']):
            with open(self.config["id_dict_path"], 'rb') as f:
                self.id_dict = pickle.load(f)

    def save_graph_dict(self, format: str = 'json', filename: str = None):
        os.makedirs(os.getcwd() + '/logs/', exist_ok=True)
        if filename == None:
            filename = f'{self.current_user.id}--{self.current_user.screen_name}.json'

        if format == 'pickle':
            with open(os.getcwd() + '/logs/' + filename, 'wb') as f:
                pickle.dump(self.social_graph_dict, f, pickle.HIGHEST_PROTOCOL)
        elif format == 'json':
            with open(os.getcwd() + '/logs/' + filename, 'w') as f:
                f.write(json.dumps(self.social_graph_dict))

    def load_graph_dict(self, format: str, filepath: str):
        os.makedirs(os.getcwd() + '/logs/', exist_ok=True)
        if format == 'pickle':
            with open(filepath, 'rb') as f:
                self.social_graph_dict = pickle.load(
                    f, pickle.HIGHEST_PROTOCOL)
        elif format == 'json':
            with open(filepath, 'r') as f:
                self.social_graph_dict = json.loads(f.read())
        else:
            raise ValueError('Format must either be json or pickle')

        self.current_user = self.get_user(filepath.split('/')
                                          [-1].replace(f'.{format}', '').split('--')[-1])


# TODO: Create same drawing social graph but from a hashtag

"""

    def get_from_hashtag(self, hashtag: str, tweet_cap: int = 2000, fav_threshold: int = 20):
        for tweet in tweepy.Cursor(self.api.search_tweets, q=f'#{hashtag}').items(tweet_cap):
            if tweet.favorite_count >= fav_threshold:
                print(
                    f'{tweet.user.name} tweeted at {tweet.created_at} and tweet was liked {tweet.favorite_count} times')
"""
