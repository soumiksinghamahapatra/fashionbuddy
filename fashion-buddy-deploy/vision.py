"""
vision.py — uses Google Gemini (free tier) to identify and describe
clothing items in an image.
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

CLOTHING_IDENTIFIER_PROMPT = """You are a clothing identifier.
From the photo, you are only identifying pieces of clothing in the picture and
describing the pieces that you identify in great detail. Be as descriptive as
possible about fabric, color, cut, and style.

Ignore anything else in the image — if there is a model wearing the clothing,
ignore them. If there is anything in the background, ignore that too. Only
focus on the clothing items.

Only use these categories:
TOPS, BOTTOMS, SHOES, ACCESSORIES, OUTERWEAR, ACTIVEWEAR, DRESSES_JUMPSUITS

Format your response exactly like this, one line per item:
TOPS - White cotton shirt with short sleeves and a button-down collar...
SHOES - Black leather loafers with a rounded toe...

Do not include any other commentary, just the formatted list."""


def describe_clothing(image_bytes: bytes, media_type: str = "image/jpeg") -> str:
    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(
        [
            {"mime_type": media_type, "data": image_bytes},
            CLOTHING_IDENTIFIER_PROMPT,
        ]
    )
    return response.text.strip()
