"""Take messy customer reviews and turn each one into clean, structured data."""

import os
import csv
import json
import logging
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

os.makedirs("output", exist_ok=True)
logging.basicConfig(
    filename="output/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)


# this is the exact shape we want back
class Review(BaseModel):
    product: str
    sentiment: str          # positive, negative, or neutral
    rating_guess: int       # 1 to 5
    main_issue: str
    is_actionable: bool


SYSTEM = (
    "You extract structured data from messy customer reviews. "
    "Reply with ONLY a JSON object, no markdown, no explanation. Keys: "
    "product (string), sentiment (positive/negative/neutral), "
    "rating_guess (integer 1-5), main_issue (string), is_actionable (boolean)."
)

# a couple of examples first, so the model knows the style we want
# (this is "few-shot" prompting. Zero-shot is just asking with no examples.)
FEW_SHOT_EXAMPLES = [
    {"role": "user", "content": "Review: love it!! best tool ive used for kafka stuff"},
    {"role": "assistant", "content": '{"product": "StreamSync", "sentiment": "positive", "rating_guess": 5, "main_issue": "none", "is_actionable": false}'},
    {"role": "user", "content": "Review: the new update broke everything pls fix asap!!!"},
    {"role": "assistant", "content": '{"product": "QueryBuilder", "sentiment": "negative", "rating_guess": 1, "main_issue": "update broke the product", "is_actionable": true}'},
]


def structure_one(product, raw_text):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        system=SYSTEM,
        messages=[
            *FEW_SHOT_EXAMPLES,
            {"role": "user", "content": f"Product: {product}\nReview: {raw_text}"},
        ],
    )
    # the model replies with text; Pydantic checks it matches the shape we want
    return Review.model_validate_json(response.content[0].text)


def main():
    results = []
    with open("data/reviews_messy.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            raw = row.get("review_text", "").strip()
            if not raw:
                logging.info("Skipped a row with no review text")
                continue
            product = row.get("product", "").strip() or "unknown"
            try:
                review = structure_one(product, raw)
                results.append(review.model_dump())
                logging.info(f"Structured a review for: {review.product}")
            except Exception as e:
                logging.error(f"Failed on a row: {e}")

    with open("output/reviews_structured.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logging.info(f"Done. Wrote {len(results)} structured reviews.")
    print(f"Wrote {len(results)} structured reviews to output/reviews_structured.json")


if __name__ == "__main__":
    main()
