import streamlit as st
import os
import time
import pandas as pd
from config_manager import load_config, save_config
from ocr_reader import batch_process_images
from classify import get_classifier
import hashlib

# Page setup
st.set_page_config(page_title="OCR Image Classifier", layout="centered")
st.title("📃 OCR Image Processor")

# Session state init
if "job_running" not in st.session_state:
    st.session_state.job_running = False
if "output_df" not in st.session_state:
    st.session_state.output_df = None

# Load config
config = load_config()

# Input UI — disable during job
st.markdown("### 📂 Image Folder Path")
image_folder = st.text_input("Folder path", value=config["image_folder"], disabled=st.session_state.job_running)

st.markdown("### 📄 Output CSV File")
output_csv = st.text_input("Output file path", value=config["output_csv"], disabled=st.session_state.job_running)

if st.button("Save Config", disabled=st.session_state.job_running):
    save_config(image_folder, output_csv)
    st.success("Configuration saved. Monitoring for changes...")

# Optional utility (can be used for future file change detection)
@st.cache_resource
def file_hash(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()

# Run job logic
def run_job():
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(".png")]
    total = len(images)

    with st.spinner("🔍 Loading model..."):
        get_classifier()

    progress_bar = st.empty()
    status_text = st.empty()

    # Phase 1: simulate scanning images
    for i, f in enumerate(images):
        status_text.text(f"Scanning image {i+1}/{total}: {f}")
        progress_bar.progress((i + 1) / total)
        time.sleep(0.05)

    # Phase 2: real processing with spinner
    status_text.text("Processing images in batch, please wait...")
    with st.spinner("Running OCR and classification..."):
        batch_process_images(image_folder, output_csv)

    progress_bar.empty()
    status_text.empty()

    df = pd.read_csv(output_csv)
    st.session_state.output_df = df

    st.success("✅ Done! Final CSV ready.")
    st.dataframe(df)

    st.session_state.job_running = False
    st.rerun()  # Refresh UI to re-enable controls and show output

# Start job — disable all buttons and fields during job
start_button = st.button("🚀 Start Job", disabled=st.session_state.job_running)

if start_button and not st.session_state.job_running:
    st.session_state.job_running = True
    st.rerun()

# Run job if flagged
if st.session_state.job_running:
    run_job()

# Show last output
elif st.session_state.output_df is not None:
    st.markdown("### ✅ Final CSV")
    st.dataframe(st.session_state.output_df)
