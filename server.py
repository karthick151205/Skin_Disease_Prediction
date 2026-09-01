import os
import io
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from transformers import AutoModelForImageClassification, AutoImageProcessor
from contextlib import asynccontextmanager

# Global variables for model and processor
processor = None
model = None

DISEASE_METADATA = {
    "benign_keratosis-like_lesions": {
        "code": "bkl",
        "name": "Benign Keratosis",
        "category": "Benign Growth",
        "risk_level": "low",
        "risk_label": "Benign (Harmless)",
        "badge_color": "green",
        "description": "Harmless skin growths such as seborrheic keratosis or solar lentigines.",
        "action": "Usually no treatment is needed unless it becomes irritated or bleeds.",
        "care": "Monitor periodically for any sudden changes in shape, size, or color.",
        "resource_url": "https://www.aocd.org/page/SeborrheicKeratoses"
    },
    "basal_cell_carcinoma": {
        "code": "bcc",
        "name": "Basal Cell Carcinoma",
        "category": "Skin Malignancy",
        "risk_level": "moderate",
        "risk_label": "Moderate Risk - Treatable Cancer",
        "badge_color": "amber",
        "description": "A common, highly treatable form of skin cancer that grows slowly.",
        "action": "Seek medical evaluation promptly for diagnosis and removal options.",
        "care": "Protect skin from UV rays with broad-spectrum sunscreen and protective clothing.",
        "resource_url": "https://www.skincancer.org/skin-cancer-information/basal-cell-carcinoma/"
    },
    "actinic_keratoses": {
        "code": "akiec",
        "name": "Actinic Keratosis",
        "category": "Precancerous Lesion",
        "risk_level": "moderate",
        "risk_label": "Precancerous Patch",
        "badge_color": "amber",
        "description": "Rough, scaly patches caused by long-term sun exposure that can develop into skin cancer.",
        "action": "Consult a dermatologist for professional evaluation and treatment options.",
        "care": "Strictly avoid excessive sun exposure and regularly use broad-spectrum SPF 50+ sunscreen.",
        "resource_url": "https://www.skincancer.org/skin-cancer-information/actinic-keratosis/"
    },
    "vascular_lesions": {
        "code": "vasc",
        "name": "Vascular Lesion",
        "category": "Vascular Overgrowth",
        "risk_level": "low",
        "risk_label": "Benign (Harmless)",
        "badge_color": "green",
        "description": "Benign overgrowth of blood vessels (such as cherry angiomas or hemangiomas).",
        "action": "Generally harmless. Medical treatment is usually only needed for cosmetic reasons.",
        "care": "Monitor for unusual bleeding or sudden expansion.",
        "resource_url": "https://www.hopkinsmedicine.org/health/conditions-and-diseases/vascular-lesions"
    },
    "melanocytic_Nevi": {
        "code": "nv",
        "name": "Common Mole (Nevus)",
        "category": "Pigmented Lesion",
        "risk_level": "low",
        "risk_label": "Benign (Normal Mole)",
        "badge_color": "green",
        "description": "Typical benign pigmented lesion composed of melanocyte cells.",
        "action": "Perform regular monthly self-exams using the ABCDE rule.",
        "care": "Apply sunscreen daily to prevent cellular mutations.",
        "resource_url": "https://www.skincancer.org/skin-cancer-information/melanoma/melanoma-warning-signs-and-images/"
    },
    "melanoma": {
        "code": "mel",
        "name": "Melanoma",
        "category": "High-Risk Malignancy",
        "risk_level": "urgent",
        "risk_label": "URGENT - High Risk Malignancy",
        "badge_color": "red",
        "description": "A serious form of skin cancer arising from pigment-producing melanocytes.",
        "action": "URGENT: Consult a qualified dermatologist or doctor immediately for evaluation and biopsy.",
        "care": "Avoid direct sun exposure completely on the area until professional examination.",
        "resource_url": "https://www.skincancer.org/skin-cancer-information/melanoma/"
    },
    "dermatofibroma": {
        "code": "df",
        "name": "Dermatofibroma",
        "category": "Benign Nodule",
        "risk_level": "low",
        "risk_label": "Benign Nodule",
        "badge_color": "green",
        "description": "Common, benign fibrous skin nodule typically occurring on lower legs.",
        "action": "Harmless and typically requires no treatment.",
        "care": "Consult a doctor if it becomes painful, itchy, or rapidly changes appearance.",
        "resource_url": "https://www.aocd.org/page/Dermatofibroma"
    }
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global processor, model
    model_path = os.path.abspath(".")
    print(f"[FASTAPI] Loading Vision Transformer model from {model_path}...")
    try:
        processor = AutoImageProcessor.from_pretrained(model_path)
        model = AutoModelForImageClassification.from_pretrained(model_path)
        model.eval()
        print("[FASTAPI] Model loaded successfully!")
    except Exception as e:
        print(f"[FASTAPI ERROR] Failed to load model: {e}")
        raise e
    yield
    print("[FASTAPI] Shutting down server...")

app = FastAPI(
    title="SkinCare AI Assistant API",
    description="FastAPI Backend for Vision Transformer Skin Lesion Classification",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse

SAMPLE_IMAGES = {
    "bkl": {
        "id": "bkl",
        "label": "Benign Keratosis",
        "filename": "ISIC_0027419.jpg",
        "path": os.path.join("HAM10000_images_part_1", "ISIC_0027419.jpg")
    },
    "nv": {
        "id": "nv",
        "label": "Common Mole",
        "filename": "ISIC_0024698.jpg",
        "path": os.path.join("HAM10000_images_part_1", "ISIC_0024698.jpg")
    },
    "akiec": {
        "id": "akiec",
        "label": "Sun Damage",
        "filename": "ISIC_0029417.jpg",
        "path": os.path.join("HAM10000_images_part_2", "ISIC_0029417.jpg")
    },
    "mel": {
        "id": "mel",
        "label": "Melanoma (Urgent)",
        "filename": "ISIC_0025964.jpg",
        "path": os.path.join("HAM10000_images_part_1", "ISIC_0025964.jpg")
    }
}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "device": "cpu"
    }

@app.get("/api/samples")
def get_sample_list():
    return [
        {
            "id": sample_id,
            "label": info["label"],
            "image_url": f"http://127.0.0.1:8000/api/sample-image/{sample_id}"
        }
        for sample_id, info in SAMPLE_IMAGES.items()
    ]

@app.get("/api/sample-image/{sample_id}")
def get_sample_image(sample_id: str):
    if sample_id not in SAMPLE_IMAGES:
        raise HTTPException(status_code=404, detail="Sample image not found.")
    
    file_path = os.path.abspath(SAMPLE_IMAGES[sample_id]["path"])
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample file missing from disk.")
    
    return FileResponse(file_path, media_type="image/jpeg")

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not a valid image.")
    
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {e}")

    try:
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
        
        # Get id2label mapping from model config
        id2label = model.config.id2label
        
        # Build probability list sorted descending
        breakdown = []
        for i in range(len(probs)):
            label_name_raw = id2label.get(i, id2label.get(str(i), f"class_{i}"))
            meta = DISEASE_METADATA.get(label_name_raw, {
                "code": label_name_raw,
                "name": label_name_raw.replace("_", " ").title(),
                "category": "Unknown",
                "risk_level": "unknown",
                "risk_label": "Unknown Risk",
                "badge_color": "gray",
                "description": "No description available.",
                "action": "Consult a physician.",
                "care": "Keep area clean.",
                "resource_url": "https://www.skincancer.org"
            })
            
            prob_float = float(probs[i].item())
            breakdown.append({
                "class_id": i,
                "raw_label": label_name_raw,
                "code": meta["code"],
                "name": meta["name"],
                "category": meta["category"],
                "probability": prob_float,
                "confidence_percent": round(prob_float * 100, 2),
                "risk_level": meta["risk_level"],
                "risk_label": meta["risk_label"],
                "badge_color": meta["badge_color"],
                "description": meta["description"],
                "action": meta["action"],
                "care": meta["care"],
                "resource_url": meta["resource_url"]
            })
            
        breakdown.sort(key=lambda x: x["probability"], reverse=True)
        primary = breakdown[0]

        return {
            "success": True,
            "filename": file.filename,
            "image_size": list(image.size),
            "primary": primary,
            "breakdown": breakdown,
            "disclaimer": "This tool is for educational and AI assistance purposes only. It is not a substitute for professional medical diagnosis or clinical judgment."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
