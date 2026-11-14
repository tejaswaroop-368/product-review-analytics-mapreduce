
#!/usr/bin/env python3
import sys

current_category = None
total_rating = 0.0
total_reviews = 0

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    category, values = line.split("\t")
    rating, count = values.split(",")

    rating = float(rating)
    count = int(count)

    if category == current_category:
        total_rating += rating
        total_reviews += count
    else:
        if current_category is not None:
            average = total_rating / total_reviews
            print(f"{current_category}\t{total_reviews}\t{average:.2f}")

        current_category = category
        total_rating = rating
        total_reviews = count

if current_category is not None:
    average = total_rating / total_reviews
    print(f"{current_category}\t{total_reviews}\t{average:.2f}")
#!/usr/bin/env python3
import sys

current_category = None
total_rating = 0
total_reviews = 0

for line in sys.stdin:
    category, values = line.strip().split("\t")
    rating, count = values.split(",")

    if category == current_category:
        total_rating += int(rating)
        total_reviews += int(count)
    else:
        if current_category is not None:
            print(f"{current_category}\t{total_reviews}\t{total_rating / total_reviews:.2f}")

        current_category = category
        total_rating = int(rating)
        total_reviews = int(count)

if current_category is not None:
    print(f"{current_category}\t{total_reviews}\t{total_rating / total_reviews:.2f}")
