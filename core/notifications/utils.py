import logging
from django.conf import settings
from .models import FCMToken

logger = logging.getLogger(__name__)

import firebase_admin
from firebase_admin import messaging, credentials

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred)
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin SDK: {e}")

def send_fcm_push(user, title, body, data=None):
    """
    Sends a push notification to all devices registered for a user.
    """
    tokens = list(FCMToken.objects.filter(user=user).values_list('token', flat=True))
    
    if not tokens:
        logger.info(f"No FCM tokens found for user {user.username}")
        return

    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            tokens=tokens,
        )
        response = messaging.send_each_for_multicast(message)
        logger.info(f"Successfully sent FCM push to {user.username}: {response.success_count} success, {response.failure_count} failure")
        
        # Optional: Clean up failed tokens
        if response.failure_count > 0:
            for idx, resp in enumerate(response.responses):
                if not resp.success:
                    # Token might be invalid or expired
                    failed_token = tokens[idx]
                    FCMToken.objects.filter(token=failed_token).delete()
                    logger.info(f"Deleted invalid FCM token for {user.username}")
                    
    except Exception as e:
        logger.error(f"Error sending FCM push to {user.username}: {e}")

