import logging
from datetime import timedelta
from django.db import transaction
from django.utils import timezone

from users.models import UserProfile

logger = logging.getLogger(__name__)


class XPService:
    SOURCE_CHECK_IN = "check_in"
    SOURCE_PURCHASE = "purchase"
    SOURCE_REFERRAL = "referral"
    SOURCE_ADMIN = "admin_adjustment"

    @staticmethod
    def add_xp(user, amount, source=None, description=None):
        """Add XP to a user's profile."""
        if amount <= 0:
            logger.warning(
                f"Attempted to add non-positive XP ({amount}) to user {user.username}"
            )
            return user.profile.xp

        try:
            with transaction.atomic():
                profile = UserProfile.objects.select_for_update().get(user=user)

                old_xp = profile.xp
                profile.xp += amount
                profile.save()

                logger.info(
                    f"Added {amount} XP to user {user.username} (Source: {source}). Total: {profile.xp}"
                )

                return profile.xp

        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user {user.username}")
            raise
        except Exception as e:
            logger.error(f"Failed to add XP to user {user.username}: {str(e)}")
            raise

    @staticmethod
    def get_user_xp(user):
        """Get the current XP of a user."""
        return user.profile.xp


class StreakService:
    """
    Service layer for handling Streak logic.

    This service determines the validity of streaks and manages Streak Freezes.
    It encapsulates the complex logic of:
    1. Perfect streaks (consecutive days).
    2. Missed days with freezes available (streak recovery).
    3. Missed days without freezes (streak reset).
    """

    @staticmethod
    def determine_next_streak(user, last_checkin):
        """Calculates the new streak day for a user."""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        if not last_checkin:
            return 1, False

        # Consecutive check-in
        if last_checkin.check_in_date == yesterday:
            new_streak = last_checkin.streak_day + 1

            # Reset after day 7
            if new_streak > 7:
                return 1, False
            return new_streak, False

        # Check for Streak Freeze
        day_before_yesterday = today - timedelta(days=2)

        if last_checkin.check_in_date == day_before_yesterday:
            if user.profile.streak_freezes > 0:
                user.profile.streak_freezes -= 1
                user.profile.save()

                new_streak = last_checkin.streak_day + 1

                if new_streak > 7:
                    return 1, True

                return new_streak, True

        return 1, False
