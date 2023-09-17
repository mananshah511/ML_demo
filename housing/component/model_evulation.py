import os,sys
from housing.exception import HousingException
from housing.logger import logging
from housing.util.util import read_yaml_file,load_numpy_array,load_object,save_object,write_yaml_file
from housing.entity.artifact_entity import ModelTrainerArtifact,DataIgenstionArtifact,DataTranformArtifact,DataValidationArtifact,ModelEvulationArtifact
from housing.entity.config_entity import ModelEvaluationConfig
from housing.constant import *
import pandas as pd
import numpy as np
from housing.entity.model_factory import get_evulate_regression_model


class ModelEvulation:

    def __init__(self,
                 model_evulation_config : ModelEvaluationConfig,
                 data_igstion_artifact : DataIgenstionArtifact,
                 data_validation_artifact : DataValidationArtifact,
                 model_trainer_artifact : ModelTrainerArtifact):
        try:
            self.model_evulation_config = model_evulation_config
            self.data_igstion_artifact = data_igstion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_best_model(self):
        try:
            logging.info("Get best model function in evulation started")
            model_evultion_config_file_path = self.model_evulation_config.model_evaluation_file_path
            model = None

            if not os.path.exists(model_evultion_config_file_path):
                write_yaml_file(file_path=model_evultion_config_file_path)
                logging.info("Writing blank file as no file was in the given dir")
                return model

            
            model_evulation_file_content = read_yaml_file(file_path=model_evultion_config_file_path)
            
            model_evulation_file_content = dict() if model_evulation_file_content is None else model_evulation_file_content
            
            if BEST_MODEL_KEY not in model_evulation_file_content:
                return model
            
            model = load_object(file_path=model_evulation_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])

            return model
                
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_update_evulation_report(self, model_evulation_artifact :ModelEvulationArtifact):
        try:
            evu_file_path = self.model_evulation_config.model_evaluation_file_path
            logging.info(f"model evulation file path:{evu_file_path}")
            model_eval_content = read_yaml_file(file_path= evu_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content

            previous_best_model = None

            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logging.info(f"previous evulation report : {model_eval_content}")

            eval_result = { BEST_MODEL_KEY : {MODEL_PATH_KEY: model_evulation_artifact.evaluated_model_path}}

            if previous_best_model is not None:
                model_history = {self.model_evulation_config.time_stamp : previous_best_model
                                 }
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY:model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated model evulation report: {model_eval_content}")
            write_yaml_file(file_path=evu_file_path,data=model_eval_content)
            logging.info("Writing successfull")
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def initiate_model_evulation(self)->ModelEvulationArtifact:
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            train_obj = load_object(file_path=trained_model_file_path)

            train_file_path = self.data_igstion_artifact.traine_file_path
            test_file_path = self.data_igstion_artifact.test_file__path

            schema_file_path = self.data_validation_artifact.schema_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            schema_content = read_yaml_file(file_path=schema_file_path)

            target_column = schema_content[TARGET_COLUMN_KEY]

            train_arry = np.array(train_df[target_column])
            test_arry = np.array(test_df[target_column])

            train_df = train_df.drop(target_column,axis=1)
            test_df = test_df.drop(target_column,axis=1)

            model = self.get_best_model()

            if model is None:
                logging.info("No model found hence accepting this model")
                model_evulation_artifact = ModelEvulationArtifact(evaluated_model_path=trained_model_file_path,
                                                                is_model_accepted=True)
                self.get_update_evulation_report(model_evulation_artifact)
                logging.info(f"model evulation artifact: {model_evulation_artifact}")

                return model_evulation_artifact
            
            model_list = [model , train_obj]

            metric_info_artifact = get_evulate_regression_model(model_list= model_list,
                                                                X_train= train_df,
                                                                X_test = test_df,
                                                                y_train=train_arry,
                                                                y_test=test_arry,
                                                                base_accuracy=self.model_trainer_artifact.model_accyracy)
            
            logging.info(f"model info artifact: {metric_info_artifact}"
                         )
            
            if metric_info_artifact is None:
                model_evulation_artifact = ModelEvulationArtifact(is_model_accepted=False,
                                                                  evaluated_model_path=trained_model_file_path)
                return model_evulation_artifact

            if metric_info_artifact.index_number==1:
                model_evulation_artifact = ModelEvulationArtifact(is_model_accepted=True,
                                                                  evaluated_model_path=trained_model_file_path)
                self.get_update_evulation_report(model_evulation_artifact)
                logging.info(f"model accepted : {model_evulation_artifact}")

            else:
                logging.info("Trained model is not better then existing model hence not accepting it")
                model_evulation_artifact = ModelEvulationArtifact(is_model_accepted=False,
                                                                  evaluated_model_path=trained_model_file_path)
                
            return model_evulation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'>>'*40}Model evulation log completed.{'<<'*40} \n\n")
                
