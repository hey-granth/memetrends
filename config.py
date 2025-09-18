from dotenv import load_dotenv
from os import getenv
import redis


load_dotenv()


class Config:
    DEBUG = getenv("DEBUG")
    SECRET_KEY = getenv("SECRET_KEY")
    redis_client = redis.StrictRedis(
        host="localhost", port=6379, db=0, decode_responses=True
    )
    CELERY_BROKER_URL = getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "UTC"

    REDDIT_CLIENT_ID = getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = getenv("REDDIT_USER_AGENT")

    X_API_KEY = getenv("X_API_KEY")
    X_API_SECRET = getenv("X_API_SECRET")
    X_BEARER_TOKEN = getenv("X_BEARER_TOKEN")

    ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost").split(",")
