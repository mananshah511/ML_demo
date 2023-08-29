from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIgenstionArtifact
from housing.exception import HousingException
from housing.config.configuration import Configuration
from housing.component.data_igestion import DataIgenstion
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataValidationArtifact
from housing.component.data_validation import DataValidation

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
    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_igenstion()
        data_validation_artifact =self.start_data_validation(data_igenstion_artifact=data_ingestion_artifact)