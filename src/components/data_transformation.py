import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from src.constant.training_pipeline import TARGET_COLUMN
from src.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from src.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from src.entity.config_entity import DataTransformationConfig
from src.exception.exception import NetworkSecurityException
from src.logger.logger import logging

from src.utils.main_utils.utils import save_numpy_array_data,save_object







class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
            
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
            
    @staticmethod
    def read_table(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def get_data_transformer_object(cls)->Pipeline:
        """
        
        It initiates a KNN Imputer obect with parameter specified in training Pipeline.py file and returs a pipeline object with the  KNNImputer object 
        as First Step
        
        Args:
         cls:DataTransformatiom

        Returns:
            Pipeline: _description_
        """
        
        try:
            imputer:KNNImputer=KNNImputer(
                **DATA_TRANSFORMATION_IMPUTER_PARAMS
            )
            
            
            logging.info(
                f"Initialize KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            
            preprocessor:Pipeline=Pipeline([("imputer",imputer)])
            
            logging.info(
                "Exited get_data_transformer object method of DataTransformation class"
            )
            
            return preprocessor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self,)-> DataTransformationArtifact:
        logging.info('Entered initiate_data_transformation method of Datatransformation class')
        try:
            logging.info('Started Data Transformation')
            
            train_df=DataTransformation.read_table(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_table(self.data_validation_artifact.valid_test_file_path)
            
            preprocessor=self.get_data_transformer_object()
            
            logging.info('Got the Preprocessor object')
            
            ##Training Dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            
            ##Testing Dataframe 
            
            
            input_feature_test_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=train_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_train_df.replace(-1,0)
            
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)
            
            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]
            
            ##Save Numpy array Data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            
            
            ## Preparing Artifacts
            
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                
            )
            logging.info(f"Data transformation artifact:{data_transformation_artifact}")
            
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)


            
            
            
            
    
    
        
        
    
    