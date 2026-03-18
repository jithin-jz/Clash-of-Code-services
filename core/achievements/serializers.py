from rest_framework import serializers
from .models import Achievement, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    is_unlocked = serializers.SerializerMethodField()
    unlocked_at = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            "id", "slug", "title", "description", "icon",
            "category", "xp_reward", "is_secret", "is_unlocked", "unlocked_at",
        ]

    def get_is_unlocked(self, obj):
        user = self.context.get("request", {})
        if hasattr(user, "user"):
            user = user.user
        if not user or not hasattr(user, "id"):
            return False
        return UserAchievement.objects.filter(user=user, achievement=obj).exists()

    def get_unlocked_at(self, obj):
        user = self.context.get("request", {})
        if hasattr(user, "user"):
            user = user.user
        if not user or not hasattr(user, "id"):
            return None
        ua = UserAchievement.objects.filter(user=user, achievement=obj).first()
        return ua.unlocked_at.isoformat() if ua else None


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ["id", "achievement", "unlocked_at"]
