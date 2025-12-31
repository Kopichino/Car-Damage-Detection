from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

# Load your custom trained model
# This runs once when the server starts
model = YOLO("car_damage_v1.pt")

@app.get("/")
def home():
    return {"message": "RepairJust AI is Active 🚗"}

@app.post("/detect")
async def detect_damage(file: UploadFile = File(...)):
    # 1. Read the image file sent from the app
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # 2. Feed it to the AI
    results = model.predict(image, conf=0.25)

    # 3. Format the results for the mobile app
    detections = []
    for result in results:
        for box in result.boxes:
            # Get coordinates and label
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            label_name = model.names[class_id]

            detections.append({
                "damage_type": label_name,
                "confidence": round(confidence, 2),
                "bbox": [x1, y1, x2, y2]
            })

    return {"status": "success", "detections": detections}
