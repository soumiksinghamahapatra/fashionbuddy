"""
tryon.py — Phase 7: Virtual try-on.

Given a photo of a person and a photo of a garment, generates an image
of the person wearing that garment.

Uses a free public Hugging Face Space (the IDM-VTON model). The actual
AI model runs on Hugging Face's free shared servers, not your computer
— so no GPU setup or big downloads needed here. It can be slow or
occasionally unavailable since it's a shared free community demo.
"""

from gradio_client import Client, handle_file

# Connects to the public demo hosted at huggingface.co/spaces/yisol/IDM-VTON
_client = Client("yisol/IDM-VTON")


def generate_tryon(person_image_path: str, garment_image_path: str, garment_description: str = ""):
    """
    Returns the file path to the generated "person wearing garment" image.
    """
    result = _client.predict(
        dict={"background": handle_file(person_image_path), "layers": [], "composite": None},
        garm_img=handle_file(garment_image_path),
        garment_des=garment_description,
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon",
    )
    # result is (generated_image_path, mask_image_path)
    return result[0]


if __name__ == "__main__":
    import os
    person = os.path.join(os.path.dirname(__file__), "..", "data", "test.jpg")
    print("This is a manual test — edit this file to point at a person photo and a garment photo.")
