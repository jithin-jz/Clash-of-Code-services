"""
Django Management Command: Load Manual Tasks
Loads 50 manually created challenges into the database.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from challenges.models import Challenge, Hint
from challenges.manual_tasks_data import MANUAL_TASKS


class Command(BaseCommand):
    help = 'Load 50 manual tasks into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing global challenges before loading',
        )

    def handle(self, *args, **options):
        reset = options.get('reset', False)

        if reset:
            self.stdout.write(self.style.WARNING('Deleting all existing global challenges...'))
            Challenge.objects.filter(created_for_user__isnull=True).delete()
            self.stdout.write(self.style.SUCCESS('✓ Deleted existing challenges'))

        self.stdout.write(self.style.HTTP_INFO(f'Loading {len(MANUAL_TASKS)} manual tasks...'))
        
        created_count = 0
        updated_count = 0
        skipped_count = 0

        with transaction.atomic():
            for task_data in MANUAL_TASKS:
                # Extract hint data
                hints_data = task_data.pop('hints', [])
                
                # Check if challenge already exists
                challenge, created = Challenge.objects.update_or_create(
                    slug=task_data['slug'],
                    defaults={
                        'title': task_data['title'],
                        'description': task_data['description'],
                        'initial_code': task_data['initial_code'],
                        'test_code': task_data['test_code'],
                        'order': task_data['order'],
                        'xp_reward': task_data['xp_reward'],
                        'created_for_user': None,  # Global challenge
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Created: {challenge.title}')
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'  ↻ Updated: {challenge.title}')
                    )

                # Create or update hints
                # First, delete existing hints for this challenge to avoid duplicates
                challenge.hints.all().delete()
                
                for hint_data in hints_data:
                    Hint.objects.create(
                        challenge=challenge,
                        content=hint_data['content'],
                        cost=hint_data['cost'],
                        order=hint_data['order']
                    )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'✓ Task Loading Complete!'))
        self.stdout.write(self.style.SUCCESS(f'  - Created: {created_count} challenges'))
        self.stdout.write(self.style.SUCCESS(f'  - Updated: {updated_count} challenges'))
        self.stdout.write(self.style.SUCCESS(f'  - Total: {created_count + updated_count} challenges'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
