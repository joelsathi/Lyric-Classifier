# 🎶 Lyric Classifier using MLlib (Apache Spark)

**Name:** Joel Sathiyendra  
**Index No:** 200590J  

---

## 🌐 Live Demo
Check out the deployed application:  
[http://157.230.5.94/](http://157.230.5.94/)

---

## 📂 Project Structure

| <br>
|-- data # Contains dataset files <br>
|-- data-generation # Scripts for collecting and preparing data <br>
|-- training-pipeline # Training pipeline code<br>


## 📊 Data Collection & Preparation

- Data is gathered from **Spotify** and **Genius** APIs.
- To use the APIs:
  1. Get API credentials.
  2. Add them to a `.env` file (refer to `.env.sample`).

- The resulting dataset contains the following columns:
  - `artist_name`
  - `track_name`
  - `release_date`
  - `genre`
  - `lyrics`

### 🎵 Supported Genres
- Pop
- Country
- Blues
- Jazz
- Reggae
- Rock
- Hip Hop
- Classic (added from a student dataset)

> Dataset sources include the [Mendeley dataset](https://data.mendeley.com/datasets/3t9vbwxgr5/2) and additional merged datasets.

---

## Model Training

To train the model, run:

```bash
cd training-pipeline
python trainer.py --dataset_path /path/to/dataset.csv
```


🔄 Training Pipeline Steps
1. Tokenizer <br>
Splits lyrics into words.

2. StopWordsRemover <br>
Removes common stopwords.

3. StemmerTransformer <br>
Applies stemming to words.

4. WordArrayToStringTransformer <br>
Converts word arrays back into a processed string.

5. StringIndexer <br>
Indexes genre labels.

6. CountVectorizer <br>
Creates feature vectors (vocab size: 10,000, minDF: 5).

7. NaiveBayes Classifier <br>
Trains the model (smoothing = 1).


📈 Model Performance
- Two models are trained:

    - Original Mendeley dataset model.

    - Merged dataset model.

- Merged dataset model accuracy: 37.5%

## Running the Application
### Option 1: Run Locally
```bash
./run.sh
```
This will start the front-end and open the browser where you can input lyrics and view predictions.

### Option 2: Run with Docker
```bash
./run_docker.sh
```

