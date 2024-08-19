import os
import sys

from src.exception.exception import NetworkSecurityException
from src.logger.logger import logging

from src.pipeline.training_pipeline import TrainingPipeline


def start_training():
    try:
        logging.info("Training has Started")
        
        model_training=TrainingPipeline()
        model_training.run_pipeline()
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        


if __name__=='__main__':
    start_training()