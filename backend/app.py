"""
app.py — Phase 5: a simple web server (FastAPI) that puts a real webpage
in front of everything we built in Phases 1-4.

Run this, then open your browser to http://127.0.0.1:8000
"""

import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from vision import describe_clothing
from web_search import find_products, find_garment_with_image, find_garment_options
from recommend import parse_description
from tryon import generate_tryon

app = FastAPI()

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "static", "generated")
os.makedirs(UPLOADS_DIR, exist_ok=True)


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/recommend/image")
async def recommend_image(file: UploadFile = File(...)):
    """Called when the user uploads a photo in the browser."""
    image_bytes = await file.read()
    media_type = file.content_type or "image/jpeg"

    description = describe_clothing(image_bytes, media_type)
    items = parse_description(description)

    results = []
    for category, desc in items:
        matches = find_products(desc, max_results=3)
        results.append({"category": category, "description": desc, "matches": matches})

    return {"results": results}


@app.post("/recommend/text")
async def recommend_text(query: str = Form(...)):
    """Called when the user types a search query in the browser."""
    matches = find_products(query, max_results=4)
    return {"results": [{"category": "SEARCH RESULTS", "description": query, "matches": matches}]}


@app.post("/find_garments")
async def find_garments(query: str = Form(...)):
    """Called when the user searches, before picking an option to try on."""
    options = find_garment_options(query, max_results=4)
    return {"options": options}


@app.post("/tryon_with_image")
async def tryon_with_image(
    person_photo: UploadFile = File(...),
    garment_image_url: str = Form(...),
    product_link: str = Form(""),
    product_title: str = Form(""),
):
    """Called once the user picks a specific option to try on."""
    request_id = uuid.uuid4().hex[:8]
    person_path = os.path.join(UPLOADS_DIR, f"{request_id}_person.jpg")
    with open(person_path, "wb") as f:
        shutil.copyfileobj(person_photo.file, f)

    try:
        result_path = generate_tryon(person_path, garment_image_url)
    except Exception as e:
        return {"error": f"Try-on failed (the free demo may be busy or offline): {e}"}

    output_filename = f"{request_id}_result.png"
    output_path = os.path.join(UPLOADS_DIR, output_filename)
    shutil.copyfile(result_path, output_path)

    return {"image_url": f"/static/generated/{output_filename}", "product_link": product_link, "product_title": product_title}


@app.post("/auto_tryon")
async def auto_tryon(person_photo: UploadFile = File(...), query: str = Form(...)):
    """
    Called when the user uploads only a person photo + types what they want
    to wear. Automatically finds a real product image and generates the try-on.
    """
    request_id = uuid.uuid4().hex[:8]
    person_path = os.path.join(UPLOADS_DIR, f"{request_id}_person.jpg")
    with open(person_path, "wb") as f:
        shutil.copyfileobj(person_photo.file, f)

    garment = find_garment_with_image(query)
    if not garment or not garment.get("image_url"):
        return {"error": "Couldn't find a product image for that. Try describing it differently."}

    try:
        result_path = generate_tryon(person_path, garment["image_url"])
    except Exception as e:
        return {"error": f"Try-on failed (the free demo may be busy or offline): {e}"}

    output_filename = f"{request_id}_result.png"
    output_path = os.path.join(UPLOADS_DIR, output_filename)
    shutil.copyfile(result_path, output_path)

    return {
        "image_url": f"/static/generated/{output_filename}",
        "product_link": garment.get("product_link"),
        "product_title": garment.get("product_title"),
    }


@app.post("/tryon")
async def tryon(person_photo: UploadFile = File(...), garment_photo: UploadFile = File(...)):
    """Called when the user uploads both a person photo and a garment photo."""
    request_id = uuid.uuid4().hex[:8]
    person_path = os.path.join(UPLOADS_DIR, f"{request_id}_person.jpg")
    garment_path = os.path.join(UPLOADS_DIR, f"{request_id}_garment.jpg")

    with open(person_path, "wb") as f:
        shutil.copyfileobj(person_photo.file, f)
    with open(garment_path, "wb") as f:
        shutil.copyfileobj(garment_photo.file, f)

    try:
        result_path = generate_tryon(person_path, garment_path)
    except Exception as e:
        return {"error": f"Try-on failed (the free demo may be busy or offline): {e}"}

    # Copy the result into our own static/generated folder so the browser can load it
    output_filename = f"{request_id}_result.png"
    output_path = os.path.join(UPLOADS_DIR, output_filename)
    shutil.copyfile(result_path, output_path)

    return {"image_url": f"/static/generated/{output_filename}"}


# This makes files in the "static" folder (like our webpage) accessible
# in the browser. Must come after the routes above.
app.mount("/static", StaticFiles(directory="static"), name="static")
