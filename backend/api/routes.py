from fastapi import APIRouter, UploadFile, File, Form
from model.detector import detect_fire_and_save

router = APIRouter()

@router.post("/detect_fire/")
async def detect_fire(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    result = await detect_fire_and_save(file, latitude, longitude)
    result["latitude"] = latitude
    result["longitude"] = longitude
    return result
