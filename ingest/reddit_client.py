import praw
from config import Config
import logging


logger = logging.getLogger(__name__)

reddit = praw.Reddit(
    client_id=Config.REDDIT_CLIENT_ID,
    client_secret=Config.REDDIT_CLIENT_SECRET,
    user_agent=Config.REDDIT_USER_AGENT,
)


def fetch_memes(subreddit_name="memes", limit=20):
    try:
        logger.info(f"Fetching Reddit posts from r/{subreddit_name} with limit={limit}")
        subreddit = reddit.subreddit(subreddit_name)
        memes = []
        for submission in subreddit.hot(limit=limit):
            if not getattr(submission, "stickied", False) and (
                str(getattr(submission, "url", "")).endswith(".jpg")
                or str(getattr(submission, "url", "")).endswith(".png")
                or str(getattr(submission, "url", "")).endswith(".gif")
                or str(getattr(submission, "url", "")).endswith(".jpeg")
                or str(getattr(submission, "url", "")).endswith(".gifv")
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
        logger.info(f"Fetched {len(memes)} Reddit posts")
        return memes
    except Exception as e:
        logger.error(f"Failed to fetch Reddit posts: {e}")
        return []
