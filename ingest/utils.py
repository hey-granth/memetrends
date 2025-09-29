from memes.models import Meme
from django.utils.dateparse import parse_datetime
from datetime import datetime, timezone
from django.utils import timezone as django_timezone
import logging
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)


def save_posts(posts):
    logger.info(f"Saving {len(posts)} posts to database")
    saved = 0
    user, created = User.objects.get_or_create(username="default_user")
    for p in posts:
        try:
            Meme.objects.update_or_create(
                platform=p["platform"],
                external_id=p["external_id"],
                defaults={
                    "text": p.get("text", ""),
                    "media": p.get("media"),
                    "posted_at": (
                        django_timezone.make_aware(parse_datetime(p["posted_at"]))
                        if isinstance(p.get("posted_at"), str)
                        else datetime.fromtimestamp(
                            p.get("posted_at", 0), tz=timezone.utc
                        )
                    ),
                    "likes": p.get("likes", 0),
                    "comments": p.get("comments", 0),
                    "shares": p.get("shares", 0),
                    "owner": user,
                },
            )
            saved += 1
        except Exception as e:
            logger.error(f"Failed to save post {p.get('external_id')}: {e}")
    logger.info(f"Saved {saved}/{len(posts)} posts")
