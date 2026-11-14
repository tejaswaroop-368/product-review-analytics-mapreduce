import gzip
import json
import os
from pathlib import Path

RAW_DIR = Path("dataset/raw")
OUTPUT_DIR = Path("dataset/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "reviews_us_Electronics.json.gz": "Electronics",
    "reviews_us_Home_and_Kitchen.json.gz": "Home & Kitchen",
    "reviews_us_Office_Products.json.gz": "Office Products"
}

CHUNK_SIZE = 100000

for filename, category in FILES.items():

    input_path = RAW_DIR / filename

    if not input_path.exists():
        raise FileNotFoundError(input_path)

    print(f"\nProcessing {category}...")

    count = 0
    chunk_number = 1
    output_file = None

    with gzip.open(input_path, "rt", encoding="utf-8") as source:

        for line in source:

            if not line.strip():
                continue

            records = json.loads(line)

            if isinstance(records, dict):
                records = [records]

            for review in records:

                clean_record = {
                    "product_id": review.get("asin", ""),
                    "rating": review.get("overall"),
                    "review_text": review.get("reviewText", ""),
                    "summary": review.get("summary", ""),
                    "review_date": review.get("cleanReviewTime", ""),
                    "category": category
                }

                if not clean_record["product_id"]:
                    continue

                if output_file is None or count % CHUNK_SIZE == 0:

                    if output_file:
                        output_file.close()

                    output_name = (
                        f"{category.lower().replace(' ', '_').replace('&', 'and')}"
                        f"_part_{chunk_number:03d}.jsonl"
                    )

                    output_file = open(
                        OUTPUT_DIR / output_name,
                        "w",
                        encoding="utf-8"
                    )

                    chunk_number += 1

                output_file.write(
                    json.dumps(clean_record, ensure_ascii=False) + "\n"
                )

                count += 1

                if count % 500000 == 0:
                    print(f"Processed {count:,} reviews")

    if output_file:
        output_file.close()

    print(f"Completed {category}: {count:,} reviews")

print("\nDATA PREPARATION COMPLETE")
