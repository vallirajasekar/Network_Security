import os
import sys


import numpy as np
import pandas as pd 

"""

Defining Common constant Variable

"""


TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="NetworkData.csv"


TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

PREPROCESSING_OBJECT_FILE_NAME='preprocessing.pkl'
MODEL_FILE_NAME="model.pkl"
SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")
SCHEMA_DROPS_COLS="drop_columns"
SAVED_MODEL_DIR=os.path.join("saved_models")

"""
    Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME:str="NetworkData"
DATA_INGESTION_DATABASE_NAME:str="KNAcademy"
DATA_INGESTION_DIR_NAME:str="NetworkData"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float=0.2
