from django.apps import AppConfig


class ChallengesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "challenges"

    def ready(self):
        import challenges.signals
        from .dynamo import dynamo_challenge_client
        dynamo_challenge_client.create_table_if_not_exists()
