from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        import notifications.signals
        from .models import Notification
        from .utils import send_fcm_push
        from .dynamo import dynamo_notification_client
        dynamo_notification_client.create_table_if_not_exists()
