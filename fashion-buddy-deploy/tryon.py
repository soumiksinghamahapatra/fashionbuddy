"""
tryon.py — Virtual try-on using a free public Hugging Face Space
(the IDM-VTON model). Runs on Hugging Face's free shared servers.
"""

import os
from gradio_client import Client, handle_file

_client = Client("yisol/IDM-VTON", hf_token=os.environ.get("HF_TOKEN") or None)


def generate_tryon(person_image_path: str, garment_image_path: str, garment_description: str = ""):
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
    return result[0]
