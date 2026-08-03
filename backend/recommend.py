"""
recommend.py — Phase 3: the full pipeline, combining vision.py and search.py.

Give it a photo, and it will:
  1. Ask Gemini to describe each clothing item in the photo (vision.py)
  2. For each item described, search the catalog for similar products (search.py)
  3. Print a clean set of recommendations

This is the core of Fashion Buddy's "image flow" from the original article,
just built with our own code instead of Langflow.
"""

import os
from vision import describe_clothing
from search import search_catalog


def parse_description(description_text: str):
    """
    Turns Gemini's output like:
        "TOPS - White cotton shirt...\nBOTTOMS - Dark jeans..."
    into a list of (category, description) tuples.
    """
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

    # Figure out the media type from the file extension
    ext = os.path.splitext(image_path)[1].lower()
    media_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")

    print("Looking at your photo...\n")
    description = describe_clothing(image_bytes, media_type)
    items = parse_description(description)

    if not items:
        print("Couldn't identify any clothing items in that photo.")
        return

    for category, desc in items:
        print(f"=== {category} ===")
        print(f"What Gemini saw: {desc}\n")

        matches = search_catalog(desc, n_results=2)
        if not matches:
            print("  No similar products found in the catalog.\n")
            continue

        print("  Recommended from our catalog:")
        for m in matches:
            print(f"  - {m['product_name']} (${m['price']}) — {m['link']}")
        print()


if __name__ == "__main__":
    test_image = os.path.join(os.path.dirname(__file__), "..", "data", "test.jpg")
    get_recommendations(test_image)
