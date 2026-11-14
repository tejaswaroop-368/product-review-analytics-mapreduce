import json
import glob
from collections import defaultdict

category_stats = defaultdict(lambda: [0, 0.0])
product_counts = defaultdict(int)

files = glob.glob("dataset/processed/*.jsonl")
total = 0
bad = 0

print("Processing dataset...")

for path in files:
    print("Reading:", path)

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
                category = r.get("category")
                rating = float(r.get("rating"))
                product = r.get("product_id")

                if not category or not product or not 1 <= rating <= 5:
                    continue

                category_stats[category][0] += 1
                category_stats[category][1] += rating
                product_counts[product] += 1
                total += 1

            except (ValueError, TypeError, json.JSONDecodeError):
                bad += 1

print("\nTOTAL VALID REVIEWS:", total)
print("INVALID RECORDS:", bad)

print("\nCATEGORY ANALYSIS")
with open("category_results.txt", "w") as out:
    out.write("CATEGORY\tREVIEW_COUNT\tAVERAGE_RATING\n")
    for category, (count, rating_sum) in sorted(category_stats.items()):
        average = rating_sum / count
        result = f"{category}\t{count}\t{average:.2f}"
        print(result)
        out.write(result + "\n")

print("\nTOP 20 MOST REVIEWED PRODUCTS")
with open("top_products.txt", "w") as out:
    out.write("PRODUCT_ID\tREVIEW_COUNT\n")
    for product, count in sorted(
        product_counts.items(), key=lambda x: x[1], reverse=True
    )[:20]:
        result = f"{product}\t{count}"
        print(result)
        out.write(result + "\n")

print("\nResults saved to category_results.txt and top_products.txt")
