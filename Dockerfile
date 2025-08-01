# --------------------------
# 1. Base image with NVIDIA CUDA
# --------------------------
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# --------------------------
# 2. System dependencies
# --------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-opencv \
    tesseract-ocr libtesseract-dev \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# --------------------------
# 3. Set working directory
# --------------------------
WORKDIR /app

# --------------------------
# 4. Copy project files
# --------------------------
COPY . /app

# --------------------------
# 5. Install Python dependencies
# --------------------------
RUN pip3 install --upgrade pip
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install -r requirements.txt

# --------------------------
# 6. Streamlit environment setup
# --------------------------
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ENABLEXsrfProtection=false

# --------------------------
# 7. Expose Streamlit port
# --------------------------
EXPOSE 8501

# --------------------------
# 8. Launch the app
# --------------------------
CMD ["streamlit", "run", "app/index.py"]
