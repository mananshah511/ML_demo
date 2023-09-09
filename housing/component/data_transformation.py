import os,sys
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import DataIgenstionArtifact,DataValidationArtifact,DataTranformArtifact
from housing.entity.config_entity import DataTransformationConfig
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd
from housing.util.util import read_yaml_file
from housing.constant import *
import dill

class FeatureGen(BaseEstimator,TransformerMixin):

    def __init__(self,add_bedroom_per_room=True,
                 total_room_idx=3,
                 population_idx=5,
                 household_idx=6,
                 total_bedroom=4, columns=None):
        try:
            self.columns=columns
            if self.columns is not None:
                total_room_idx=self.columns.index(COLUMN_TOTAL_ROOMS)
                population_idx=self.columns.index(COLUMN_POPULATION)
                household_idx=self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedroom=self.columns.index(COLUMN_TOTAL_BEDROOM)
            self.add_bedroom_per_room=add_bedroom_per_room
            self.total_room_idx=total_room_idx
            self.population_idx=population_idx
            self.household_idx=household_idx
            self.total_bedroom=total_bedroom
        except Exception as e:
            raise HousingException(e,sys) from e

    def fit(self,X,y=None):
        return self

    def transform(self,X,y=None):
        try:
            room_per_household = X[:,self.total_room_idx]/X[:,self.household_idx]

            population_per_household = X[:,self.population_idx]/X[:,self.household_idx]

            if self.add_bedroom_per_room:
                bedroom_per_room = X[:,self.total_bedroom]/X[:,self.total_room_idx]

                generated_feature=np.c_[X,room_per_household,population_per_household,bedroom_per_room]
            else:
                generated_feature=np.c_[X,room_per_household,population_per_household]
            return generated_feature
        except Exception as e:
            raise HousingException(e,sys) from e
class DataTransformation:

    def __init__(self,data_transformation_config: DataTransformationConfig,
                 data_igention_artifact: DataIgenstionArtifact,
                 data_validation_artifact: DataValidationArtifact):
        try:
            logging.info(f"{'>>'*20}Data Transform log started.{'<<'*20} ")
            self.data_tranform_config = data_transformation_config
            self.data_igention_artifact = data_igention_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        
    
    def get_data_tranform_object(self)-> ColumnTransformer:
        try:
            logging.info("get data tranform object started")
            schema_file_path=self.data_validation_artifact.schema_file_path
            logging.info(f"scheme file path is:{schema_file_path}")
            dataset_scheme=read_yaml_file(file_path=schema_file_path)

            num_coulmns=dataset_scheme[NUMERICAL_COLUMN_KEY]
            cat_columns=dataset_scheme[CATEGORICAL_COLUMN_KEY]
            logging.info(f"Numerical columns are:{num_coulmns}")
            logging.info(f"Categorical columns are;{cat_columns}")
            num_pipeline=Pipeline(steps=[('imputer',SimpleImputer(strategy='median')),
                                         ('FeatureGen',FeatureGen(add_bedroom_per_room=self.data_tranform_config.add_bedroom_per_room,\
                                                                  columns=num_coulmns)),
                                        ('scaler',StandardScaler())
                                         ])
            logging.info("numerical pipeline is esambled")
            cat_pipeline=Pipeline(steps=[('imputer',SimpleImputer(strategy='most_frequent')),
                                         ('onehotencoding',OneHotEncoder()),
                                        ('scaler',StandardScaler(with_mean=False))
                                         ])
            logging.info("categorical pipeline is esabmled")
            preprocessing = ColumnTransformer([('num_pipeline',num_pipeline,num_coulmns),
                                               ('cat_pipeline',cat_pipeline,cat_columns)])
            return preprocessing
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def initiate_data_transformation(self)->DataTranformArtifact:
        try:
            logging.info("initiate data tranformation functionn started")
            logging.info("making preprocessing object")

            preprocessing_obj=self.get_data_tranform_object()

            logging.info("loading training and testing path")

            train_path=self.data_igention_artifact.traine_file_path

            test_path=self.data_igention_artifact.test_file__path

            logging.info(f"train path is :{train_path}")

            logging.info(f"test path is :{test_path}")

            logging.info(f"reading train and test files into pandas dataframe")
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("reading schema file for traget column name")

            schema_path=self.data_validation_artifact.schema_file_path

            logging.info("reading scheme yaml file")

            schema=read_yaml_file(schema_path)

            target_coulmn_name=schema[TARGET_COLUMN_KEY]

            logging.info("splitting target columns from the dataframe")

            train_feature_df=train_df.drop(columns=[target_coulmn_name],axis=1)
            train_target_df=train_df[target_coulmn_name]

            test_feature_df=test_df.drop(columns=[target_coulmn_name],axis=1)
            test_target_df=test_df[target_coulmn_name]

            logging.info("applying preprocessing")

            train_feature_arry=preprocessing_obj.fit_transform(train_feature_df)
            test_feature_arry=preprocessing_obj.transform(test_feature_df)

            train_arr=np.c_[train_feature_arry,np.array(train_target_df)]
            test_arr=np.c_[test_feature_arry,np.array(test_target_df)]

            logging.info("getting transform dir")
            transform_train_dir_path=self.data_tranform_config.transformed_train_dir

            transform_test_dir_path=self.data_tranform_config.transformed_test_dir

            logging.info("getting basefile name")
            train_file_name=os.path.basename(train_path).replace(".csv",".npy")
            test_file_name=os.path.basename(test_path).replace(".csv",".npy")

            logging.info("getting combine file path")
            
            transform_train_file_path = os.path.join(transform_train_dir_path,train_file_name)

            transform_test_file_path  = os.path.join(transform_test_dir_path,test_file_name)
            logging.info(f"{transform_train_dir_path}")
            logging.info(f"{transform_train_file_path}")
            
            logging.info("saving array")
            train_dir=os.path.dirname(transform_train_file_path)
            os.makedirs(train_dir,exist_ok=True)
            test_dir=os.path.dirname(transform_test_file_path)
            os.makedirs(test_dir,exist_ok=True)
            np.save(transform_train_file_path,train_arr)
            np.save(transform_test_file_path,test_arr)
            logging.info(f"{train_dir}")
            logging.info("saving preprocessing object")
            preprocessing_object_file_path=self.data_tranform_config.preprocessed_object_file_path

            pre_dir=os.path.dirname(preprocessing_object_file_path)
            os.makedirs(pre_dir,exist_ok=True)
            with open(preprocessing_object_file_path, "wb") as file_obj:
                dill.dump(preprocessing_obj, file_obj)





            Data_trasnform_artifact=DataTranformArtifact(transformed_test_file_path=transform_test_file_path,
                                                         transformed_train_file_path=transform_train_file_path,
                                                         preprocessed_object_file_path=preprocessing_object_file_path,
                                                         is_transformed="True",
                                                         message="successfull completed")
            return Data_trasnform_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
    def __del__(self):
        logging.info(f"{'>>'*50}Data Transform log completed.{'<<'*50} \n\n")