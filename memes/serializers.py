from rest_framework import serializers
from memes.models import Meme


class MemeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Meme
        fields = [
            "platform",
            "id",
            "text",
            "media",
            "posted_at",
            "updated_at",
            "trending_score",
            "likes",
            "owner",
            "comments",
            "shares",
        ]
