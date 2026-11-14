#!/usr/bin/env python3
import sys

current_product = None
total_reviews = 0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    product_id, count = line.split("\t")
    count = int(count)

    if product_id == current_product:
        total_reviews += count
    else:
        if current_product is not None:
            print(f"{current_product}\t{total_reviews}")

        current_product = product_id
        total_reviews = count

if current_product is not None:
    print(f"{current_product}\t{total_reviews}")
