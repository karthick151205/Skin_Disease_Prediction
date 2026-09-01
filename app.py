import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
import os
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkinCare AI Assistant",
    page_icon="🔮",
    layout="wide",
)

# ---------------- BLACK & VIOLET THEME ----------------
st.markdown("""
<style>
/* Deep black to dark violet gradient background */
.stApp {
    background: linear-gradient(#4A2DC2, #30309C, #1A1604);
    color: #e0dced;
}

/* Accent headers with a glowing violet */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
}

/* Style the file uploader text */
.stFileUploader label {
    color: #FFFFFF !important;
    font-weight: 600;
}

/* Customizing the progress bar to be bright violet */
.stProgress > div > div > div > div {
    background-color: #9d4edd;
}

/* Custom Info Box for Suggestions */
div.stInfo {
    background-color: rgba(157, 78, 221, 0.1) !important;
    border-left-color: #9d4edd !important;
    color: #e0dced !important;
}

/* FIXED FOOTER STYLING */
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #000000;
    text-align: center;
    padding: 15px;
    font-size: 14px;
    color: #FFFFFF;
    z-index: 999; 
}

/* Add padding to the bottom of the main container */
.block-container {
    padding-bottom: 80px; 
}

/* Hide default Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADING ----------------
st.title("🔮 SkinCare AI Assistant")
st.markdown("---")

# ---------------- CLASS DATA & SUGGESTIONS ----------------
class_codes = ["akiec", "bcc", "bkl", "df", "nv", "mel", "vasc"]

class_details = {
    "akiec": {"name": "Sun Damage Patch"},
    "bcc": {"name": "Basal Cell Carcinoma"},
    "bkl": {"name": "Benign Keratosis"},
    "df": {"name": "Dermatofibroma"},
    "nv": {"name": "Common Mole"},
    "mel": {"name": "Melanoma"},
    "vasc": {"name": "Vascular Lesion"}
}

disease_suggestions = {
    "akiec": "**Actinic Keratoses** are considered precancerous.\n* **Action:** Consult a dermatologist for evaluation.\n* **Care:** Strictly avoid excessive sun exposure and use broad-spectrum sunscreen.",
    "bcc": "**Basal Cell Carcinoma** is a common, highly treatable skin cancer.\n* **Action:** Seek medical evaluation promptly.\n* **Care:** Protect your skin from UV rays with clothing and sunscreen.",
    "bkl": "**Benign Keratosis** refers to harmless skin growths.\n* **Action:** Usually no treatment is needed unless it becomes irritated or bleeds.\n* **Care:** Monitor for any sudden changes in color or rapid growth.",
    "df": "**Dermatofibromas** are common, benign fibrous nodules.\n* **Action:** Harmless and typically require no treatment.\n* **Care:** Consult a doctor if it becomes painful, itchy, or changes appearance.",
    "nv": "**Common Moles** are typically benign.\n* **Action:** Perform regular self-exams using the ABCDE rule (Asymmetry, Border, Color, Diameter, Evolving).\n* **Care:** Always use sun protection to prevent cellular changes.",
    "mel": "**Melanoma** is a serious form of skin cancer.\n* **Action:** 🚨 **URGENT:** Please consult a healthcare provider immediately for a professional biopsy.\n* **Care:** Avoid sun exposure completely until evaluated.",
    "vasc": "**Vascular Lesions** are usually benign overgrowths of blood vessels.\n* **Action:** Generally harmless. Treatment is usually only for cosmetic reasons.\n* **Care:** Monitor for unusual bleeding or rapid expansion."
}

# --- NEW: Specific medical links for each condition ---
disease_resources = {
    "akiec": "https://www.skincancer.org/skin-cancer-information/actinic-keratosis/",
    "bcc": "https://www.skincancer.org/skin-cancer-information/basal-cell-carcinoma/",
    "bkl": "https://www.aocd.org/page/SeborrheicKeratoses",
    "df": "https://www.aocd.org/page/Dermatofibroma",
    "nv": "https://www.skincancer.org/skin-cancer-information/melanoma/melanoma-warning-signs-and-images/",
    "mel": "https://www.skincancer.org/skin-cancer-information/melanoma/",
    "vasc": "https://www.hopkinsmedicine.org/health/conditions-and-diseases/vascular-lesions"
}

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    processor = AutoImageProcessor.from_pretrained("./")
    model = AutoModelForImageClassification.from_pretrained("./")
    model.eval()
    return processor, model

try:
    processor, model = load_model()
except Exception as e:
    st.error(f"Error loading model. Please ensure model files are in the root directory. Details: {e}")
    st.stop()

# ---------------- MAIN TWO COLUMN LAYOUT ----------------
left_col, right_col = st.columns([1, 1.2], gap="large")

# ---------- LEFT SIDE (UPLOAD) ----------
with left_col:
    st.subheader("📤 Upload Image")
    st.markdown("Please upload a clear, well-lit image of the skin lesion.")
    
    uploaded_file = st.file_uploader(
        "Choose a skin lesion image",
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_container_width=True)

# ---------- RIGHT SIDE (RESULTS) ----------
with right_col:
    if uploaded_file:
        st.subheader("🔬 Analysis Result")

        with st.spinner("Our AI is analyzing the image..."):
            inputs = processor(images=image, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)

            probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
            top_probs, top_indices = torch.topk(probs, len(class_codes))

            # Primary Prediction
            predicted_index = top_indices[0].item()
            predicted_code = class_codes[predicted_index]
            predicted_name = class_details[predicted_code]["name"]
            confidence = top_probs[0].item() * 100

            st.metric(label="Primary Prediction", value=predicted_name, delta=f"{confidence:.2f}% Confidence", delta_color="normal")
            st.divider()

            # Percentage Breakdown
            st.subheader("📈 Detailed Breakdown")
            for i in range(len(class_codes)):
                idx = top_indices[i].item()
                code = class_codes[idx]
                condition_name = class_details[code]["name"]
                prob_value = top_probs[i].item()
                
                col_text, col_percent = st.columns([3, 1])
                with col_text:
                    st.write(f"**{condition_name}**")
                with col_percent:
                    st.write(f"{prob_value * 100:.1f}%")
                
                st.progress(prob_value)

            st.divider()
            
            # Bar Graph
            st.subheader("📊 Comparative Chart")
            friendly_names = [class_details[class_codes[idx.item()]]["name"] for idx in top_indices]
            prob_df = pd.DataFrame({
                "Condition": friendly_names,
                "Confidence (%)": (top_probs.numpy() * 100)
            })
            st.bar_chart(prob_df.set_index("Condition"), color="#9d4edd")

    else:
        st.info("Upload an image on the left to see the AI analysis results here.")

# ---------- LEFT SIDE (SUGGESTIONS & RESOURCES) ----------
if uploaded_file:
    with left_col:
        st.subheader("💡 Suggestions & Care")
        
        # Advice Box
        advice_text = disease_suggestions.get(predicted_code, "Consult a medical professional for advice.")
        st.info(advice_text, icon="ℹ️")
        
        st.write("") # Quick spacing
        st.subheader("🏥 Next Steps & Resources")
        
        # Specific Condition Link Button
        if predicted_code in disease_resources:
            url = disease_resources[predicted_code]
            st.link_button(f"📖 Read more about {predicted_name}", url, use_container_width=True)
            
        # Generic Google Maps Search Button for Dermatologists
        st.link_button("📍 Find a Dermatologist Near Me", "https://www.google.com/maps/search/dermatologists+near+me/", use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    <strong>Disclaimer:</strong> This tool is for educational purposes only. It is an AI-assisted clinical support tool and should not replace professional medical advice or diagnosis.
</div>
""", unsafe_allow_html=True)