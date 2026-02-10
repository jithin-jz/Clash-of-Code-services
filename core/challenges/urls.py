from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChallengeViewSet,
    LeaderboardView,
)
from .certificate_views import CertificateViewSet

router = DefaultRouter()
router.register(r"challenges", ChallengeViewSet)
router.register(r"certificates", CertificateViewSet, basename='certificate')


urlpatterns = [
    path("challenges/leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("", include(router.urls)),
]
