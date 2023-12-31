import os,sys
from housing.entity.artifact_entity import DataIgenstionArtifact
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataValidationArtifact
from housing.constant import *
from housing.exception import HousingException
from housing.logger import logging
import pandas as pd
import numpy as np
from housing.util.util import read_yaml_file
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,data_igenstion_artifact:DataIgenstionArtifact)->None:
        try:
            logging.info(f"{'>>'*20}Data Validation log started.{'<<'*20} ")
            self.data_validation_config = data_validation_config
            self.data_igenstion_artifact = data_igenstion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_train_test_data(self):
        try:
            logging.info(f"Reading training and testing file")
            train_file = pd.read_csv(self.data_igenstion_artifact.traine_file_path)
            test_file = pd.read_csv(self.data_igenstion_artifact.traine_file_path)
            logging.info(f"Reading successfull")
            return train_file,test_file
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def check_train_test_dir_exist(self)->bool:
        try:
            logging.info(f"Checking train and test dir exist or not")
            train_path_flag = False
            test_path_flag = False
            train_path=self.data_igenstion_artifact.traine_file_path
            test_path=self.data_igenstion_artifact.test_file__path

            train_path_flag = os.path.exists(train_path)
            test_path_flag = os.path.exists(test_path)

            final_path_test=False

            if train_path_flag and test_path_flag:
                final_path_test = True
                logging.info("training and testing path is there:")
            else:
                raise Exception("Path for training and testing is not avaiable")
            return final_path_test
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def schema_validation(self)->bool:
        try:
            validation_status = True
            train_file,test_file=self.get_train_test_data()
            train_coulmns=len(train_file.columns)
            test_coulmns=len(test_file.columns)
            logging.info(f"Number of columns in train file is:{train_coulmns}")
            logging.info(f"Number of columns in test file is:{test_coulmns}")

            schema_file = self.data_validation_config.schema_file_path
            logging.info(f"Schema file path:{schema_file}")
            dict_schema = read_yaml_file(schema_file)
            logging.info(f"Schema file looks like:{dict_schema}")
            
            categorical_value_actual = list(dict_schema['domain_value']['ocean_proximity'])
            logging.info(f"categorical value checking from scheme file, actual value is:{categorical_value_actual}")
            train_target_value_list=list(train_file['ocean_proximity'])
            test_target_value_list=list(test_file['ocean_proximity'])

            train_cat_flag = True
            test_cat_flag = True
            for i in range(len(train_target_value_list)):
                if train_target_value_list[i] not in categorical_value_actual:
                    train_cat_flag = False
                    validation_status = False

            for i in range(len(test_target_value_list)):
                if test_target_value_list[i] not in categorical_value_actual:
                    test_cat_flag = False
                    validation_status = False

            if train_cat_flag and test_cat_flag:
                logging.info("Categorical values are in the range")

            if list(dict_schema['columns'])==list(train_file.columns):
                logging.info("Training columns are valid")
            else:
                validation_status = False

            if list(dict_schema['columns'])==list(test_file.columns):
                logging.info("Test columns are valid")
            else:
                validation_status = False
            return validation_status
        except Exception as e:
            raise HousingException(e,sys) from e
        
        
    
    def save_data_drift_report(self):
        try:
            logging.info(f"Save data drift report started")
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, test_df = self.get_train_test_data()
            profile.calculate(train_df,test_df)
            report = json.loads(profile.json())
            logging.info("report created")

            report_file_path = self.data_validation_config.report_file_path

            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)
            logging.info("report path exists is ok")
            with open(report_file_path,"w") as rp:
                json.dump(report, rp, indent=6)
            logging.info("report is saved ok")
            return report
        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            logging.info("save data drift report page started:")
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_train_test_data()
            dashboard.calculate(train_df,test_df)
            dashboard.save(self.data_validation_config.report_page_file_path)
            logging.info("save data drift report page completed:")
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info(f"data validation pipeline started")
            self.get_train_test_data()
            ans = self.check_train_test_dir_exist()
            schme_stutes=self.schema_validation()
            self.save_data_drift_report()
            self.save_data_drift_report_page()
            logging.info(f"data validation piepline completed")
            data_validation_artifact=DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path,
                                                            report_file_path=self.data_validation_config.report_file_path,
                                                            report_file_page_path=self.data_validation_config.report_page_file_path,
                                                            is_validated=schme_stutes,
                                                            message="Data vlidated")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def __del__(self):
        logging.info(f"{'>>'*50}Data Validation log completed.{'<<'*50} \n\n")

