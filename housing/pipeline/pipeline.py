from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIgenstionArtifact
from housing.exception import HousingException
from housing.config.configuration import Configuration
from housing.component.data_igestion import DataIgenstion
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataValidationArtifact
from housing.component.data_validation import DataValidation
from housing.entity.artifact_entity import DataTranformArtifact
from housing.component.data_transformation import DataTransformation
from housing.entity.config_entity import ModelTrainerConfig
from housing.entity.artifact_entity import ModelTrainerArtifact
from housing.component.model_trainer import ModelTrainer
from housing.component.model_evulation import ModelEvulation
import sys,os

class Pipeline():
    def __init__(self,config:Configuration=Configuration()) -> None:
        try:
            self.config=config
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def start_data_igenstion(self)->DataIgenstionArtifact:
        try:
            dataigention = DataIgenstion(data_igention_config=self.config.get_data_igestion_config())
            return dataigention.initate_data_igenetion()
        except Exception as e:
            raise HousingException(e,sys) from e
    def start_data_validation(self,data_igenstion_artifact:DataIgenstionArtifact)->DataValidationArtifact:
        try:
            datavalidation = DataValidation(data_validation_config=self.config.get_data_validation_config(),data_igenstion_artifact=data_igenstion_artifact)
            return datavalidation.initiate_data_validation()
            
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def start_data_transformation(self,data_igenstion_artifact:DataIgenstionArtifact,data_validatin_artifact:
                                  DataValidationArtifact)->DataTranformArtifact:
        try:
            datatran = DataTransformation(data_transformation_config=self.config.get_data_transforamtion_config(),
                                          data_igention_artifact=data_igenstion_artifact,
                                          data_validation_artifact=data_validatin_artifact)
            return datatran.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e,sys) from e
    def start_model_training(self,data_transform_artifact:
                             DataTranformArtifact)->ModelTrainerArtifact:
        try:
            model_train = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                       data_transform_artifact=data_transform_artifact)
            return model_train.initlized_model_trainer()
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def start_model_evulation(self,data_valiadtion_artifact : DataValidationArtifact,
                              data_igenstion_artifact : DataIgenstionArtifact , 
                              model_training_artifact : ModelTrainerArtifact):
        try:
            model_evulation = ModelEvulation(model_evulation_config=self.config.get_model_evulation_config(),
                                             data_igstion_artifact= data_igenstion_artifact,
                                             data_validation_artifact= data_valiadtion_artifact,
                                             model_trainer_artifact= model_training_artifact)
            return model_evulation.initiate_model_evulation()
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_igenstion()
        data_validation_artifact =self.start_data_validation(data_igenstion_artifact=data_ingestion_artifact)
        data_transform_artifact = self.start_data_transformation(data_validatin_artifact=data_validation_artifact,
                                                                 data_igenstion_artifact=data_ingestion_artifact)
        model_trainer_artifact = self.start_model_training(data_transform_artifact=data_transform_artifact)
        model_evulation_artifact = self.start_model_evulation(data_igenstion_artifact=data_ingestion_artifact,
                                                              data_valiadtion_artifact=data_validation_artifact,
                                                              model_training_artifact=model_trainer_artifact)