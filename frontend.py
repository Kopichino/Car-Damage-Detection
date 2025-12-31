import streamlit as st
import requests
from PIL import Image
import io

# TITLE AND LOGO
st.set_page_config(page_title="RepairJust", page_icon="🚗")
st.title("🚗 RepairJust AI")
st.write("Instant Car Damage Repair Estimator")

# SIDEBAR / INPUTS
st.sidebar.header("Car Details")
car_model = st.sidebar.selectbox("Select Car Model", ["Swift", "City", "Creta", "Generic"])
car_year = st.sidebar.slider("Car Year", 2010, 2025, 2022)
part_name = st.sidebar.selectbox("Damaged Part", ["Bumper", "Door", "Hood", "Headlight", "Fender"])

# CAMERA INPUT (Works on Mobile & Laptop)
st.write("### 1. Upload or Take a Photo")
enable_camera = st.checkbox("Use Camera")
image_file = None

if enable_camera:
    image_file = st.camera_input("Take a picture of the damage")
else:
    image_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

# THE ACTION BUTTON
if image_file is not None:
    # Show the image to the user
    st.image(image_file, caption="Selected Image", use_column_width=True)
    
    if st.button("💰 Get Repair Estimate"):
        with st.spinner("Analyzing damage..."):
            
            # 1. Prepare Data for API
            files = {"file": image_file.getvalue()}
            data = {
                "car_model": car_model,
                "car_year": car_year,
                "part_name": part_name
            }

            # 2. Call the Backend API (Ensure backend is running!)
            try:
                # IMPORTANT: If running on same laptop, use localhost
                response = requests.post("http://127.0.0.1:8000/estimate", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 3. Display Results Beautifully
                    st.success("Analysis Complete!")
                    
                    # Big Price Tag
                    st.metric(label="Estimated Repair Cost", value=result.get("total_estimate", "N/A"))
                    
                    # Breakdown Table
                    if "breakdown" in result:
                        st.write("### 🧾 Cost Breakdown")
                        for item in result["breakdown"]:
                            st.info(f"**{item['damage_detected'].upper()}** on {item['part_context']}")
                            st.write(f"severity: {item['severity_multiplier']}x")
                            st.write(f"Cost: ₹{item['cost_for_this_damage']}")
                    
                    st.warning(f"Note: This is an estimate for a {result.get('car_info', 'car')}.")
                    
                else:
                    st.error("Error connecting to server.")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Connection Failed. Is the backend running? Error: {e}")