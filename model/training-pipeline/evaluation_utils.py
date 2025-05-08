from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, expr
from pyspark.sql.types import StringType, FloatType
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def evaluate_model(cvModel, test_df, predictions_path):
    """
    Evaluate the model on test data and save predictions to CSV.
    
    Args:
        cvModel: Trained CrossValidatorModel
        test_df: Test DataFrame
        predictions_path: Path to save the predictions CSV
    """

    # Determine if the input is a CrossValidatorModel or PipelineModel
    if isinstance(cvModel, CrossValidatorModel):
        bestModel = cvModel.bestModel
    elif isinstance(cvModel, PipelineModel):
        bestModel = cvModel
    else:
        raise ValueError("Input model must be a CrossValidatorModel or PipelineModel")
    
    # bestModel = cvModel.bestModel
    predictions = bestModel.transform(test_df)
    
    # Get genre labels from StringIndexer
    indexer_model = bestModel.stages[4]  # StringIndexer is the 5th stage
    genre_labels = indexer_model.labels
    
    # UDF to map prediction index to genre
    def index_to_genre(index):
        return genre_labels[int(index)]
    index_to_genre_udf = udf(index_to_genre, StringType())
    
    # UDF to extract the predicted probability
    def get_predicted_prob(prob_vector, prediction):
        return float(prob_vector[int(prediction)])
    get_predicted_prob_udf = udf(get_predicted_prob, FloatType())
    
    # UDF to convert probability vector to string
    def vector_to_string(vector):
        return ",".join(map(str, vector.toArray()))
    vector_to_string_udf = udf(vector_to_string, StringType())
    
    # Add predicted genre, predicted probability, and probability string columns
    predictions = predictions.withColumn("predicted_genre", index_to_genre_udf(col("prediction")))
    predictions = predictions.withColumn("predicted_prob", get_predicted_prob_udf(col("probability"), col("prediction")))
    predictions = predictions.withColumn("probability_str", vector_to_string_udf(col("probability")))
    
    # Select relevant columns for saving, excluding the original probability vector
    predictions_select = predictions.select(
        "genre", "lyrics", "label", "prediction", "predicted_genre", "predicted_prob", "probability_str"
    )
    
    # Save predictions to CSV
    predictions_select.write.csv(predictions_path, header=True, mode="overwrite")
    
    # Compute and display overall accuracy
    evaluator = MulticlassClassificationEvaluator(
        labelCol="label", 
        predictionCol="prediction", 
        metricName="accuracy"
    )
    accuracy = evaluator.evaluate(predictions)
    print(f"Test Accuracy: {accuracy}")
    
    # Compute and display accuracy breakdown by genre
    accuracy_df = predictions.groupBy("genre") \
        .agg(
            expr("sum(cast(prediction = label as int)) as correct"),
            expr("count(*) as total")
        ) \
        .withColumn("accuracy", col("correct") / col("total")) \
        .orderBy("genre")
    print("Accuracy breakdown by genre:")
    accuracy_df.show()

def display_predictions(predictions_path, num_rows=10):
    """
    Read saved predictions from CSV and display sample predictions with probabilities.
    
    Args:
        predictions_path: Path to the saved predictions CSV
        num_rows: Number of rows to display
    """
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.csv(predictions_path, header=True)
    print(f"Displaying top {num_rows} predictions:")
    df.select("genre", "predicted_genre", "predicted_prob", "probability_str").show(num_rows)