FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files and model weights
COPY server.py config.json preprocessor_config.json ./
COPY model.safetensors ./

# Expose port 7860 (default port for Hugging Face Spaces Docker)
EXPOSE 7860

# Run uvicorn on port 7860
CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
