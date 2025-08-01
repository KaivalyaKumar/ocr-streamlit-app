import streamlit as st
from transformers import pipeline
import torch
import re

# Predefined labels
cities = ["Dubai", "Fujairah", "Abu Dhabi", "Sharjah", "Ajman", "Umm Al Quwain", "Ras Al Khaimah"]
statuses = ["Under Construction", "Completed", "Proposed", "Cancelled"]
categories = [
    "Midstream: Oil & Gas Transfer",
    "Marine",
    "Power Station",
    "District Cooling",
    "Warehouse",
    "Office",
    "Manufacturing / Processing Facility",
    "Plant"
]

@st.cache_resource
def get_classifier():
    device = 0 if torch.cuda.is_available() else -1
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

# ---------- Batched classification ----------
def classify_batch(texts, image_name, classifier=None):
    """
    Classify a list of texts for city, status, and category in batch mode.
    Returns a list of dicts, one per text line.
    """
    if classifier is None:
        classifier = get_classifier()
    if not texts:
        return []

    # Run pipeline in batch for each label set
    city_preds = classifier(texts, cities, multi_label=False)
    if isinstance(city_preds, dict):
        city_preds = [city_preds]

    status_preds = classifier(texts, statuses, multi_label=False)
    if isinstance(status_preds, dict):
        status_preds = [status_preds]

    category_preds = classifier(texts, categories, multi_label=True)
    if isinstance(category_preds, dict):
        category_preds = [category_preds]

    results = []
    for i, text in enumerate(texts):
        city = city_preds[i]["labels"][0]
        status = status_preds[i]["labels"][0]
        category = category_preds[i]["labels"][0]

        # Remove trailing metadata like "<city> <status> United Arab Emirates <category>"
        metadata = f"{city} {status} United Arab Emirates {category}"
        pattern = re.compile(re.escape(metadata) + r"[\s\-,:]*$", re.IGNORECASE)
        project_name = pattern.sub("", text).strip().rstrip("-:,").strip()

        results.append({
            "Project Name": project_name,
            "City": city,
            "Status": status,
            "Category": category,
            "Source Image": image_name
        })

    return results
