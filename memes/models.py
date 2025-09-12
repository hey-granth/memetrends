from django.db import models
from django.contrib.auth.models import User


class Meme(models.Model):
    PLATFORM_CHOICES = [
        ("reddit", "Reddit"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
    ]

    platform = models.CharField(
        max_length=100, null=True, blank=True, choices=PLATFORM_CHOICES
    )
    external_id = models.CharField(
        max_length=100, null=True, blank=True
    )  # memes.Meme: (models.E004) 'id' can only be used as a field name if the field also sets 'primary_key=True'.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memes")
    text = models.TextField(null=True, blank=True)
    media = models.JSONField(blank=False, null=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # when the meme entry was created in our DB
    updated_at = models.DateTimeField(
        auto_now=True
    )  # when the meme was actually uploaded on that platform
    posted_at = models.DateTimeField()
    engagement_score = models.IntegerField(null=True, blank=True)
