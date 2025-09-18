from celery import shared_task
from .utils import save_posts
import x_client, reddit_client


@shared_task
def fetch_reddit_memes():
    posts = reddit_client.fetch_memes("memes", limit=50)
    save_posts(posts)


@shared_task
def fetch_twitter_memes():
    posts = x_client.fetch_memes(query="#meme", max_results=20)
    save_posts(posts)
