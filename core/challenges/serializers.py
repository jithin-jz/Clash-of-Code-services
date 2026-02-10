from rest_framework import serializers
from .models import Challenge, Hint, UserProgress, UserCertificate


class HintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hint
        fields = ["id", "content", "cost", "order"]


class ChallengeSerializer(serializers.ModelSerializer):
    # Determine status/stars dynamically based on user context if needed,
    # but initially we might just return static data or use a separate serializer for list vs detail.
    class Meta:
        model = Challenge
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "initial_code",
            "test_code",
            "order",
            "xp_reward",
            "time_limit",
            "created_for_user_id",
        ]
    
    created_for_user_id = serializers.IntegerField(write_only=True, required=False)


class UserProgressSerializer(serializers.ModelSerializer):
    challenge_id = serializers.IntegerField(source="challenge.id")

    class Meta:
        model = UserProgress
        fields = ["challenge_id", "status", "stars", "completed_at"]


class UserCertificateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    verification_url = serializers.CharField(read_only=True)
    certificate_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UserCertificate
        fields = ['id', 'certificate_id', 'username', 'issued_date', 'is_valid', 
                  'completion_count', 'verification_url', 'certificate_url']
        read_only_fields = ['certificate_id', 'issued_date']
    
    def get_certificate_url(self, obj):
        if obj.certificate_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.certificate_image.url)
        return None
