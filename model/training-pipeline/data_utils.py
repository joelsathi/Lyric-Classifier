from pyspark.sql.functions import col, lower, trim, regexp_replace

def load_and_clean_data(spark, file_path):
    """
    Load and clean the music dataset from a CSV file.
    
    Args:
        spark: SparkSession object
        file_path: Path to the input CSV file
    
    Returns:
        DataFrame with cleaned 'genre' and 'lyrics' columns
    """
    df = spark.read.csv(file_path, inferSchema=True, header=True)
    df = df.select("genre", "lyrics")
    df = df.withColumn("lyrics", 
                       lower(trim(regexp_replace(col("lyrics"), r'[^\w\s]', ' '))))
    df = df.withColumn("lyrics", regexp_replace(col("lyrics"), r'\s+', ' '))
    return df

def load_and_clean_data_df(spark, df):
    """
    Load and clean the music dataset from a CSV file.
    
    Args:
        spark: SparkSession object
        file_path: Path to the input CSV file
    
    Returns:
        DataFrame with cleaned 'genre' and 'lyrics' columns
    """
    df = df.withColumn("lyrics", 
                       lower(trim(regexp_replace(col("lyrics"), r'[^\w\s]', ' '))))
    df = df.withColumn("lyrics", regexp_replace(col("lyrics"), r'\s+', ' '))
    return df