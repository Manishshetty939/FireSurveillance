import uuid
import os
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
from db.db_utils import insert_fire_alert

# Load your trained YOLOv8 model
model = YOLO("models/best.pt")

# Folder to save snapshots
SNAPSHOT_DIR = "snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

async def detect_fire_and_save(file, latitude, longitude):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model.predict(image, imgsz=640, conf=0.5)

    fire_detected = False
    confidence = 0

    for result in results:
        boxes = result.boxes
        if boxes and len(boxes) > 0:
            fire_detected = True
            confidence = float(boxes.conf[0])
            break

    if fire_detected:
        snapshot_name = f"{uuid.uuid4().hex}.jpg"
        snapshot_path = os.path.join(SNAPSHOT_DIR, snapshot_name)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        Image.fromarray(image_rgb).save(snapshot_path)

        # Save to PostgreSQL
        insert_fire_alert("Fire Detected", confidence, snapshot_path.replace("\\", "/"), latitude, longitude)

        return {
            "status": "Fire Detected",
            "confidence": confidence,
            "image": snapshot_path.replace("\\", "/")
        }

    # Save to PostgreSQL even if no fire detected
    insert_fire_alert("No Fire Detected", confidence, "", latitude, longitude)

    return {"status": "No Fire Detected"}

