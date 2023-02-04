import pickle
import re
from time import sleep
from typing import Optional, Match

import praw

from scripts import config


class Brobot:
    def __init__(self):
        self.subreddits = ['tifu', 'amitheasshole']
        self.bot_name = '/brobot'
        self.reddit = praw.Reddit(client_id=config.CLIENT_ID,
                                  client_secret=config.CLIENT_SECRET,
                                  username=config.USERNAME,
                                  password=config.PASSWORD,
                                  user_agent=config.USER_AGENT)
        self.replied_to = self.get_replied_to()

    def get_replied_to(self) -> set:
        try:
            with open("data/replied_to.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return set()

    def save_replied_to(self):
        with open("data/replied_to.pkl", "wb") as f:
            pickle.dump(self.replied_to, f)

    def create_text(self, initial_text: str) -> str:
        text = initial_text.replace("pro", "bro")
        text += "\n\n###### Beep Boop I'm a brogram created by a brofessional brogrammer."
        return text

    def is_bot_called(self, comment: str) -> Optional[Match[str]]:
        return re.search(self.bot_name, comment, re.IGNORECASE)

    def brotify(self, subreddit_name: str):
        for comment in self.reddit.subreddit(subreddit_name).comments(limit=25):
            if self.is_bot_called(comment.body) and comment.id not in self.replied_to:
                comment.reply(self.create_text(comment.submission.selftext))
                self.replied_to.add(comment.id)

    def run(self):
        while True:
            sleep(1)
            for subreddit_name in self.subreddits:
                self.brotify(subreddit_name)
            self.save_replied_to()
