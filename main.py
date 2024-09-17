import sys
import os

import certifi
ca = certifi.where()
print(f'The ca is {ca}')
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(f'The Mango_dd_url{mongo_db_url}')

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID_ENV_KEY")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY_ENV_KEY")

os.environ["AWS_ACCESS_KEY_ID"]=AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"]=AWS_SECRET_ACCESS_KEY

import pymongo

#from src.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from src.constant.training_pipeline import *

from src.exception.exception import NetworkSecurityException
from src.logger.logger import logging
from src.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from src.utils.ml_utils.model.estimator import ModelResolver
from src.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


from src.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


        
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        # if train_pipeline.is_pipeline_running:
        #     return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    

'''@app.get("/predict")
async def predict_route(request:Request,file: UploadFile = File(...)):
    try:
        pass
    except Exception as e:
            raise NetworkSecurityException(e,sys)
'''
# def main():
#     try:
#         training_pipeline = TrainingPipeline()
#         training_pipeline.run_pipeline() 
#     except Exception as e:
#             raise NetworkSecurityException(e,sys)

               
if __name__=="__main__":
    app_run(app, host="localhost", port=8000)