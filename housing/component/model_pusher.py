import os,sys
from housing.exception import HousingException
from housing.logger import logging
from housing.entity.artifact_entity import ModelPusherArtifact,ModelEvulationArtifact
from housing.entity.config_entity import ModelPusherConfig
import shutil

class ModelPusher:

    def __init__(self, model_pusher_config : ModelPusherConfig,
                 model_evulation_artifact : ModelEvulationArtifact):
        try:
            logging.info(f"{'>>'*40}Model Pusher log started.{'<<'*40} \n\n")
            self.model_pusher_config = model_pusher_config
            self.model_evulation_artifact = model_evulation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def export_model(self)->ModelPusherArtifact:
        try:
            trained_model_path=self.model_evulation_artifact.evaluated_model_path
            export_dir = self.model_pusher_config.export_dir_path
            train_file_name = os.path.basename(trained_model_path)
            export_file_path = os.path.join(export_dir,train_file_name)
            os.makedirs(export_file_path, exist_ok=True)
            shutil.copy(src=trained_model_path,dst=export_file_path)

            logging.info(f"trained model is copied in : {export_file_path}")

            model_pusher_artifact = ModelPusherArtifact(export_dir_path= export_file_path)

            return ModelPusherArtifact
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def initiate_model_pusher(self):
        try:
            self.export_model()
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'>>'*40}Model Pusher log completed.{'<<'*40} \n\n")