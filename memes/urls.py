from django.urls import path, include
from .views import MemeViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"memes", MemeViewSet, basename="memes")
urlpatterns = [
    path("", include(router.urls)),
]
