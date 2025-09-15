from config import Config

LEADERBOARD_KEY = "trending_memes"


def update_leaderboard(meme_id, score):
    """Update the leaderboard with the given meme ID and score."""
    Config.redis_client.zadd(LEADERBOARD_KEY, {meme_id: score})
    # https://redis.io/docs/latest/commands/zadd/


def get_top_memes(limit=20):
    """Retrieve the top N memes from the leaderboard."""
    return Config.redis_client.zrange(
        LEADERBOARD_KEY, 0, limit - 1, desc=True, withscores=True
    )
    # https://redis.io/docs/latest/commands/zrevrange/
    # desc=True with ZRANGE replaces ZREVRANGE in the newer versions of Redis
