import os
import gradio as gr
from server import app as fastapi_app

# Create a minimal Gradio Blocks UI
with gr.Blocks(title="SkinCare AI Backend API") as demo:
    gr.Markdown("# 🔮 SkinCare AI - Vision Transformer Backend API")
    gr.Markdown("FastAPI backend is active. API Endpoints available at `/api/predict`, `/api/health`, and `/api/samples`.")

# Mount FastAPI app onto Gradio so HuggingFace Space runner detects and serves both
app = gr.mount_gradio_app(app=fastapi_app, blocks=demo, path="/")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
