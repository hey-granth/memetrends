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
            "created_at",
            "updated_at",
            "engagement_score",
            "owner",
        ]
