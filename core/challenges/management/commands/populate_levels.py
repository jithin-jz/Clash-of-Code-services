from django.core.management.base import BaseCommand
from challenges.models import Challenge
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with 25 initial challenges'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating levels...')
        
        # Define some basic tasks to start with
        tasks = [
            ("Print Hello World", "Write a python function `solve` that prints 'Hello World'.", "def solve():\n    pass", "import sys\nfrom io import StringIO\n\ndef check():\n    capturedOutput = StringIO()\n    sys.stdout = capturedOutput\n    solve()\n    sys.stdout = sys.__stdout__\n    assert capturedOutput.getvalue().strip() == 'Hello World', 'Output must be Hello World'"),
            ("Sum of Two Numbers", "Write a function `add(a, b)` that returns the sum of a and b.", "def add(a, b):\n    pass", "assert add(2, 3) == 5\nassert add(-1, 1) == 0"),
        ]

        # Populate defined tasks first
        for i, (title, desc, code, test) in enumerate(tasks, 1):
            Challenge.objects.get_or_create(
                order=i,
                defaults={
                    'title': title,
                    'slug': slugify(title),
                    'description': desc,
                    'initial_code': code,
                    'test_code': test,
                    'xp_reward': 50
                }
            )

        # Fill the rest up to 25 with placeholders
        for i in range(len(tasks) + 1, 26):
            title = f"Task {i}"
            Challenge.objects.get_or_create(
                order=i,
                defaults={
                    'title': title,
                    'slug': f"task-{i}",
                    'description': f"This is a placeholder for Level {i}. Implement a solution.",
                    'initial_code': "def solve():\n    # Your code here\n    pass",
                    'test_code': "def check():\n    pass",
                    'xp_reward': 50 + (i * 10) # Increasing XP
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated 25 challenges'))
