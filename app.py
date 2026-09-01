import gradio as gr
from server import app as fastapi_app

# Mount FastAPI backend onto Gradio Blocks for HuggingFace Spaces
demo = gr.Blocks(title="SkinCare AI API")

with demo:
    gr.Markdown("# 🔮 SkinCare AI - Vision Transformer Backend API")
    gr.Markdown("FastAPI Endpoints active at `/api/predict` and `/api/health`.")

# Combine Gradio with FastAPI app
app = gr.mount_gradio_app(app=fastapi_app, blocks=demo, path="/")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
