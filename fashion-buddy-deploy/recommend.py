"""
recommend.py — combines vision.py + web_search.py: photo in, real
product recommendations out. Also used by app.py for parse_description.
"""

import os
from vision import describe_clothing
from web_search import find_products


def parse_description(description_text: str):
    """Turns Gemini's "CATEGORY - description" lines into (category, description) tuples."""
    items = []
    for line in description_text.strip().split("\n"):
        line = line.strip()
        if not line or " - " not in line:
            continue
        category, desc = line.split(" - ", 1)
        items.append((category.strip(), desc.strip()))
    return items


def get_recommendations(image_path: str):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    ext = os.path.splitext(image_path)[1].lower()
    media_type = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(ext, "image/jpeg")

    print("Looking at your photo...\n")
    description = describe_clothing(image_bytes, media_type)
    items = parse_description(description)

    if not items:
        print("Couldn't identify any clothing items in that photo.")
        return

    for category, desc in items:
        print(f"=== {category} ===")
        print(f"What Gemini saw: {desc}\n")
        matches = find_products(desc, max_results=2)
        if not matches:
            print("  No similar products found.\n")
            continue
        print("  Recommended:")
        for m in matches:
            print(f"  - {m['product_name']} — {m['link']}")
        print()
