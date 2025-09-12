from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Meme
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import MemeSerializer
from .permissions import IsOwnerOrReadOnly


class MemeViewSet(viewsets.ModelViewSet):
    queryset = Meme.objects.all().order_by("-posted_at")
    serializer_class = MemeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "platform",
        "posted_at",
    ]  # enables ?platform=reddit, ?posted_at__gte=2025-01-01
    ordering_fields = ["posted_at", "created_at"]  # enables ?ordering=posted_at
    ordering = ["-posted_at"]  # default ordering

    # create meme with owner as the logged-in user
    # requires authentication to create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
