from django.urls import path, include
from .views import MemeViewSet, trending_memes
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"memes", MemeViewSet, basename="memes")
urlpatterns = [
    path("", include(router.urls)),
    path("trending/", trending_memes, name="trending_memes"),
]
