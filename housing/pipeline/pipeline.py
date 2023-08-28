from housing.entity.config_entity import DataIngestionConfig
from housing.entity.artifact_entity import DataIgenstionArtifact
from housing.exception import HousingException
from housing.config.configuration import Configuration
from housing.component.data_igestion import DataIgenstion
import sys,os

class Pipeline():
    def __init__(self,config:Configuration=Configuration()) -> None:
        try:
            self.config=config
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def start_data_igenstion(self)->DataIgenstionArtifact:
        try:
            print(self.config.get_data_igestion_config())
            dataigention = DataIgenstion(data_igention_config=self.config.get_data_igestion_config())
            return dataigention.initate_data_igenetion()
        except Exception as e:
            raise HousingException(e,sys) from e
    def run_pipeline(self):
        data_ingestion_artifact = self.start_data_igenstion()