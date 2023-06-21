import os
import json
from datetime import datetime

import tweepy
import pandas as pd
import PySimpleGUI as sg

from modules.twitter import TwitterUser

# Constants
TWITTER_SETTINGS_PATH = "settings/twitter_credentials.json"
OUTPUT_DIRECTORY = "output"

# Load twitter settings
with open(TWITTER_SETTINGS_PATH) as f:
    twitter_settings = json.load(f)


def create_api(ts) -> tweepy.API:
    """Create a tweepy API instance."""
    auth = tweepy.OAuthHandler(ts["api_key"], ts["api_key_secret"])
    auth.set_access_token(ts["access_token"], ts["token_secret"])
    return tweepy.API(auth, wait_on_rate_limit=True)


def fetch_followers(api: tweepy.API, screen_name: str, count: int = 256):
    """Fetch the followers of the specified user."""
    user = api.get_user(screen_name=screen_name)
    return api.get_follower_ids(user_id=user.id, count=count)


def create_spam_list(api, followers):
    """Create a list of spam account information."""
    spam_list = []
    for follower in followers:
        user = api.get_user(user_id=follower)
        twitter_user = TwitterUser(user)
        if twitter_user.is_spam():
            spam_list.append(twitter_user.to_dict())
    return spam_list


def save_spam_list(spam_list, output_path):
    """Save the spam account list to a file."""
    df = pd.DataFrame(spam_list)
    now = datetime.now()
    output_path = f"{output_path}/{now:%Y%m%d_%H%M%S}.tsv"
    df.to_csv(output_path, sep="\t", index=False)


def main():
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    api = create_api(twitter_settings)
    sc_list = sg.popup_get_text()
    for screen_name in sc_list:
        followers = fetch_followers(api, screen_name)
        spam_list = create_spam_list(api, followers)
        save_spam_list(spam_list, OUTPUT_DIRECTORY)
    print("Done")


if __name__ == "__main__":
    main()
