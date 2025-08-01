<img width="1111" height="783" alt="ocr" src="https://github.com/user-attachments/assets/027010dc-7c25-40b5-9a6c-8b456e8b2f04" />


OCR Streamlit App
=================

Extract structured project information from construction project screenshots using:

- Tesseract OCR for text extraction
- OpenCV for image preprocessing
- Hugging Face Zero-Shot Classification for labeling
- Streamlit for an interactive UI

------------------------------------------------------------
🚀 Features
------------------------------------------------------------
- Batch OCR and classification for .png images
- GPU and CPU support (Any CUDA GPU)
- Configurable input/output paths via config.json
- Streamlit UI with progress visualization
- Single CSV output per run (final_output.csv)
- Docker-ready for cross-platform usage

------------------------------------------------------------
📦 Local Setup (Python)
------------------------------------------------------------
1. Install Python and dependencies:

    git clone https://github.com/yourusername/ocr-streamlit-app.git
    cd ocr-streamlit-app

    # Optional: create virtual environment
    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate

    pip install --upgrade pip
    pip install -r requirements.txt

2. Configure Paths:

Edit config.json:

    {
        "image_folder": "images/sample",
        "output_csv": "output/final_output.csv"
    }

- Drop input .png images into the images/ folder
- Output CSV will be created in output/

3. Run Streamlit App:

    streamlit run app/index.py

Then open: http://localhost:8501


------------------------------------------------------------
Note: Edit config.json for docker runs as below:

    {
        "image_folder": "/app/images",
        "output_csv": "/app/output/final_output.csv"
    }
------------------------------------------------------------

------------------------------------------------------------
🐳 Docker Usage (CPU Mode)
------------------------------------------------------------

1. Build the Docker image:

    docker build -t ocr-streamlit-app .

2. Run the container:

    docker run -p 8501:8501 ocr-streamlit-app

Then open http://localhost:8501 in your browser.

------------------------------------------------------------
⚡ Docker GPU Mode (Recommended)
------------------------------------------------------------
Supports any NVIDIA GPU with CUDA.

1. Install Prerequisites:

- Docker: https://www.docker.com/products/docker-desktop
- NVIDIA Container Toolkit: 
  https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

Verify GPU access:

    docker run --rm --gpus all nvidia/cuda:12.1.1-base nvidia-smi

2. Run with GPU via docker-compose:

    docker-compose up --build

- Mounts local images/ and output/ folders
- Starts Streamlit app on port 8501

Access the app at: http://localhost:8501

Drop .png images into ./images on your host → processed CSV appears in ./output.

------------------------------------------------------------
📊 Output Format
------------------------------------------------------------
The app generates output/final_output.csv with columns:

- Project Name – Extracted from image minus metadata
- City – Predicted city label
- Status – Predicted construction status
- Category – Predicted project category
- Source Image – Original filename

------------------------------------------------------------
📄 License
------------------------------------------------------------
This project is released under the MIT License.
Free to use, modify, and distribute.

------------------------------------------------------------
💡 Notes for Contributors
------------------------------------------------------------
- Streamlit session state is used to manage job status and progress.
- Batch processing is optimized for GPU using Hugging Face pipeline.
- For large datasets (400+ images), GPU mode is 2–5× faster than CPU mode.
- Pull requests and improvements are welcome!

