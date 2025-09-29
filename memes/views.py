from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from config import Config
from .services import LEADERBOARD_KEY
from .models import Meme
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    AllowAny,
    IsAuthenticated,
)
from .serializers import MemeSerializer
from .permissions import IsOwnerOrReadOnly
import logging


logger = logging.getLogger(__name__)


class MemeViewSet(viewsets.ModelViewSet):
    queryset = Meme.objects.all().order_by("-posted_at")
    serializer_class = MemeSerializer

    def get_permissions(self) -> list:
        # list means GET /memes/, retrieve means GET /memes/{id}
        # create means POST /memes/, update means PUT /memes/{id}, partial_update means PATCH /memes/{id}, destroy means DELETE /memes/{id}
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields: list[str] = [
        "platform",
        "posted_at",
    ]  # enables ?platform=reddit, ?posted_at__gte=2025-01-01
    ordering_fields: list[str] = [
        "posted_at",
        "created_at",
    ]  # enables ?ordering=posted_at
    ordering: list[str] = ["-posted_at"]  # default ordering

    # create meme with owner as the logged-in user
    # requires authentication to create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        logger.info(f"Meme created by user {self.request.user.username}")


@api_view(["GET"])
def trending_memes(request):
    top_ids = Config.redis_client.zrange(
        LEADERBOARD_KEY, 0, 9
    )  # will display the top 10 trending memes
    memes = list(Meme.objects.filter(id__in=top_ids))
    # if i were to display this list only, the db would have jumbled the redis ordering. saari mehenat kharab ho jati
    meme_dict = {str(m.id): m for m in memes}
    ordered = [meme_dict[i] for i in top_ids if i in meme_dict]
    serializer = MemeSerializer(ordered, many=True)
    logger.info("Returning top trending memes")
    return Response(serializer.data)
