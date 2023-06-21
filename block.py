import glob
import json

import tweepy
import pandas as pd


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


def combine_tsv(tsv_files):
    df = pd.DataFrame()
    for tsv_path in tsv_files:
        cdf = pd.read_csv(tsv_path, sep="\t")
        df = pd.concat([df, cdf])
    return df.drop_duplicates()


def block_user(api: tweepy.API, screen_name):
    """Block a specified user."""
    try:
        api.create_block(screen_name=screen_name)
        print(f"Blocked {screen_name}")
    except tweepy.errors.NotFound:
        pass
    

def main():
    tsv_files = glob.glob("./output/*.tsv")
    df = combine_tsv(tsv_files)
    df.to_csv("block_list.tsv", sep="\t", index=False)
    api = create_api(twitter_settings)
    for screen_name in df.screen_name.tolist():
        block_user(api, screen_name)
    print(f"ブロックしたアカウントの数：{len(df)}")


if __name__ == "__main__":
    main()
