# import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
import joblib

description = """
JEDHA Project predicting Tesla quote from Elon Musk Tweet. 

## Preview

Where you can: 
* `/preview` a few rows of your dataset
* get `/unique-values` of a given column in your dataset

## Predict

Where you can: 
* `/predict` a given Elon Musk Tweet 


Check out documentation for more information on each endpoint. 
"""

tags_metadata = [
    {
        "name": "LoadTweets",
        "description": "Load Elon Musk Tweets local file to Dataframe"
    },
   {
        "name": "LoadTeslaQuote",
        "description": "Load Tesla Quote local to Dataframe"
    },

    {
        "name": "loadMidleFile",
        "description": "Load intermediar file to Dataframe"
    },

    {
        "name": "S3LoadTweets1",
        "description": "Load 1 Elon Musk Tweets from S3  to Dataframe"    },

    {
        "name": "S3LoadTweets",
        "description": "Load Elon Musk Tweets from S3  to Dataframe"
    }

]

app = FastAPI(
    title="👨‍💼 Elon Musk Twee Tesla Quote Predict API",
    description=description,
    version="0.1",
    contact={
        "name": "Elon Musk Twee Tesla Quote Predict API - by dsf-od-05 Jedha",
        "url": "https://jedha.co",
    },
    openapi_tags=tags_metadata
)

# Function to load the DataFrame from S3
def load_dataframe_from_s3(bucket_name: str, s3_key: str):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=s3_key)
        content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(content))
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/loadTweets", tags=["LoadTweets"])
async def random_tweet(rows: int=10):
    """
    Load file of Tesla Qotes in dataframe. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    """
    Simply returns a welcome message!
    """

    df_tweets = pd.read_csv('data/elon_musk_tweets.csv')
    sample = df_tweets.sample(rows)
    return sample.to_json()
    


@app.get("/loadTesla", tags=["LoadTeslaQuote"])
async def random_tesla(rows: int=10):
    """
    Load file of Tesla Qotes in dataframe. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    """
    Simply returns a welcome message!
    """


    df_tesla = pd.read_excel("data/courstesla20222024.xlsx")
    sample = df_tesla.sample(rows)
    return sample.to_json()

@app.get("/loadMidleFile", tags=["loadMidleFile"])
async def random_tesla(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    """
    Simply returns a welcome message!
    """
    
    df = pd.read_csv("data/df_total3v1.csv")
    sample = df.sample(rows)
    return sample.to_json()

@app.get("/S3loadTweets1", tags=["S3loadTweets1"])
async def random_S3Tweets1(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    """
    Simply returns a welcome message!
    """
    
    df = pd.read_csv("https://elon-tweet-tesla-010348410745.s3-accesspoint.eu-central-1.amazonaws.com/mlflow-artefacts/elon_musk_tweets.csv")
    sample = df.sample(rows)
    return sample.to_json()


@app.get("/S3loadTweets", tags=["S3loadTweets"])
async def random_S3Tweets(rows: int=10):
    """
    Get a sample of your whole dataset. 
    You can specify how many rows you want by specifying a value for `rows`, default is `10`
    """
    """
    Simply returns a welcome message!
    """
    bucket_name = "jedha-mlflow-bucket"
    s3_key = "mlflow-artefacts/elon_musk_tweets.csv"
    df = load_dataframe_from_s3(bucket_name, s3_key)
    sample = df.sample(rows)
    return sample.to_json()

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)