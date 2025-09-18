from django.db import models
from django.contrib.auth.models import User


class Meme(models.Model):
    PLATFORM_CHOICES: list[tuple[str, str]] = [
        ("reddit", "Reddit"),
        ("twitter", "Twitter"),
        ("instagram", "Instagram"),
    ]

    platform: str = models.CharField(
        max_length=100, null=True, blank=True, choices=PLATFORM_CHOICES
    )
    external_id: str = models.CharField(
        max_length=100, null=True, blank=True, unique=True
    )  # memes.Meme: (models.E004) 'id' can only be used as a field name if the field also sets 'primary_key=True'.
    owner: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="memes"
    )
    text: str = models.TextField(null=True, blank=True)
    media = models.JSONField(blank=False, null=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # when the meme entry was created in our DB
    updated_at = models.DateTimeField(
        auto_now=True
    )  # when the meme was actually uploaded on that platform
    posted_at = models.DateTimeField()

    # engagement fields for calculating trending score
    likes: int = models.PositiveIntegerField(
        default=0
    )  # used PositiveIntegerField rather than IntegerField coz engagement can't be negative
    shares: int = models.PositiveIntegerField(default=0)
    comments: int = models.PositiveIntegerField(default=0)

    trending_score: float = models.FloatField(default=0.0)


    class Meta:
        unique_together = (("platform", "external_id"),)
    indexes = [
            models.Index(fields=["platform", "posted_at"]),
            models.Index(fields=["-trending_score"]),
        ]


    def __str__(self):
        return f"{self.platform} meme {self.id}"
