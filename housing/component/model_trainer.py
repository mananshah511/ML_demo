import os,sys
from housing.entity.model_factory import ModelFactory,get_evulate_regression_model
from housing.exception import HousingException
from housing.logger import logging
from housing.constant import *
from housing.entity.artifact_entity import ModelTrainerArtifact,DataIgenstionArtifact,DataTranformArtifact,DataValidationArtifact
from housing.entity.config_entity import ModelTrainerConfig
from housing.entity.model_factory import GridSearchedBestModel,MetricInfoArtifact
from housing.util.util import load_numpy_array,load_object,save_object

class HousingestimatorModel:

    def __init__(self,preprocessing_object, trained_model):
        self.pre_processing_object = preprocessing_object
        self.trained_model = trained_model

    def predict(self,X):
        transfromed_feature = self.pre_processing_object.transform(X)
        return self.trained_model.predict(transfromed_feature)
class ModelTrainer:

    def __init__(self, model_trainer_config : ModelTrainerConfig, data_transform_artifact : DataTranformArtifact) -> None:
        try:
            logging.info(f"{'>>'*20}Model Trainer log started.{'<<'*20} ")
            self.model_trainer_config = model_trainer_config
            self.data_transform_artifact =data_transform_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def initlized_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("initlized model trainer function started")

            logging.info("loading training transformed data")
            transfrom_train_file_path = self.data_transform_artifact.transformed_train_file_path
            train_array= load_numpy_array(transfrom_train_file_path)

            logging.info("loading testing transfromed data")
            transfrom_test_file_path = self.data_transform_artifact.transformed_test_file_path
            test_array= load_numpy_array(transfrom_test_file_path)

            logging.info("splitting into input and target features")
            X_train,y_train,X_test,y_test = train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]

            logging.info("Exctracting model config path")
            model_config_path=self.model_trainer_config.model_config_file_path

            logging.info("initlization of model factory class")
            model_factory = ModelFactory(model_config_path=model_config_path)

            base_accuracy= self.model_trainer_config.base_accuracy

            logging.info(f"base accuracy: {base_accuracy}")

            logging.info("Generating best model")

            best_model = model_factory.get_best_model(X=X_train,y=y_train,bas_accuracy=base_accuracy)

            logging.info(f"best model found on: {best_model}")

            logging.info("Exctracting trained model list")
            grid_serched_best_model_list:list[GridSearchedBestModel]=model_factory.grid_serched_best_model_list

            model_list = [model.best_model for model in grid_serched_best_model_list]

            logging.info("evulation of the trained model on training and testing dataset")

            metric_info:MetricInfoArtifact=get_evulate_regression_model(X_train=X_train,y_train=y_train,X_test=X_test,
                                                                        y_test=y_test,base_accuracy=base_accuracy,model_list=model_list)
            preprossedobj = load_object(file_path=self.data_transform_artifact.preprocessed_object_file_path)
            model_object = metric_info.model_object

            housing_model =HousingestimatorModel(preprocessing_object=preprossedobj,trained_model=model_object)

            logging.info(f"saving our model in :{self.model_trainer_config.trained_model_file_path}")

            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=housing_model)

            model_trainer_artifact = ModelTrainerArtifact(is_trained="true",
                                                          message="Model trained successfully",
                                                          trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                          train_rmse=metric_info.train_rmse,
                                                          test_rmse=metric_info.test_rmse,
                                                          train_accuracy=metric_info.train_accuracy,
                                                          test_accuracy=metric_info.test_accuracy,
                                                          model_accyracy=metric_info.model_accuracy)
            logging.info(f"model_artifact{model_trainer_artifact}")
            return model_trainer_artifact





        except Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'>>'*30}Model training log completed.{'<<'*30} \n\n")