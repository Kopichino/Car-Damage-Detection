from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

# Load the model (Ensure car_damage_v1.pt is in the same folder)
# If you don't have the file yet, comment this line out to test the server first
try:
    model = YOLO("car_damage_v1.pt")
    print("✅ Model loaded successfully!")
except:
    print("⚠️ Model file not found. Please download 'best.pt' from Kaggle.")
    model = None

@app.get("/")
def home():
    return {"message": "RepairJust AI is Active 🚗"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return {"error": "Model not loaded. Check server logs."}

    # 1. Read the image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # 2. Run the AI
    results = model.predict(image, conf=0.25)

    # 3. Extract Data
    detections = []
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            confidence = float(box.conf[0])
            
            detections.append({
                "damage": label,
                "confidence": round(confidence, 2)
            })

    return {
        "filename": file.filename,
        "detections": detections,
        "total_damages": len(detections)
    }