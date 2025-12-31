from fastapi import FastAPI, UploadFile, File, Form
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

# 1. LOAD AI MODEL
try:
    model = YOLO("car_damage_v1.pt")
except:
    model = None

# --- THE PRICING BRAIN ---

# A. Base prices for parts (in Rupees)
# You can expand this list later or fetch it from a real database
CAR_PARTS_DB = {
    "swift": {
        "bumper": 2500, "door": 4500, "hood": 3500, "headlight": 1800, "fender": 1200
    },
    "city": {
        "bumper": 6500, "door": 8500, "hood": 7000, "headlight": 4500, "fender": 3200
    },
    "creta": {
        "bumper": 5500, "door": 7000, "hood": 6000, "headlight": 4000, "fender": 2800
    },
    # Fallback for unknown cars
    "generic": {
        "bumper": 3500, "door": 5000, "hood": 4000, "headlight": 2500, "fender": 1500
    }
}

# B. Multipliers based on Damage Type (AI Detection)
# "How much of the part cost does it take to fix this?"
# 0.5 = 50% of replacement cost. 1.5 = Replacement + Extra Labor.
DAMAGE_LOGIC = {
    "dent": 0.40,          # Dents usually cost 40% of a new part to fix
    "scratch": 0.15,       # Scratches are cheap (buffing/painting)
    "glass shatter": 1.10, # 110% (Part price + Installation labor)
    "lamp broken": 1.10,   # 110% (Replacement + Labor)
    "crack": 0.50,         # Plastic welding or filling
    "tire flat": 0.05      # Very cheap relative to car value
}

@app.get("/")
def home():
    return {"message": "RepairJust Advanced Pricing Engine 💰"}

@app.post("/estimate")
async def get_estimate(
    car_model: str = Form(...),      # User Input: "swift"
    car_year: int = Form(...),       # User Input: 2020
    part_name: str = Form(...),      # User Input: "bumper"
    file: UploadFile = File(...)     # User Input: Image
):
    if model is None:
        return {"error": "AI Model not loaded."}

    # 1. Normalize Inputs (Handle case sensitivity)
    model_key = car_model.lower().strip()
    part_key = part_name.lower().strip()

    # 2. Find Base Price of the Part
    # Logic: Look for the specific car, if not found, use "generic"
    car_data = CAR_PARTS_DB.get(model_key, CAR_PARTS_DB["generic"])
    
    # Logic: Look for the specific part, if not found, default to 3000
    base_part_price = car_data.get(part_key, 3000)

    # 3. Adjust for Car Year (Inflation Logic)
    # Older cars might have cheaper parts, or identical. Let's keep it simple for now.
    # If car is very new (>2023), add 10% premium.
    if car_year >= 2023:
        base_part_price = int(base_part_price * 1.1)

    # 4. Run AI on the Image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    results = model.predict(image, conf=0.25)

    detected_damages = []
    final_estimate_min = 0
    final_estimate_max = 0

    # 5. Calculate Final Price
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            damage_type = model.names[class_id] # e.g., "dent"
            confidence = float(box.conf[0])

            # Get the multiplier (default to 0.5 if unknown damage)
            multiplier = DAMAGE_LOGIC.get(damage_type, 0.5)

            # CALCULATION:
            # Min Estimate = Base Price * Multiplier
            # Max Estimate = Min Estimate + 20% buffer
            estimated_cost = int(base_part_price * multiplier)
            
            # Accumulate totals
            final_estimate_min += estimated_cost
            final_estimate_max += int(estimated_cost * 1.2) # Add 20% buffer

            detected_damages.append({
                "damage_detected": damage_type,
                "part_context": part_name,
                "base_part_price": base_part_price,
                "severity_multiplier": multiplier,
                "cost_for_this_damage": estimated_cost
            })

    # Handle case where AI finds nothing
    if not detected_damages:
        return {
            "status": "partial_success",
            "message": "No visible damage detected by AI.",
            "base_part_price": base_part_price
        }

    return {
        "car_info": f"{car_model} ({car_year})",
        "part_selected": part_name,
        "breakdown": detected_damages,
        "total_estimate": f"₹{final_estimate_min} - ₹{final_estimate_max}",
        "currency": "INR"
    }