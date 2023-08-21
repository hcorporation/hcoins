import praw
import db
from dotenv import load_dotenv
import os

backend = db.dbUtils()

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("ID"),
    client_secret=os.getenv("SECRET"),
    user_agent="hCoins-bot v0.1.0 (by /u/h_corp)",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)

new_mentions_unparsed = reddit.inbox.mentions
new_mentions = praw.models.util.stream_generator(new_mentions_unparsed, skip_existing=True)


def get_parent(mention):
    if "t1_" in mention.parent_id:
        return reddit.comment(id=mention.parent_id.replace("t1_", ""))
    elif "t3_" in mention.parent_id:
        return reddit.submission(id=mention.parent_id.replace("t3_", ""))
