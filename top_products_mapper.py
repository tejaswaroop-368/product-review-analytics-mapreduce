
#!/usr/bin/env python3
import sys
import json

for line in sys.stdin:
    try:
        review = json.loads(line)
        product_id = review.get("product_id")

        if product_id:
            print(f"{product_id}\t1")

    except (json.JSONDecodeError, TypeError):
        continue
