import yaml
import numpy as np
import pandas as pd
from collections import namedtuple
import importlib
from housing.exception import HousingException
from housing.logger import logging
import os,sys
from sklearn.metrics import r2_score,mean_squared_error

GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"
InitializedModelDetail = namedtuple("InitializedModelDetail",
                                    ["model_serial_number", "model", "param_grid_search", "model_name"])
GridSearchedBestModel = namedtuple("GridSearchedBestModel", ["model_serial_number",
                                                             "model",
                                                             "best_model",
                                                             "best_parameters",
                                                             "best_score",
                                                             ])
BestModel = namedtuple("BestModel", ["model_serial_number",
                                     "model",
                                     "best_model",
                                     "best_parameters",
                                     "best_score", ])

MetricInfoArtifact = namedtuple("MetricInfoArtifact",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])

def get_evulate_regression_model(model_list:list,X_train=np.ndarray, y_train=np.ndarray, X_test=np.ndarray, y_test=np.ndarray
                                 , base_accuracy:float=0.6)->MetricInfoArtifact:
    try:
        index_number=0
        Metric_info_artifact=None
        logging.info("get evulation regression model log started")
        logging.info(f"Model list{model_list}")
        for model in model_list:
            model_name = str(model)

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_accuracy=r2_score(y_train,y_train_pred)
            test_accuracy=r2_score(y_test,y_test_pred)
            logging.info(f"train_accuracy: {train_accuracy}")
            logging.info(f"test_accuracy: {test_accuracy}")

            train_rmse=np.sqrt(mean_squared_error(y_train,y_train_pred))
            test_rmse=np.sqrt(mean_squared_error(y_test,y_test_pred))
            logging.info(f"train_rmse: {train_rmse}")
            logging.info(f"test_rmse: {test_rmse}")

            model_accuracy= (2*(train_accuracy*test_accuracy))/(train_accuracy + test_accuracy)
            diff_test_train_accu = np.abs(train_accuracy-test_accuracy)
            logging.info(f"model accuracy: {model_accuracy}")
            logging.info(f"difference in train test accuracy: {diff_test_train_accu}")

            if model_accuracy>=base_accuracy and diff_test_train_accu < 0.10:
                base_accuracy = model_accuracy

                Metric_info_artifact = MetricInfoArtifact(
                    model_name=model_name,
                    model_object=model,
                    train_rmse=train_rmse,
                    test_rmse=test_rmse,
                    train_accuracy=train_accuracy,
                    test_accuracy=test_accuracy,
                    model_accuracy=model_accuracy,
                    index_number=index_number
                )
            index_number+=1

        if Metric_info_artifact is None:
                logging.info("No model matched base accuracy")
        return Metric_info_artifact
    except Exception as e:
        raise HousingException(e,sys) from e
    


class ModelFactory:
    def __init__(self, model_config_path:str = None):
        try:
            self.config : dict = ModelFactory.read_param(model_config_path)
            self.grid_serch_cv_module : str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_serch_class_module : str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_serch_property_data : dict= dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])
            self.model_intial_config : dict = dict(self.config[MODEL_SELECTION_KEY])
            self.initlized_model_list = None
            self.grid_serched_best_model_list = None
            #print(self.get_initlized_model_list())
            print(self.config)
            print(self.model_intial_config)
        except Exception as e:
            raise HousingException(e,sys) from e
    @staticmethod
    def read_param(config_path:str)->dict:
        try:
            with open(config_path) as yaml_files:
                config:dict = yaml.safe_load(yaml_files)
                return config
        except Exception as e:
            raise HousingException(e,sys) from e
    @staticmethod
    def class_for_name(class_name:str, module_name:str):
        try:
            module = importlib.import_module(module_name)
            class_ref = getattr(module, class_name)
            return class_ref
        except Exception as e:
            raise HousingException(e,sys) from e
    @staticmethod
    def update_property_clas(insta_ref : object , property_data : dict):
        try:
            for key, value in property_data.items():
                setattr(insta_ref, key, value)
                return insta_ref
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_initlized_model_list(self)->list[InitializedModelDetail]:
        try:
            logging.info("get intilized model function is called")
            intilized_model_list=[]
            for model_seral_number in self.model_intial_config.keys():
                model_config = self.model_intial_config[model_seral_number]
                print(model_config)
                model_object_ref = ModelFactory.class_for_name(module_name=model_config[MODULE_KEY],
                                                               class_name=model_config[CLASS_KEY])
                print(model_object_ref)
                model = model_object_ref()

                if PARAM_KEY in model_config:
                    model_object_property_data = dict(model_config[PARAM_KEY])
                    model = ModelFactory.update_property_clas(insta_ref=model, property_data = model_object_property_data)
                param_grid_serach = model_config[SEARCH_PARAM_GRID_KEY]

                model_name = f"{model_config[MODULE_KEY]}.{model_config[CLASS_KEY]}"

                model_config = InitializedModelDetail(model_serial_number=model_seral_number,
                                                      model=model,
                                                      model_name=model_name,
                                                      param_grid_search=param_grid_serach)
                intilized_model_list.append(model_config)
                logging.info(f"Model list is{intilized_model_list}")
                self.initlized_model_list = intilized_model_list
            return self.initlized_model_list
        except Exception as e:
            raise HousingException(e,sys) from e  
    def initiate_best_parameter_search_for_initialized_models(self,initializedmodeldetails:list[InitializedModelDetail],
                                                              input_feature,
                                                              output_feature)->list[GridSearchedBestModel]:
        try:
            logging.info("Inside best parameter search models function")
            self.grid_serched_best_model_list=[]
            for initializedmodeldetails in initializedmodeldetails:
                logging.info(f"Calling best parameter model for:{initializedmodeldetails}")
                grid_serched_best_model=self.initiate_best_parameter_search_for_initialized_model(
                    initializedmodeldetails=initializedmodeldetails,
                    input_feature=input_feature,
                    output_feature=output_feature
                )
                logging.info(f"Best model is:{grid_serched_best_model}")
                self.grid_serched_best_model_list.append(grid_serched_best_model)
            return self.grid_serched_best_model_list
        except Exception as e:
            raise HousingException(e,sys) from e 
    def initiate_best_parameter_search_for_initialized_model(self,initializedmodeldetails:InitializedModelDetail,
                                                              input_feature,
                                                              output_feature)->GridSearchedBestModel:
        try:
            logging.info("Best parameter for individual function is called")
            grid_search_cv_ref = ModelFactory.class_for_name(module_name=self.grid_serch_cv_module,
                                                             class_name=self.grid_serch_class_module)
            grid_serch_cv = grid_search_cv_ref(estimator=initializedmodeldetails.model,
                                               param_grid = initializedmodeldetails.param_grid_search)
            grid_serch_cv = ModelFactory.update_property_clas(grid_serch_cv, self.grid_serch_property_data)
            #logging.info(f"{input_feature.shape},{output_feature.shape}")
            grid_serch_cv.fit(input_feature,output_feature)

            grid_search_best_model = GridSearchedBestModel(model_serial_number=initializedmodeldetails.model_serial_number,
                                                           model=initializedmodeldetails.model,
                                                           best_model=grid_serch_cv.best_estimator_,
                                                             best_parameters=grid_serch_cv.best_params_,
                                                             best_score=grid_serch_cv.best_score_)
            return grid_search_best_model
        except Exception as e:
            raise HousingException(e,sys) from e 
    @staticmethod
    def get_best_model_from_grid_serached_best_model_list(grid_serached_best_model:list[GridSearchedBestModel],
                                                          base_accuracy=0.6)->BestModel:
        try:
            logging.info("Best model from grid serched best model list function started")
            best_model=None
            for grid_serached_model in grid_serached_best_model:
                if base_accuracy < grid_serached_model.best_score:
                    base_accuracy = grid_serached_model.best_score

                    best_model = grid_serached_model
            if not best_model:
                raise Exception("None has base accuracy")
            return best_model
        except Exception as e:
            raise HousingException(e,sys) from e
    def get_best_model(self,X,y,bas_accuracy=0.6)->BestModel:
        try:
            logging.info("Get best model function started")
            logging.info("Calling get intlized model list function")
            Initlized_model_list=self.get_initlized_model_list()
            logging.info(f"Final model list is:{Initlized_model_list}")
            logging.info("Calling get best parameteres seearch from intlized models function")
            grid_serched_best_model_list=self.initiate_best_parameter_search_for_initialized_models(
                initializedmodeldetails=Initlized_model_list,
                input_feature=X,
                output_feature=y
            )
            logging.info(f"Best individual models with paramater is :{grid_serched_best_model_list}")
            logging.info("Calling best model from grid serached model list function")
            return ModelFactory.get_best_model_from_grid_serached_best_model_list(grid_serached_best_model=grid_serched_best_model_list,
                                                                                  base_accuracy=0.6)

        except Exception as e:
            raise HousingException(e,sys) from e