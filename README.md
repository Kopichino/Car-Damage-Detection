# 🚗 RepairJust - AI Vehicle Damage Estimator

> **InsurTech Solution:** Automating car repair estimates using Computer Vision and Deep Learning.

![Project Status](https://img.shields.io/badge/Status-Prototype-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI Model](https://img.shields.io/badge/Model-YOLOv8-orange)
![Backend](https://img.shields.io/badge/Backend-FastAPI-teal)

## 📖 Overview
**RepairJust** is an AI-powered system designed to bridge the gap between vehicle owners, mechanics, and insurance companies.

Traditionally, getting a repair quote involves visiting a shop, waiting for an inspection, and negotiating prices. **RepairJust** solves this by analyzing photos of vehicle damage and generating an instant, localized cost estimate based on the car model and severity of damage.

---

## ✨ Features
* **🔍 AI Damage Detection:** Automatically identifies dents, scratches, shattered glass, and broken lamps using a custom-trained YOLOv8 model.
* **💰 Instant Cost Estimation:** Innovative pricing algorithm that calculates repair costs based on:
  * Car Model (e.g., Swift vs. Creta)
  * Part Price (e.g., Bumper vs. Door)
  * Damage Severity (e.g., Scratch vs. Deep Dent)
* **📱 User-Friendly Interface:** Simple web/mobile interface for uploading photos and viewing quotes.
* **⚡ Fast API:** Built on FastAPI for high-performance, real-time inference.

---

## 🛠️ Tech Stack
* **Deep Learning:** YOLOv8 (Ultralytics) trained on the CarDD dataset  
* **Backend:** FastAPI (Python)  
* **Frontend:** Streamlit  
* **Pricing Logic:** Custom rule-based engine simulating mechanic labor/part costs  
* **Deployment:** Ready for Docker / AWS EC2  

---

## 📂 Project Structure
```bash
repairjust_backend/
├── main.py              # The Brain: FastAPI Backend & Pricing Logic
├── frontend.py          # The Face: Streamlit User Interface
├── car_damage_v1.pt     # The Core: Trained YOLOv8 Model Weights
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.9+
- Git

---

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/repairjust.git
cd repairjust
```

---

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install fastapi uvicorn ultralytics python-multipart pillow streamlit requests
```

---

### **3. Add the Model**
Place your trained model file **car_damage_v1.pt** in the project root directory.

---

## 🏃‍♂️ How to Run

You will run **two terminals**: backend + frontend.

---

### **Terminal 1 — Start the Backend (FastAPI)**
```bash
uvicorn main:app --reload
```

Backend URL:  
➡️ http://127.0.0.1:8000  

---

### **Terminal 2 — Start the Frontend (Streamlit)**
```bash
streamlit run frontend.py
```

Frontend UI opens at:  
➡️ http://localhost:8501  

---

## 🔌 API Documentation

Once backend is running, API docs available at:

➡️ http://127.0.0.1:8000/docs  

### **Endpoints**

#### **GET /**  
Health check endpoint.

#### **POST /estimate**  
**Inputs:**  
- Image file  
- Car Model  
- Year  
- Part Name  

**Outputs:**  
- Detected damage  
- Confidence score  
- Estimated price range (Min/Max)

---

## 🔮 Future Roadmap (Startup Goals)

- [ ] **Mechanic Integration:** Connect users with verified nearby repair shops  
- [ ] **Insurance API:** Integrate with insurance company workflows  
- [ ] **3D Damage Analysis:** Multi-angle photo-based volumetric assessment  
- [ ] **Part Procurement:** Auto-order replacement parts  

---

## 📝 License
This project is for educational and prototyping purposes.

---

## 📦 Bonus: `requirements.txt`

Create a file named **requirements.txt** and paste:

```text
fastapi
uvicorn
ultralytics
python-multipart
pillow
streamlit
requests
numpy
```

