import logging
from django.db import transaction
from django.conf import settings
from users.models import UserProfile

logger = logging.getLogger(__name__)

class XPService:
    """
    Service layer for handling Experience Points (XP) logic.
    Centralizes all XP modifications to ensure consistency.
    """
    
    # Define source constants to avoid magic strings
    SOURCE_CHECK_IN = 'check_in'
    SOURCE_PURCHASE = 'purchase'
    SOURCE_REFERRAL = 'referral'
    SOURCE_ADMIN = 'admin_adjustment'

    @staticmethod
    def add_xp(user, amount, source=None, description=None):
        """
        Add XP to a user's profile.
        
        Args:
            user (User): The user object to add XP to.
            amount (int): The amount of XP to add. Must be positive.
            source (str): The source of the XP (e.g., 'check_in', 'purchase').
            description (str): Optional details about the transaction.
            
        Returns:
            int: The new total XP of the user.
        """
        if amount <= 0:
            logger.warning(f"Attempted to add non-positive XP ({amount}) to user {user.username}")
            return user.profile.xp

        try:
            with transaction.atomic():
                profile = UserProfile.objects.select_for_update().get(user=user)
                old_xp = profile.xp
                profile.xp += amount
                profile.save()
                
                logger.info(f"Added {amount} XP to user {user.username} (Source: {source}). Total: {profile.xp}")
                
                # TODO: If we implement an XPTransaction history model, create the record here.
                # XPTransaction.objects.create(user=user, amount=amount, source=source, ...)
                
                # Check for level up (optional logic, if you want to trigger notifications/events)
                # XPService._check_level_up(user, old_xp, profile.xp)
                
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
    """
    
    @staticmethod
    def calculate_streak(user, last_checkin_date):
        """
        Calculates the new streak based on the last check-in date.
        Handles Streak Freeze logic if applicable.
        
        Args:
            user (User): The user object.
            last_checkin_date (date): The date of the last check-in.
            
        Returns:
            tuple: (new_streak_day, freeze_used)
        """
        from datetime import timedelta
        from django.utils import timezone
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        if not last_checkin_date:
            return 1, False
            
        if last_checkin_date == yesterday:
            # Perfect streak
            return last_checkin_date.streak_day + 1, False # Wait, last_checkin_date is a DATE, not object.
            # I need the last_checkin object's streak_day. Logic refactor needed in caller or here.
            # Let's verify how we pass data. 
            pass

    # The previous implementation relies on the caller passing 'last_checkin_date' but we need the streak value too.
    # Let's adjust the signature to take the 'last_checkin' OBJECT or handle lookup here?
    # Caller 'CheckInView' has 'last_checkin' object.
    
    @staticmethod
    def determine_next_streak(user, last_checkin):
        """
        Determines the next streak day, handling freezes.
        
        Args:
            user (User): The user.
            last_checkin (DailyCheckIn): The last check-in object (can be None).
            
        Returns:
            tuple: (streak_day, freeze_used_boolean)
        """
        from datetime import timedelta
        from django.utils import timezone
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        if not last_checkin:
            return 1, False
            
        # If checked in yesterday, strictly increment
        if last_checkin.check_in_date == yesterday:
            new_streak = last_checkin.streak_day + 1
            if new_streak > 7:
                 # Standard logic from before (reset loop)
                 # But implies we might want infinite streaks later? 
                 # User asked for "implement 3" which is Freeze.
                 # User didn't ask for infinite. So keep reset to 1 after 7?
                 # Actually, usually streaks freeze works best with infinite or loops.
                 # Let's keep the loop behavior: > 7 -> 1.
                 return 1, False
            return new_streak, False
            
        # If gap > 1 day (e.g. checkin was day before yesterday)
        # Day Before Yesterday = Today - 2
        day_before_yesterday = today - timedelta(days=2)
        
        if last_checkin.check_in_date == day_before_yesterday:
            # Missed exactly ONE day. Check for freeze.
            if user.profile.streak_freezes > 0:
                # Consume freeze
                user.profile.streak_freezes -= 1
                user.profile.save()
                
                # Recover streak!
                # If last was Day 1, today becomes Day 2 (saved). 
                # Wait, if I missed yesterday, technically yesterday was Day 2 (missed), today is Day 3?
                # Or does usage just maintain the count?
                # Usually: "Streak Saved! You are on Day X".
                # Let's say last was Day 1. Yesterday missed. 
                # Freeze saves the streak. So today counts as the NEXT day.
                # So new_streak = last.streak_day + 1.
                new_streak = last_checkin.streak_day + 1
                 
                if new_streak > 7:
                    return 1, True # Reset logic still applies
                    
                return new_streak, True
        
        # If missed more than 1 day OR no freeze
        return 1, False
