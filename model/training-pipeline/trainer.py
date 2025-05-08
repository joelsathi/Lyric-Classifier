from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
import argparse
from data_utils import load_and_clean_data
from pipeline_utils import build_pipeline
from training_utils import train_model
from evaluation_utils import evaluate_model, display_predictions
from pyspark.sql.functions import col

def main():
    parser = argparse.ArgumentParser(description="Music Genre Prediction with Spark ML")
    parser.add_argument("--input_file", default="../data/Merged_dataset.csv", help="Path to the input CSV file")
    parser.add_argument("--model_path", default="genre_prediction_model_2", help="Path to save the best model")
    parser.add_argument("--predictions_path", default="predictions_csv/predictions_2.csv", help="Path to save the predictions")
    args = parser.parse_args()

    # Initialize Spark Session
    spark = SparkSession.builder.appName("Music Genre Prediction").getOrCreate()

    print("Loading and cleaning data...")
    df = load_and_clean_data(spark, args.input_file)

    # Display dataset statistics
    print("Number of records:", df.count())
    print("Unique genres:", df.select("genre").distinct().count())
    df.groupBy("genre").count().orderBy(col("count").desc()).show(10)

    # Split data into training and test sets
    print("Splitting data into train and test sets...")
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    # Build the pipeline
    print("Building pipeline...")
    pipeline = build_pipeline()

    # Train the model
    print("Training the model with cross-validation...")
    cvModel = train_model(pipeline, train_df)

    # Load the saved model
    # print("Loading saved model...")
    # cvModel = PipelineModel.load(args.model_path)

    # Save the best model immediately after training
    print("Saving best model...")
    bestModel = cvModel.bestModel
    bestModel.write().overwrite().save(args.model_path)
    print(f"Best model saved to {args.model_path}")

    # Evaluate the model and save predictions
    print("Evaluating on test data...")
    evaluate_model(cvModel, test_df, args.predictions_path)
    print(f"Predictions saved to {args.predictions_path}")

    # Display sample predictions
    print("Displaying sample predictions...")
    display_predictions(args.predictions_path)

if __name__ == "__main__":
    main()