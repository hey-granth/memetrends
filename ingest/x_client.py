import requests
from config import Config

BEARER_TOKEN = Config.X_BEARER_TOKEN
BASE_URL = "https://api.twitter.com/2/tweets/search/recent"


def fetch_memes(query="#meme", max_results=20):
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "created_at,public_metrics",
    }
    resp = requests.get(BASE_URL, headers=headers, params=params)
    data = resp.json().get("data", [])
    posts = []
    for t in data:
        metrics = t.get("public_metrics", {})
        posts.append(
            {
                "platform": "twitter",
                "external_id": t["id"],
                "text": t["text"],
                "media": None,  # needs extra API call if you want images
                "posted_at": t["created_at"],
                "likes": metrics.get("like_count", 0),
                "comments": metrics.get("reply_count", 0),
                "shares": metrics.get("retweet_count", 0),
            }
        )
    return posts
