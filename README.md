# Product Review Analytics using Hadoop MapReduce and Spark MLlib

## Project Overview
This project analyzes large-scale e-commerce product reviews using Apache Hadoop MapReduce and Apache Spark MLlib.

The system processes product reviews to calculate average product ratings, identify the most-reviewed products, analyze category-wise ratings, and classify customer review sentiment.

## Dataset
- Name: XMarket Cross-Market Product Reviews
- Source: XMarket / UMass CIIR
- Website: https://xmrec.github.io/
- Categories: Electronics, Home & Kitchen, Office Products
- Total processed reviews: 8,541,956

## Technologies Used
- Python
- Apache Hadoop 3.5.0
- Hadoop MapReduce
- Hadoop Streaming
- Apache Spark 4.3.0
- Spark MLlib
- TF-IDF
- Linux

## Hadoop MapReduce Analytics

1. Product-wise average rating and review count.
2. Category-wise review count and average rating.
3. Top 20 most-reviewed products.

## Spark MLlib Sentiment Classification

Review ratings are mapped into three sentiment classes:
- 1–2 stars: Negative
- 3 stars: Neutral
- 4–5 stars: Positive

Text processing:
- Regex Tokenizer
- Stop Words Removal
- HashingTF
- IDF (TF-IDF)

Models compared:
- Multinomial Naive Bayes
- Logistic Regression

Training sample: 120,000 reviews  
Train-test split: 80:20

### Model Results

| Model | Accuracy | Weighted F1 |
|---|---:|---:|
| Multinomial Naive Bayes | 76.16% | 77.96% |
| Logistic Regression | 83.31% | 81.93% |

Best performing model: Logistic Regression.

## Project Results
The Hadoop analytics processed 8,541,956 reviews across three product categories.

Category-wise results:

| Category | Review Count | Average Rating |
|---|---:|---:|
| Electronics | 4,169,476 | 4.07 |
| Home & Kitchen | 1,687,112 | 4.14 |
| Office Products | 2,685,368 | 4.22 |

The `results/` directory contains the generated analytics outputs and ML model comparison.

## Repository Structure

- `mapper.py`, `reducer.py`: Product average rating MapReduce
- `category_mapper.py`, `category_reducer.py`: Category analytics
- `top_products_mapper.py`, `top_products_reducer.py`: Product review counts
- `sentiment_analysis.py`: Spark MLlib classification
- `scripts/`: Dataset preparation scripts
- `results/`: Generated analysis results

## Note
The raw and processed dataset files are not included in this repository because of their size. Download the dataset from the official XMarket source before running the project.
