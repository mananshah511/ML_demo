from housing.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig, \
    ModelTrainerConfig,ModelPusherConfig,ModelEvaluationConfig,TrainingPipelineConfig
from housing.util.util import read_yaml_file
from housing.constant import *
from housing.exception import HousingException
import os,sys
from housing.logger import logging



class Configuration:

    def __init__(self,
                 config_file_path:str=CONFIG_PATH_NAME,
                 current_time_stamp:str=CURRENT_TIME_STAMP) -> None:
        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config=self.get_training_pipeline_config()
            self.time_stamp=current_time_stamp
        except Exception as e:
            raise HousingException(e,sys) from e


    def get_data_igestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_igestion_artifact_fact_dir=os.path.join(artifact_dir,DATA_IGENSTION_ARTIFACT_DIR_KEY,self.time_stamp)
            data_igestion_config=self.config_info[DATA_IGENSTION_CONFIG_KEY]

            data_igestion_download_url=data_igestion_config[DATA_IGENSTION_DOWNLOAD_URL_KEY]

            data_igestion_tgt_dir=os.path.join(data_igestion_artifact_fact_dir,data_igestion_config[DATA_IGENSTION_TGT_DOWNLOAD_DIR_KEY])

            data_igestion_raw_data_dir=os.path.join(data_igestion_artifact_fact_dir,data_igestion_config[DATA_IGENSTION_RAW_DATASET_DOWNLOAD_DIR_KEY])

            data_igestion_dir=os.path.join(data_igestion_artifact_fact_dir,data_igestion_config[DATA_IGENSTION_IGNESTED_DIR_KEY])

            data_igestion_test_dir=os.path.join(data_igestion_dir,data_igestion_config[DATA_IGENSTION_IGNESTED_TEST_DIR_KEY])

            data_igestion_train_dir=os.path.join(data_igestion_dir,data_igestion_config[DATA_IGENSTION_IGNESTED_TRAIN_DIR_KEY])

            data_igestion_config=DataIngestionConfig(dataset_download_url=data_igestion_download_url,
                                                     tgz_download_dir=data_igestion_tgt_dir,
                                                     raw_data_dir=data_igestion_raw_data_dir,
                                                     ingested_test_dir=data_igestion_test_dir,
                                                     ingested_train_dir=data_igestion_train_dir)
            logging.info(f"Data igenstion config:{data_igestion_config}")
            return data_igestion_config
        
            
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            logging.info(f"get validation config function started")
            artifact_dir=self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir=os.path.join(artifact_dir,DATA_VALIDATION_ARTIFACT_DIR_KEY,self.time_stamp)

            data_validation_config=self.config_info[DATA_VALIDATION_CONFIG_KEY]

            scheme_file_path=os.path.join(ROOT_DIR,data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],data_validation_config[DATA_VALIDATION_SCHEMA_FILENAME_KEY]
                                          )
            
            report_file_path=os.path.join(data_validation_artifact_dir,data_validation_config[DATA_VALIDATION_REPORT_FILE_DIR_KEY])

            report_page_file_path=os.path.join(data_validation_artifact_dir,data_validation_config[DATA_VALIDATION_REPORT_FILE_PAGE_DIR_KEY])

            datavaliadationconfig=DataValidationConfig(schema_file_path=scheme_file_path,
                                                       report_file_path=report_file_path,
                                                       report_page_file_path=report_page_file_path)
            logging.info(f"Data validation config:{datavaliadationconfig}")
            return datavaliadationconfig
        except Exception as e:
            raise HousingException(e,sys) from e

    def get_data_transforamtion_congig(self) -> DataTransformationConfig:
        pass

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        pass

    def get_model_evulation_config(self) -> ModelEvaluationConfig:
        pass

    def get_model_pusher_config(self) -> ModelPusherConfig:
        pass
    
    def get_training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            training_piepline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR,
                                      training_piepline_config[TRAINING_PIPELINE_NAME_KEY],
                                      training_piepline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])
            training_piepline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"training_pipeline_config{training_piepline_config}")
            return training_piepline_config 
        except Exception as e:
            raise HousingException(e,sys) from e

