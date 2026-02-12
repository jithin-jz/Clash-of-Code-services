from django.utils import timezone
from django.db.models import Max, Q
from .models import Challenge, UserProgress, Hint
from users.models import UserProfile
from xpoint.services import XPService


class ChallengeService:
    """
    Service layer for handling Challenge interactions.
    Encapsulates logic for progression, locking, hints, and submissions.
    """

    @staticmethod
    def get_annotated_challenges(user, queryset=None):
        """
        Returns a list of challenges annotated with status and stars for the given user.
        Handles the implicit locking logic (Next level unlocked only if previous is completed).
        """
        if queryset is None:
            queryset = Challenge.objects.all()

        challenges = queryset.order_by("order")

        # optimized: fetch all progress in one query
        progress_map = {
            p.challenge_id: p for p in UserProgress.objects.filter(user=user)
        }

        results = []
        previous_completed = True  # Level 1 is always unlocked

        for challenge in challenges:
            p = progress_map.get(challenge.id)

            status = UserProgress.Status.LOCKED
            stars = 0

            if p:
                status = p.status
                stars = p.stars

            # Implicit unlocking logic
            if status == UserProgress.Status.LOCKED and previous_completed:
                status = UserProgress.Status.UNLOCKED

            # Prepare data object (similar to what serializer expects)
            # We preserve the model instance but attach dynamic fields
            challenge.user_status = status
            challenge.user_stars = stars

            results.append(challenge)

            # Update flag for next iteration
            previous_completed = status == UserProgress.Status.COMPLETED

        return results

    @staticmethod
    def get_challenge_details(user, challenge):
        """
        Retrieves detailed challenge info including unlocked hints and current status.
        """
        progress, _ = UserProgress.objects.get_or_create(user=user, challenge=challenge)

        # Use annotated list logic to determine if effectively unlocked if record exists but is locked
        # For simplicity, we assume if they can access the detail page, they likely can see it,
        # but strictly we might want to check the previous level here.

        return {
            "status": progress.status,
            "stars": progress.stars,
            "unlocked_hints": progress.hints_unlocked.all(),
            "ai_hints_purchased": progress.ai_hints_purchased,
        }

    @staticmethod
    def process_submission(user, challenge, passed=False):
        """
        Handles success/failure of a code submission.
        """
        if not passed:
            return {"status": "failed"}

        progress, _ = UserProgress.objects.get_or_create(user=user, challenge=challenge)

        # Calculate Stars based on static hints used
        # 0-1 Hints: 3 Stars (First hint is free/safe)
        # 2 Hints: 2 Stars
        # 3+ Hints: 1 Star
        
        hints_used = progress.hints_unlocked.count()
        
        if hints_used >= 3:
            stars = 1
        elif hints_used == 2:
            stars = 2
        else:
            # 0 or 1 hint used
            stars = 3
            
        stars = max(1, stars)

        newly_completed = progress.status != UserProgress.Status.COMPLETED

        # Update Progress
        # If already completed, only update if we got more stars?
        # Typically we just keep the best result.
        if newly_completed or stars > progress.stars:
            progress.status = UserProgress.Status.COMPLETED
            progress.completed_at = timezone.now()
            progress.stars = max(progress.stars, stars)
            progress.save()

            # Award XP only on first completion
            if newly_completed:
                xp_earned = challenge.xp_reward
                XPService.add_xp(user, xp_earned, source="challenge_completion")

        next_slug = ChallengeService._get_next_level_slug(challenge, user)
        
        # Check for Certificate Trigger (Level 53 completed)
        certificate_data = {}
        if challenge.order == 53:
            try:
                from .certificate_generator import CertificateGenerator
                generator = CertificateGenerator()
                if generator.is_eligible(user):
                        cert = generator.generate_certificate(user)
                        certificate_data = {
                            "certificate_unlocked": True,
                            "certificate_id": str(cert.certificate_id),
                             # Ensure this relative path matches what frontend expects
                            "certificate_url": f"/api/certificates/download/" 
                        }
            except Exception as e:
                # Log error but don't fail the submission
                print(f"Error generating certificate: {e}")

        result_data = {
            "status": "completed" if newly_completed else "already_completed",
            "xp_earned": xp_earned if newly_completed else 0,
            "stars": stars,
            "next_level_slug": next_slug,
        }
        result_data.update(certificate_data)
        
        return result_data

    @staticmethod
    def unlock_hint(user, challenge, hint_order):
        """
        Unlocks a specific hint for a user, deducting XP.
        Raises Hint.DoesNotExist or PermissionError.
        """
        hint = Hint.objects.get(challenge=challenge, order=hint_order)

        progress, _ = UserProgress.objects.get_or_create(user=user, challenge=challenge)

        if progress.hints_unlocked.filter(id=hint.id).exists():
            return hint  # Already unlocked

        if user.profile.xp >= hint.cost:
            XPService.add_xp(user, -hint.cost, source="hint_unlock")
            progress.hints_unlocked.add(hint)
            return hint
        else:
            raise PermissionError("Insufficient XP")

    @staticmethod
    def purchase_ai_assist(user, challenge):
        """
        Purchases the next AI hint level, deducting progressive XP.
        1st hint: 10 XP
        2nd hint: 20 XP
        3rd hint: 30 XP
        """
        progress, _ = UserProgress.objects.get_or_create(
            user=user, challenge=challenge
        )
        
        if progress.ai_hints_purchased >= 3:
            raise PermissionError("Maximum of 3 AI hints allowed for this challenge.")
        
        current_count = progress.ai_hints_purchased
        cost = 10 * (current_count + 1)
        
        if user.profile.xp >= cost:
            XPService.add_xp(user, -cost, source="ai_assist")

            progress.ai_hints_purchased += 1
            progress.save()

            return user.profile.xp
        else:
            raise PermissionError("Insufficient XP")


    @staticmethod
    def _get_next_level_slug(current_challenge, user):
        """Get the next level slug (all challenges are global now)."""
        next_challenge = (
            Challenge.objects.filter(order__gt=current_challenge.order)
            .order_by("order")
            .first()
        )
        return next_challenge.slug if next_challenge else None
