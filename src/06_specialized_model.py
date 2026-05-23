"""Classify the reviews with a small Hugging Face model. No API, runs on your laptop.

Demo 3 did this with an LLM API. For a simple labeling task like sentiment, you
often don't need a big model and you don't need to pay per call. A small
specialized model from Hugging Face downloads once and runs locally, for free.
"""

import csv
from transformers import pipeline

# downloads a tiny sentiment model the first time, then caches it locally
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
)

with open("data/reviews_messy.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        text = row.get("review_text", "").strip()
        if not text:
            continue
        result = classifier(text)[0]
        label = result["label"].lower()          # POSITIVE / NEGATIVE
        score = round(result["score"], 2)        # confidence 0-1
        print(f"[{label:>8}  {score}]  {text[:70]}")
