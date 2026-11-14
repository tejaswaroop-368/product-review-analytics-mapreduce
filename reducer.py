#!/usr/bin/env python3
import sys

current_product = None
total_rating = 0
total_reviews = 0

for line in sys.stdin:
    product_id, values = line.strip().split("\t")
    rating, count = values.split(",")

    if current_product == product_id:
        total_rating += int(rating)
        total_reviews += int(count)
    else:
        if current_product is not None:
            average = total_rating / total_reviews
            print(
                f"{current_product}\t"
                f"{total_reviews}\t{average:.2f}"
            )

        current_product = product_id
        total_rating = int(rating)
        total_reviews = int(count)

if current_product is not None:
    average = total_rating / total_reviews
    print(
        f"{current_product}\t"
        f"{total_reviews}\t{average:.2f}"
    )
