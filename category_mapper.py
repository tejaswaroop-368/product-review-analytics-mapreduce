
#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    try:
        review = json.loads(line)

        category = review.get("category")
        rating = review.get("rating")

        if category is None or rating is None:
            continue

        print(f"{category}\t{float(rating)},1")

    except (json.JSONDecodeError, ValueError, TypeError):
        continue
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    fields = line.strip().split(",")

    if len(fields) != 4 or fields[0] == "product_id":
        continue

    product_id, category, rating, review_id = fields

    print(f"{category}\t{rating},1")
