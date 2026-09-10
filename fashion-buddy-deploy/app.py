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
    matches = find_products(query, max_results=4)
    return {"results": [{"category": "SEARCH RESULTS", "description": query, "matches": matches}]}


@app.post("/find_garments")
async def find_garments(query: str = Form(...)):
    options = find_garment_options(query, max_results=4)
    return {"options": options}


@app.post("/tryon_with_image")
async def tryon_with_image(
    person_photo: UploadFile = File(...),
    garment_image_url: str = Form(...),
    product_link: str = Form(""),
    product_title: str = Form(""),
):
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

    output_filename = f"{request_id}_result.png"
    output_path = os.path.join(UPLOADS_DIR, output_filename)
    shutil.copyfile(result_path, output_path)

    return {"image_url": f"/static/generated/{output_filename}"}


app.mount("/static", StaticFiles(directory="static"), name="static")
