import os, sys, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from challenges.models import Challenge, UserProgress
from challenges.levels import LEVELS
from store.models import StoreItem

# ──────────────────────────────────────────────
#  CLEAR EXISTING DATA
# ──────────────────────────────────────────────
print("\n🗑️  Clearing existing data...")
UserProgress.objects.all().delete()
print("  ✅ Cleared UserProgress")
Challenge.objects.all().delete()
print("  ✅ Cleared Challenges")

# ──────────────────────────────────────────────
#  SEED CHALLENGES FROM levels.py
# ──────────────────────────────────────────────
print(f"\n🎮 Seeding {len(LEVELS)} challenges from levels.py...")
for lvl in LEVELS:
    obj = Challenge.objects.create(
        title=lvl["title"],
        slug=lvl["slug"],
        description=lvl["description"],
        initial_code=lvl["initial_code"],
        test_code=lvl["test_code"],
        order=lvl["order"],
        xp_reward=lvl["xp_reward"],
        target_time_seconds=lvl["target_time_seconds"],
    )
    print(f"  ✅ Level {lvl['order']:>2}: {lvl['title']}")

print(f"\n  Total challenges: {Challenge.objects.count()}")

# ──────────────────────────────────────────────
#  SEED STORE ITEMS
# ──────────────────────────────────────────────
store_items_data = [
    {
        "name": "Dracula",
        "description": "A dark theme with purple accents. Classic vampire aesthetic for late-night coding.",
        "cost": 100,
        "icon_name": "moon",
        "category": "THEME",
        "item_data": {"theme_key": "dracula"},
        "image": "/store/dracula.png",
    },
    {
        "name": "Nord",
        "description": "An arctic, north-bluish color palette. Clean, minimal, and easy on the eyes.",
        "cost": 100,
        "icon_name": "snowflake",
        "category": "THEME",
        "item_data": {"theme_key": "nord"},
        "image": "/store/nord.png",
    },
    {
        "name": "Monokai",
        "description": "The legendary Monokai theme. Vibrant colors on a dark background.",
        "cost": 150,
        "icon_name": "palette",
        "category": "THEME",
        "item_data": {"theme_key": "monokai"},
        "image": "/store/monokai.png",
    },
    {
        "name": "Solarized Dark",
        "description": "Precision colors for machines and people.",
        "cost": 150,
        "icon_name": "sun",
        "category": "THEME",
        "item_data": {"theme_key": "solarized_dark"},
        "image": "/store/solarized.png",
    },
    {
        "name": "Cyberpunk",
        "description": "Neon lights and dark streets. Code with the aesthetic of the future.",
        "cost": 200,
        "icon_name": "zap",
        "category": "THEME",
        "item_data": {"theme_key": "cyberpunk"},
        "image": "/store/cyberpunk.png",
    },
    {
        "name": "JetBrains Mono",
        "description": "A typeface for developers. Increased height for better readability.",
        "cost": 75,
        "icon_name": "type",
        "category": "FONT",
        "item_data": {"font_family": "JetBrains Mono"},
    },
    {
        "name": "Fira Code",
        "description": "Monospaced font with programming ligatures.",
        "cost": 75,
        "icon_name": "type",
        "category": "FONT",
        "item_data": {"font_family": "Fira Code"},
    },
    {
        "name": "Comic Code",
        "description": "A fun comic-style monospaced font. Because coding should be fun!",
        "cost": 120,
        "icon_name": "smile",
        "category": "FONT",
        "item_data": {"font_family": "Comic Code"},
    },
    {
        "name": "Sparkle Trail",
        "description": "Leave a trail of sparkles as you type.",
        "cost": 200,
        "icon_name": "sparkles",
        "category": "EFFECT",
        "item_data": {"effect_key": "sparkle"},
    },
    {
        "name": "Matrix Rain",
        "description": "Digital rain follows your cursor.",
        "cost": 250,
        "icon_name": "binary",
        "category": "EFFECT",
        "item_data": {"effect_key": "matrix"},
    },
    {
        "name": "Fire Trail",
        "description": "Your code is on fire! Flames follow every keystroke.",
        "cost": 300,
        "icon_name": "flame",
        "category": "EFFECT",
        "item_data": {"effect_key": "fire"},
    },
    {
        "name": "Confetti Burst",
        "description": "Celebrate with colorful confetti on level completion!",
        "cost": 150,
        "icon_name": "party-popper",
        "category": "VICTORY",
        "item_data": {"victory_key": "confetti"},
    },
    {
        "name": "Fireworks",
        "description": "Light up the sky with fireworks when you conquer a challenge!",
        "cost": 250,
        "icon_name": "rocket",
        "category": "VICTORY",
        "item_data": {"victory_key": "fireworks"},
    },
]

print("\n🏪 Seeding Store Items...")
for item in store_items_data:
    obj, created = StoreItem.objects.update_or_create(
        name=item["name"],
        defaults={
            "description": item["description"],
            "cost": item["cost"],
            "icon_name": item["icon_name"],
            "category": item["category"],
            "item_data": item.get("item_data", {}),
            "image": item.get("image", ""),
        },
    )
    status = "✅ Created" if created else "🔄 Updated"
    print(f"  {status}: {item['name']} ({item['category']}) - {item['cost']} XP")

print(f"\n  Total store items: {StoreItem.objects.count()}")
print("\n🎉 Database seeding complete!")
