from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

def train_model(pipeline, train_df):
    """
    Train the model using cross-validation with an expanded parameter grid.
    
    Args:
        pipeline: Configured Pipeline object
        train_df: Training DataFrame
    
    Returns:
        CrossValidatorModel with the best model
    """
    stages = pipeline.getStages()
    countVectors = stages[5]  # CountVectorizer is the 6th stage (0-based index)
    nb = stages[6]  # NaiveBayes is the 7th stage
    
    # Expanded parameter grid for Naive Bayes and CountVectorizer
    paramGrid = ParamGridBuilder() \
        .addGrid(countVectors.vocabSize, [5000, 10000, 15000]) \
        .addGrid(countVectors.minDF, [3, 5, 7]) \
        .addGrid(nb.smoothing, [0.5, 1.0, 1.5]) \
        .build()

    evaluator = MulticlassClassificationEvaluator(
        labelCol="label", 
        predictionCol="prediction", 
        metricName="accuracy"
    )
    
    crossval = CrossValidator(
        estimator=pipeline,
        estimatorParamMaps=paramGrid,
        evaluator=evaluator,
        numFolds=3
    )
    
    cvModel = crossval.fit(train_df)
    return cvModel