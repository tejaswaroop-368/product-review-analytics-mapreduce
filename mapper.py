#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    if line.startswith("product_id"):
        continue

    fields = line.split(",")

    if len(fields) != 4:
        continue

    product_id, category, rating, review_id = fields

    print(f"{product_id}\t{rating},1")
