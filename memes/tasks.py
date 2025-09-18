from celery import shared_task
from .models import Meme
from math import log10, sqrt
from django.utils import timezone
from .services import update_leaderboard
import logging


logger = logging.getLogger(__name__)


# @shared_task is a celery decorator used with django which allows this function to be run asynchronously as a background task
@shared_task
def update_meme_leaderboard(meme_id):
    memes = Meme.objects.all()
    logger.info(f'Updating leaderboard for {len(memes)} memes')
    for i in memes:
        engagement: int = max(
            ((i.likes * 1) + (i.comments * 2) + (i.shares * 3)), 1
        )  # weighted engagement calc
        log_engagement: float = log10(
            engagement
        )  # used log10 so that massively popular memes don't dominate the trending list forever

        # age in hours
        age: float = max(
            (timezone.now() - i.posted_at).total_seconds() / 3600, 1
        )  # to prevent zero or negative values
        # did this to give preference to newer memes

        trending_score: float = (
            log_engagement / sqrt(age)
        )  # the decay of popularity of trending memes will be a lil slower to maintain stability and consistency by using sqrt

        # now updating db
        i.trending_score = trending_score
        i.save(update_fields=["trending_score"])
        logger.info(f'Meme leaderboard updated for {i.id}')

        # pushing to redis leaderboard
        update_leaderboard(i.id, i.trending_score)
