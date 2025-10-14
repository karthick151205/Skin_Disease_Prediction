import streamlit as st
from PIL import Image
import torch
from transformers import AutoModelForImageClassification, AutoImageProcessor
import os
import pandas as pd
import cv2
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="Skin Lesion Analyzer",
    page_icon="🩺",
    layout="wide",
)

# --- Model and Processor Loading ---
@st.cache_resource
def load_model_and_processor():
    """
    Loads the Hugging Face model and processor from the local directory.
    """
    local_model_path = './'
    # Check if necessary files exist
    required_files = ['config.json', 'model.safetensors', 'preprocessor_config.json']
    if not all(os.path.exists(os.path.join(local_model_path, f)) for f in required_files):
        raise FileNotFoundError("Model files (config.json, model.safetensors, etc.) not found. Please ensure they are in the same directory as the app.")
    
    try:
        processor = AutoImageProcessor.from_pretrained(local_model_path)
        model = AutoModelForImageClassification.from_pretrained(local_model_path)
        return processor, model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Attempt to load the model and handle potential errors
try:
    processor, model = load_model_and_processor()
except FileNotFoundError as e:
    st.error(e)
    processor, model = None, None
except Exception as e:
    st.error(f"A critical error occurred during model loading: {e}")
    processor, model = None, None


# --- Main Application ---
st.title("🩺 Skin Lesion Analyzer")
st.markdown("Upload an image of a skin condition to get a preliminary classification.")
st.warning(
    "**Disclaimer:** This tool is for educational purposes only. It is **not a substitute for professional medical advice**. "
    "Please consult a qualified dermatologist for any health concerns."
)
st.write("---")


if model is not None and processor is not None:
    uploaded_file = st.file_uploader(
        "Choose an image file", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # Create two columns for layout
        col1, col2 = st.columns(2)

        with col1:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Image", use_column_width=True)

        with col2:
            st.subheader("🔬 Analysis Results")
            with st.spinner("Classifying the lesion..."):
                # Preprocess the image using the Hugging Face processor
                inputs = processor(images=image, return_tensors="pt")
                
                # Make prediction
                with torch.no_grad():
                    outputs = model(**inputs)
                
                # Get top prediction and confidence
                logits = outputs.logits
                probabilities = torch.nn.functional.softmax(logits, dim=1)[0]
                predicted_class_idx = probabilities.argmax().item()
                confidence = probabilities[predicted_class_idx].item() * 100
                predicted_class_name = model.config.id2label[predicted_class_idx]

                # Display the top prediction
                st.success(f"**Top Prediction:** {predicted_class_name}")
                st.metric(label="Confidence", value=f"{confidence:.2f}%")
                st.write("---")

                # Display all probabilities in a chart
                st.subheader("Confidence Score for Each Class")
                
                # Create a DataFrame for the bar chart
                class_names = list(model.config.id2label.values())
                prob_df = pd.DataFrame({
                    'Class': class_names,
                    'Probability': probabilities.numpy() 
                })
                
                st.bar_chart(prob_df.set_index('Class'))
else:
    st.warning("Application is not ready. Please resolve the errors displayed above.")