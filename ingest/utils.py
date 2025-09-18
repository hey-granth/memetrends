from memes.models import Meme
from django.utils.dateparse import parse_datetime
from datetime import datetime, timezone
from django.utils import timezone as django_timezone


def save_posts(posts):
    for p in posts:
        Meme.objects.update_or_create(
            platform=p["platform"],
            external_id=p["external_id"],
            defaults={
                "text": p["text"],
                "media": p["media"],
                "posted_at": (
                    django_timezone.make_aware(parse_datetime(p["posted_at"]))
                    if isinstance(p["posted_at"], str)
                    else datetime.fromtimestamp(p["posted_at"], tz=timezone.utc)
                ),
                "likes": p["likes"],
                "comments": p["comments"],
                "shares": p["shares"],
            },
        )
