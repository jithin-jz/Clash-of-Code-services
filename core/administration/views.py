import uuid

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiTypes, inline_serializer
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.db.models import Sum, Avg, Count

from users.models import UserProfile
from users.serializers import UserSerializer
from .models import AdminAuditLog
from .permissions import IsAdminUser, can_manage_user
from .serializers import (
    AdminStatsSerializer,
    AdminAuditLogSerializer,
    ChallengeAnalyticsSerializer,
    StoreAnalyticsSerializer,
    SystemIntegritySerializer,
)
from challenges.models import Challenge, UserProgress
from store.models import StoreItem, Purchase
from notifications.models import Notification
from auth.throttles import SensitiveOperationThrottle


def _request_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _request_id(request):
    return request.headers.get("X-Request-ID") or str(uuid.uuid4())


def _parse_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "on"}
    return False


def log_admin_action(admin, action, request=None, target_user=None, details=None):
    """Helper to record administrative actions in the audit log."""
    AdminAuditLog.objects.create(
        admin=admin,
        admin_username=admin.username if admin else "system",
        action=action,
        target_user=target_user,
        target_username=target_user.username if target_user else "",
        target_email=target_user.email if target_user else "",
        details=details or {},
        actor_ip=_request_ip(request) if request else None,
        user_agent=(request.headers.get("User-Agent", "")[:512] if request else ""),
        request_id=_request_id(request) if request else "",
    )


class AdminStatsView(APIView):
    """View to get admin dashboard statistics."""

    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={
            200: AdminStatsSerializer,
            403: OpenApiTypes.OBJECT,
        },
        description="Get administration statistics.",
    )
    def get(self, request):
        total_users = User.objects.count()

        # Active sessions in last 24 hours
        yesterday = timezone.now() - timedelta(days=1)
        active_sessions = User.objects.filter(last_login__gte=yesterday).count()

        # OAuth logins (Providers other than email/local)
        oauth_logins = UserProfile.objects.exclude(
            provider__in=["email", "local"]
        ).count()

        # Total Gems (XP)
        total_xp = UserProfile.objects.aggregate(total_xp=Sum("xp"))["total_xp"] or 0

        data = {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "oauth_logins": oauth_logins,
            "total_gems": total_xp,
        }
        serializer = AdminStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(APIView):
    """View to list all users for admin."""

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    @extend_schema(
        responses={
            200: UserSerializer(many=True),
            403: OpenApiTypes.OBJECT,
        },
        description="List all users (Admin only).",
    )
    def get(self, request):
        users = (
            User.objects.select_related("profile")
            .annotate(
                followers_total=Count("followers", distinct=True),
                following_total=Count("following", distinct=True),
            )
            .order_by("-date_joined")
        )
        if not request.user.is_superuser:
            users = users.filter(is_staff=False, is_superuser=False)
        return Response(
            UserSerializer(users, many=True, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )


class UserBlockToggleView(APIView):
    """View to toggle user active status."""

    permission_classes = [IsAdminUser]
    throttle_classes = [SensitiveOperationThrottle]

    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT},
        description="Toggle user active status (block/unblock).",
    )
    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        allowed, message = can_manage_user(request.user, user)
        if not allowed:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        reason = (request.data.get("reason") or "").strip()

        # Toggle status directly on user model
        new_is_active = not user.is_active

        # Do not allow disabling the final active superuser account.
        if user.is_superuser and not new_is_active:
            active_superusers = User.objects.filter(is_superuser=True, is_active=True).count()
            if active_superusers <= 1:
                return Response(
                    {"error": "Cannot block the last active superuser account."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        previous_is_active = user.is_active
        user.is_active = new_is_active
        user.save(update_fields=["is_active"])

        log_admin_action(
            admin=request.user,
            action="TOGGLE_USER_BLOCK",
            target_user=user,
            request=request,
            details={
                "before": {"is_active": previous_is_active},
                "after": {"is_active": user.is_active},
                "reason": reason,
            },
        )

        return Response(
            {
                "message": f"User {'unblocked' if user.is_active else 'blocked'} successfully",
                "is_active": user.is_active,
            },
            status=status.HTTP_200_OK,
        )


class UserDeleteView(APIView):
    """View to delete a user account."""

    permission_classes = [IsAdminUser]
    throttle_classes = [SensitiveOperationThrottle]

    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT},
        description="Delete a user account (Admin only).",
    )
    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        allowed, message = can_manage_user(request.user, user)
        if not allowed:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)

        if user.is_superuser:
            superuser_count = User.objects.filter(is_superuser=True).count()
            if superuser_count <= 1:
                return Response(
                    {"error": "Cannot delete the last superuser account."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        reason = (request.query_params.get("reason") or "").strip()
        target_username = user.username
        target_email = user.email

        log_admin_action(
            admin=request.user,
            action="DELETE_USER",
            target_user=user,
            request=request,
            details={"username": username, "email": target_email, "reason": reason},
        )

        user.delete()

        return Response(
            {"message": f"User {username} deleted successfully"},
            status=status.HTTP_200_OK,
        )


class ChallengeAnalyticsView(APIView):
    """View to get detailed challenge performance analytics."""
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={200: ChallengeAnalyticsSerializer(many=True)},
        description="Get detailed challenge performance analytics.",
    )
    def get(self, request):
        challenges = Challenge.objects.all()
        progress_summary = (
            UserProgress.objects.values("challenge_id")
            .annotate(
                total_attempts=Count("id"),
                completions=Count(
                    "id",
                    filter=models.Q(status=UserProgress.Status.COMPLETED),
                ),
                avg_stars=Avg(
                    "stars",
                    filter=models.Q(status=UserProgress.Status.COMPLETED),
                ),
            )
        )
        summary_map = {row["challenge_id"]: row for row in progress_summary}
        analytics_data = []

        for challenge in challenges:
            summary = summary_map.get(challenge.id, {})
            total_attempts = summary.get("total_attempts", 0)
            completions = summary.get("completions", 0)
            avg_stars = summary.get("avg_stars") or 0

            analytics_data.append({
                "id": challenge.id,
                "title": challenge.title,
                "completions": completions,
                "completion_rate": (completions / total_attempts * 100) if total_attempts > 0 else 0,
                "avg_stars": avg_stars,
                "is_personalized": challenge.created_for_user is not None
            })

        serializer = ChallengeAnalyticsSerializer(analytics_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreAnalyticsView(APIView):
    """View to get store economy and item popularity."""
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={200: StoreAnalyticsSerializer},
        description="Get store economy and item popularity analytics.",
    )
    def get(self, request):
        items = StoreItem.objects.annotate(
            purchase_count=Count("purchases")
        ).order_by("-purchase_count")

        item_stats = [{
            "name": item.name,
            "category": item.category,
            "cost": item.cost,
            "sales": item.purchase_count,
            "revenue": item.purchase_count * item.cost
        } for item in items]

        total_revenue = sum(item["revenue"] for item in item_stats)

        data = {
            "items": item_stats,
            "total_xp_spent": total_revenue
        }
        serializer = StoreAnalyticsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GlobalNotificationView(APIView):
    """View to send notifications to all users."""
    permission_classes = [IsAdminUser]
    throttle_classes = [SensitiveOperationThrottle]

    def post(self, request):
        verb = request.data.get("message")
        if not verb:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate message length
        if len(verb) > 500:
            return Response({"error": "Message too long (max 500 characters)"}, status=status.HTTP_400_BAD_REQUEST)
        include_staff = _parse_bool(request.data.get("include_staff", False))
        users_qs = User.objects.filter(is_active=True).exclude(id=request.user.id)
        if not include_staff:
            users_qs = users_qs.filter(is_staff=False, is_superuser=False)

        recipient_ids = list(users_qs.values_list("id", flat=True))
        notifications = [
            Notification(recipient_id=user_id, actor=request.user, verb=verb)
            for user_id in recipient_ids
        ]
        Notification.objects.bulk_create(notifications, batch_size=1000)

        reason = (request.data.get("reason") or "").strip()

        log_admin_action(
            admin=request.user,
            action="SEND_GLOBAL_NOTIFICATION",
            request=request,
            details={
                "message": verb,
                "recipient_count": len(recipient_ids),
                "include_staff": include_staff,
                "reason": reason,
            },
        )

        return Response({"message": f"Broadcast sent to {len(recipient_ids)} users"}, status=status.HTTP_200_OK)


class AdminAuditLogView(APIView):
    """View to retrieve administrative action logs."""
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={200: AdminAuditLogSerializer(many=True)},
        description="Retrieve administrative action logs.",
    )
    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 100))
        except (TypeError, ValueError):
            limit = 100
        try:
            offset = int(request.query_params.get("offset", 0))
        except (TypeError, ValueError):
            offset = 0

        limit = max(1, min(limit, 500))
        offset = max(0, offset)

        logs = AdminAuditLog.objects.select_related("admin", "target_user").all()

        action = request.query_params.get("action")
        admin_username = request.query_params.get("admin")
        target_username = request.query_params.get("target")
        if action:
            logs = logs.filter(action=action)
        if admin_username:
            logs = logs.filter(admin_username=admin_username)
        if target_username:
            logs = logs.filter(target_username=target_username)

        logs = logs[offset:offset + limit]
        serializer = AdminAuditLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SystemIntegrityView(APIView):
    """View to check core system health and counts."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {
            "users": User.objects.count(),
            "challenges": Challenge.objects.count(),
            "store_items": StoreItem.objects.count(),
            "notifications": Notification.objects.count(),
            "audit_logs": AdminAuditLog.objects.count()
        }
        serializer = SystemIntegritySerializer(data)
        return Response(serializer.data)


