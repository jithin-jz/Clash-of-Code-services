from rest_framework import viewsets, permissions, status, mixins, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiTypes, inline_serializer
from auth.throttles import NotificationRateThrottle
from .models import Notification, FCMToken
from .serializers import NotificationSerializer, FCMTokenSerializer


class FCMTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for managing FCM tokens for push notifications.
    """

    serializer_class = FCMTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FCMToken.objects.filter(user=self.request.user)

    @extend_schema(
        request=FCMTokenSerializer,
        responses={200: FCMTokenSerializer, 201: FCMTokenSerializer},
        description="Register or update an FCM token for the authenticated user.",
    )
    def create(self, request, *args, **kwargs):
        token = request.data.get("token")
        device_id = request.data.get("device_id")

        if not token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Use token as the primary lookup to avoid IntegrityError if device_id changes
            fcm_token, created = FCMToken.objects.update_or_create(
                token=token, defaults={"user": request.user, "device_id": device_id}
            )

            serializer = self.get_serializer(fcm_token)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NotificationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    ViewSet for managing user notifications.
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [NotificationRateThrottle]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by(
            "-created_at"
        )

    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT},
        description="Mark all notifications as read for the authenticated user.",
    )
    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({"status": "marked all read"}, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={204: None},
        description="Delete all notifications for the authenticated user.",
    )
    @action(detail=False, methods=["delete"])
    def clear_all(self, request):
        self.get_queryset().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT},
        description="Mark a specific notification as read.",
    )
    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "marked read"}, status=status.HTTP_200_OK)
