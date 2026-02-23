from celery import shared_task
from .emails import send_welcome_email, send_otp_email
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email_task(user_id):
    """
    Async task to send welcome email.
    We pass user_id because passing complex objects (User) to Celery is an anti-pattern.
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        send_welcome_email(user)
        logger.info(f"Welcome email task completed for user {user_id}")
        return {"status": "sent", "user_id": user_id}
    except User.DoesNotExist:
        logger.warning(f"User {user_id} not found for welcome email task")
        return {"status": "user_not_found", "user_id": user_id}
    except Exception as e:
        logger.exception(f"Welcome email task failed: {str(e)}")
        return {"status": "error", "error": str(e)}


@shared_task
def send_otp_email_task(email, otp):
    """
    Async task to send OTP email.
    """
    try:
        send_otp_email(email, otp)
        logger.info(f"OTP email task completed for {email}")
        return {"status": "sent", "email": email}
    except Exception as e:
        logger.exception(f"OTP email task failed: {str(e)}")
        return {"status": "error", "error": str(e)}
