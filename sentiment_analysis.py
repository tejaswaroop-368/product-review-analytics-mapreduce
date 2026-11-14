
import glob
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, rand, length
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import NaiveBayes, LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Start Spark using local CPU cores
spark = (
    SparkSession.builder
    .appName("ProductReviewSentimentAnalysis")
    .master("local[4]")
    .config("spark.driver.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Read all processed JSONL review files
data = spark.read.json("dataset/processed/*.jsonl")

# Convert ratings into sentiment labels:
# 1-2 = Negative, 3 = Neutral, 4-5 = Positive
data = data.select("review_text", "rating").dropna()
data = data.withColumn(
    "sentiment",
    when(col("rating") <= 2, "negative")
    .when(col("rating") == 3, "neutral")
    .otherwise("positive")
)

# Remove empty or very short reviews
data = data.filter(length(col("review_text")) >= 10)

# Limit the dataset to 120,000 reviews for ML training
# Hadoop MapReduce analytics still uses the full dataset
data = data.orderBy(rand(seed=42)).limit(120000)

print("\nSENTIMENT DISTRIBUTION")
data.groupBy("sentiment").count().show()

# Convert text into numerical TF-IDF features
tokenizer = RegexTokenizer(
    inputCol="review_text",
    outputCol="words",
    pattern="\\W+",
    minTokenLength=2
)

remover = StopWordsRemover(
    inputCol="words",
    outputCol="filtered_words"
)

hashing = HashingTF(
    inputCol="filtered_words",
    outputCol="raw_features",
    numFeatures=1 << 16
)

idf = IDF(
    inputCol="raw_features",
    outputCol="features"
)

label_indexer = StringIndexer(
    inputCol="sentiment",
    outputCol="label",
    stringOrderType="alphabetAsc"
)

# Split into training and testing data
train, test = data.randomSplit([0.8, 0.2], seed=42)

# Models to compare
models = {
    "Multinomial Naive Bayes": NaiveBayes(
        labelCol="label",
        featuresCol="features",
        modelType="multinomial"
    ),
    "Logistic Regression": LogisticRegression(
        labelCol="label",
        featuresCol="features",
        maxIter=30,
        regParam=0.01
    )
}

accuracy_evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="accuracy"
)

f1_evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="f1"
)

results = []

for model_name, classifier in models.items():
    print("\nTraining:", model_name)

    pipeline = Pipeline(stages=[
        tokenizer,
        remover,
        hashing,
        idf,
        label_indexer,
        classifier
    ])

    fitted_model = pipeline.fit(train)
    predictions = fitted_model.transform(test)

    accuracy = accuracy_evaluator.evaluate(predictions)
    f1 = f1_evaluator.evaluate(predictions)

    results.append((model_name, accuracy, f1))

    print("Accuracy:", round(accuracy, 4))
    print("Weighted F1:", round(f1, 4))

print("\nFINAL MODEL COMPARISON")
for name, accuracy, f1 in results:
    print(
        f"{name}: Accuracy={accuracy:.4f}, "
        f"Weighted F1={f1:.4f}"
    )

best_model = max(results, key=lambda x: x[2])
print("\nBEST MODEL BASED ON WEIGHTED F1:", best_model[0])

spark.stop()
