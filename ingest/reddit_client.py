import praw
from config import Config


reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    user_agent=Config.REDDIT_USER_AGENT,
)


def fetch_memes(subreddit_name="memes", limit=20):
    subreddit = reddit.subreddit(subreddit_name)
    memes = []
    for submission in subreddit.hot(limit=limit):
        if not submission.stickied and (
            submission.url.endswith(".jpg")
            or submission.url.endswith(".png")
            or submission.url.endswith(".gif")
            or submission.url.endswith(".jpeg")
            or submission.url.endswith(".gifv")
        ):
            memes.append(
                {
                    "platform": "reddit",
                    "external_id": submission.id,
                    "text": submission.title,
                    "media": getattr(submission, "url", None),
                    "posted_at": submission.created_utc,
                    "likes": submission.score,
                    "comments": submission.num_comments,
                    "shares": 0,  # Reddit has no share metric
                }
            )
    return memes
