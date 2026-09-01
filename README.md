---
license: apache-2.0
---

# 🔮 SkinCare AI Assistant - Vision Transformer Skin Lesion Classifier

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)

An advanced **AI-powered clinical support web application** that classifies skin lesion photographs into **7 diagnostic disease categories** using Google's **Vision Transformer (ViT-16)** fine-tuned on the **HAM10000 dataset**.

The application features a full-stack architecture combining a **FastAPI PyTorch backend** with a **React + Vite glassmorphism web interface** offering dark/light theme switching, drag-and-drop uploader, real-time laser scanning animations, severity risk rating, clinical action recommendations, local scan history, and dermatologist locator integration.

---

## 🌟 Features

- **🤖 High-Accuracy Vision Transformer (ViT-16)**: Achieves **96.95% validation accuracy** across 7 skin disease categories.
- **⚡ Fast REST API Backend**: Built with FastAPI, PyTorch, and HuggingFace Transformers (`model.safetensors`).
- **🎨 Dual Theme UI (Light & Dark Modes)**: Ultra-sleek glassmorphism design system supporting theme toggling with stored preferences.
- **📤 Interactive Upload & Real-Time Scanning**: Drag & drop image upload zone with laser scanning animation during model inference.
- **📊 7-Class Confidence Distribution**: Color-coded risk indicators (`🚨 URGENT` for Melanoma, `⚠️ Precancerous` for Actinic Keratosis, `🟢 Benign` for Common Moles).
- **💡 Clinical Recommendations & Care Plans**: Provides actionable next steps, dermatology links, and direct 1-click Google Maps search for nearby dermatologists.
- **📜 Scan History Drawer**: Automatically saves previous scans locally in `localStorage` for review and side-by-side comparison.
- **🧪 Real Dataset Test Samples**: Built-in test cards featuring real HAM10000 skin lesion photographs for instant test scans without uploading files.

---

## 📁 Project Structure

```
Skin_Model/
├── server.py                   # FastAPI backend server (PyTorch ViT inference API on port 8000)
├── model.safetensors           # Fine-tuned Vision Transformer model weights (343 MB)
├── config.json                 # HuggingFace ViT architecture & id2label mapping
├── preprocessor_config.json    # Image preprocessing parameters (224x224, normalization)
├── requirements.txt            # Python dependencies
├── train_model.py              # Script to train/fine-tune PyTorch image classifier
├── train_val.py                # Train/Validation dataset splitting script
├── merge.py                    # Dataset folder merging utility
├── summary.py                  # Dataset statistical summary helper
├── README.md                   # Project documentation
│
└── frontend/                   # React Web Application (Vite dev server on port 5173)
    ├── vite.config.js          # Vite configuration with API proxy to FastAPI
    ├── package.json            # Node.js dependencies & scripts
    ├── index.html              # HTML entry point
    └── src/
        ├── main.jsx            # React root component initialization
        ├── App.jsx             # Main application layout, theme state & API wiring
        ├── index.css           # Glassmorphism & Light/Dark mode CSS design tokens
        └── components/
            ├── ImageUploader.jsx    # Drag-and-drop uploader + real sample test cards
            ├── ScanAnimation.jsx    # Animated laser scanner overlay
            ├── ResultsDashboard.jsx # Primary diagnosis, confidence bars & care tabs
            └── ScanHistory.jsx      # Slide-out scan history drawer
```

---

## 🔬 Classification Categories

The model classifies skin lesions into 7 distinct medical categories:

| Code | Disease Name | Category | Risk Level |
| :--- | :--- | :--- | :--- |
| `mel` | **Melanoma** | High-Risk Malignancy | 🚨 **URGENT** |
| `bcc` | **Basal Cell Carcinoma** | Skin Cancer | 🟡 Moderate Risk |
| `akiec` | **Actinic Keratosis** | Precancerous Lesion | ⚠️ Precancerous |
| `bkl` | **Benign Keratosis** | Benign Growth | 🟢 Benign |
| `nv` | **Common Mole (Nevus)** | Pigmented Lesion | 🟢 Benign |
| `df` | **Dermatofibroma** | Benign Nodule | 🟢 Benign |
| `vasc` | **Vascular Lesion** | Vascular Overgrowth | 🟢 Benign |

---

## 🚀 Getting Started & Setup

### Prerequisites

- **Python**: `3.10` or higher
- **Node.js**: `v18.0` or higher
- **NPM**: `v9.0` or higher

---

### 1. Clone the Repository

```bash
git clone https://github.com/karthick151205/Skin_Disease_Prediction.git
cd Skin_Disease_Prediction
```

---

### 2. Set Up the Python Backend

Create a virtual environment and install the required dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Set Up the React Frontend

Navigate to the `frontend` directory and install Node.js packages:

```bash
cd frontend
npm install
cd ..
```

---

## 🏃 Running the Application

Run the backend API server and frontend development server in two separate terminal windows:

#### Terminal 1: Launch FastAPI Backend
```bash
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```
*(The backend loads `model.safetensors` and serves API endpoints at `http://127.0.0.1:8000`)*

#### Terminal 2: Launch React Frontend
```bash
cd frontend
npm run dev
```
*(Open your browser at **`http://localhost:5173`**)*

---

## 📡 API Documentation

### `GET /api/health`
Checks backend status and model loading state.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu"
}
```

### `POST /api/predict`
Accepts a skin lesion image file (`multipart/form-data`) and returns AI predictions.

**Parameters**: `file` (UploadFile)

**Response**:
```json
{
  "success": true,
  "filename": "lesion.jpg",
  "primary": {
    "code": "nv",
    "name": "Common Mole (Nevus)",
    "category": "Pigmented Lesion",
    "confidence_percent": 99.92,
    "risk_level": "low",
    "risk_label": "Benign (Normal Mole)",
    "badge_color": "green"
  },
  "breakdown": [ ... ],
  "disclaimer": "This tool is for educational purposes only."
}
```

### `GET /api/samples`
Returns available real dataset sample test cases.

### `GET /api/sample-image/{sample_id}`
Serves actual HAM10000 dataset JPEG sample images (`bkl`, `nv`, `akiec`, `mel`).

---

## 📊 Training Performance & Results

Fine-tuned Vision Transformer (ViT-16) training progress over 5 epochs on HAM10000 dataset:

| Epoch | Train Loss | Train Accuracy | Validation Loss | Validation Accuracy |
| :---: | :---: | :---: | :---: | :---: |
| **1** | 0.7168 | 75.86% | 0.4994 | 83.55% |
| **2** | 0.4550 | 84.66% | 0.3237 | 89.73% |
| **3** | 0.2959 | 90.28% | 0.1790 | 95.30% |
| **4** | 0.1595 | 94.82% | 0.1498 | 95.55% |
| **5** | **0.1208** | **96.14%** | **0.1000** | **96.95%** |

---

## 🌐 Web Hosting & Deployment Guide

To deploy this project to the web for public access, host the **FastAPI Backend** and **React Frontend** using free / low-cost cloud platforms.

### Step 1: Host the FastAPI Backend (Render / Hugging Face Spaces / Railway)

#### Option A: Deploy on Render.com (Free Web Service)
1. Push your repository to GitHub.
2. Sign up at [Render.com](https://render.com) and click **New > Web Service**.
3. Connect your GitHub repository.
4. Set the following parameters:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Deploy service. Once finished, copy your public backend URL (e.g. `https://skincare-api.onrender.com`).

#### Option B: Deploy on Hugging Face Spaces (Free CPU/GPU Docker/FastAPI)
1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces).
2. Choose **Docker** or **FastAPI** template.
3. Upload `server.py`, `model.safetensors`, `config.json`, `preprocessor_config.json`, and `requirements.txt`.
4. Copy the public space endpoint URL.

---

### Step 2: Host the React Frontend (Vercel / Netlify / Render)

#### Deploy on Vercel (Recommended - Free & Fast)
1. Sign up at [Vercel.com](https://vercel.com) and click **Add New > Project**.
2. Import your GitHub repository.
3. Set the **Root Directory** to `frontend`.
4. Under **Environment Variables**, add:
   - `VITE_API_URL`: `https://your-backend-url.onrender.com` (replace with your deployed FastAPI backend URL from Step 1).
5. Click **Deploy**. Vercel will build your React app and provide a live URL (e.g. `https://skincare-ai.vercel.app`).

---

## 📄 License & Medical Disclaimer

### License
This project is licensed under the [Apache License 2.0](LICENSE).

### ⚠️ Medical Disclaimer
> **IMPORTANT**: This application is an artificial intelligence prototype developed for educational and decision-support demonstration purposes only. It is **not** a certified medical diagnostic device and should **never** replace professional medical advice, clinical examination, or biopsy diagnosis by a qualified dermatologist.
