import requests
from config import Config
import logging


logger = logging.getLogger(__name__)
BEARER_TOKEN = Config.X_BEARER_TOKEN
BASE_URL = Config.X_BASE_URL


def fetch_memes(query="#meme", max_results=20):
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "created_at,public_metrics",
    }
    try:
        logger.info(
            f"Fetching X posts for query '{query}' with max_results={max_results}"
        )
        resp = requests.get(BASE_URL, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("data", [])
    except requests.RequestException as e:
        logger.error(f"Failed to fetch X posts: {e}")
        return []
    except ValueError:
        logger.error("Invalid JSON received from X API")
        return []

    posts = []
    for t in data:
        metrics = t.get("public_metrics", {})
        posts.append(
            {
                "platform": "twitter",
                "external_id": t["id"],
                "text": t.get("text", ""),
                "media": None,  # needs extra API call if you want images
                "posted_at": t.get("created_at"),
                "likes": metrics.get("like_count", 0),
                "comments": metrics.get("reply_count", 0),
                "shares": metrics.get("retweet_count", 0),
            }
        )
    logger.info(f"Fetched {len(posts)} X posts")
    return posts
