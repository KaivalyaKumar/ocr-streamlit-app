import pytesseract
import platform
import shutil
import cv2
import os
import csv
import re
from PIL import Image
import numpy as np
import streamlit as st

from classify import classify_batch

# Dynamically set tesseract path
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    # Linux / Docker / Mac: use system tesseract if available
    tesseract_path = shutil.which("tesseract")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

# ---------- Preprocess Each Image ----------
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.dilate(thresh, kernel, iterations=1)
    return processed

# ---------- Extract Text Using Tesseract ----------
def extract_text(image_path):
    image = preprocess_image(image_path)
    config = r"--psm 6 -l eng"
    text = pytesseract.image_to_string(image, config=config)
    return text

# ---------- Append Rows to CSV ----------
def append_rows_to_csv(rows, csv_path, write_header=False):
    if not rows:
        return
    fieldnames = rows[0].keys()
    file_exists = os.path.isfile(csv_path)

    with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header and not file_exists:
            writer.writeheader()
        writer.writerows(rows)

# ---------- Main OCR + Classification Pipeline ----------
def batch_process_images(image_folder, output_csv, limit=None):
    """
    Process each image once, extract lines >30 chars, classify in batch, and append to CSV.
    """
    image_files = sorted([
        f for f in os.listdir(image_folder)
        if f.lower().endswith(".png")
    ])

    if limit is not None:
        image_files = image_files[:limit]

    first_image = not os.path.exists(output_csv)

    all_rows = []
    for file in image_files:
        path = os.path.join(image_folder, file)
        print(f"Processing: {file}")
        text = extract_text(path)

        # Keep only non-empty lines with length > 30
        lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 30]
        if not lines:
            continue

        # Classify all lines in batch for this image
        rows = classify_batch(lines, file)
        all_rows.extend(rows)

    # ✅ Write once per batch to avoid duplicates
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        if all_rows:
            fieldnames = all_rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)

    print(f"\n✅ Done! CSV saved to {output_csv}")
