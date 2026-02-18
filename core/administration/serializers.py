from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AdminAuditLog

class AdminStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_sessions = serializers.IntegerField()
    oauth_logins = serializers.IntegerField()
    total_gems = serializers.IntegerField()

class AdminAuditLogSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = AdminAuditLog
        fields = [
            "admin",
            "action",
            "target",
            "details",
            "timestamp",
            "request_id",
            "actor_ip",
        ]

    def get_admin(self, obj):
        return obj.admin_username or (obj.admin.username if obj.admin else "System")

    def get_target(self, obj):
        return obj.target_username or (obj.target_user.username if obj.target_user else "System")

class ChallengeAnalyticsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    completions = serializers.IntegerField()
    completion_rate = serializers.FloatField()
    avg_stars = serializers.FloatField()
    is_personalized = serializers.BooleanField()

class StoreItemSalesSerializer(serializers.Serializer):
    name = serializers.CharField()
    category = serializers.CharField()
    cost = serializers.IntegerField()
    sales = serializers.IntegerField()
    revenue = serializers.IntegerField()

class StoreAnalyticsSerializer(serializers.Serializer):
    items = StoreItemSalesSerializer(many=True)
    total_xp_spent = serializers.IntegerField()

class SystemIntegritySerializer(serializers.Serializer):
    users = serializers.IntegerField()
    challenges = serializers.IntegerField()
    store_items = serializers.IntegerField()
    notifications = serializers.IntegerField()
    audit_logs = serializers.IntegerField()

