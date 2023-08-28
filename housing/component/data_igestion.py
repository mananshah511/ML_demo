import os,sys
from housing.exception import HousingException
from housing.entity.artifact_entity import DataIgenstionArtifact
from housing.entity.config_entity import DataIngestionConfig
from housing.logger import logging
import numpy as np
import pandas as pd
import tarfile
from six.moves import urllib
from sklearn.model_selection import StratifiedShuffleSplit


class DataIgenstion:

    def __init__(self,data_igention_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_igention_config=data_igention_config
        except Exception as e:
            raise HousingException(e,sys)

    def download_housing_data(self) ->str:
        try:
            download_data_url=self.data_igention_config.dataset_download_url

            tgz_dir=self.data_igention_config.tgz_download_dir

            os.makedirs(tgz_dir,exist_ok=True)

            housing_file_name=os.path.basename(download_data_url)

            tgz_file_path=os.path.join(tgz_dir,housing_file_name)
            logging.info(f"downloading data from {download_data_url} and in the {tgz_file_path} folder")
            urllib.request.urlretrieve(download_data_url,tgz_file_path)
            logging.info(f"data download completed")


            return tgz_file_path
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def exctract_tgz_file(self,tgz_file_path:str):
        try:
            raw_data_dir=self.data_igention_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)
            logging.info(f"Exctracting {tgz_file_path} into dir {raw_data_dir}")
            with tarfile.open(tgz_file_path) as housing_data:
                housing_data.extractall(path=raw_data_dir)
            logging.info(f"Extcratction completed")

        except Exception as e:
            raise Exception(e,sys) from e
        
    def split_data_as_train_test(self)->DataIgenstionArtifact:
        try:
            raw_data_dir=self.data_igention_config.raw_data_dir

            housing_file_name=os.listdir(raw_data_dir)[0]

            housing_file_path=os.path.join(raw_data_dir,housing_file_name)
            logging.info(f"housing data csv file reading:{housing_file_path}")
        
            housing_dataframe=pd.read_csv(housing_file_path)

            housing_dataframe['income_cat']=pd.cut(housing_dataframe["median_income"],
                                                   bins=[0.0,1.5,3.0,4.5,6.0,np.inf],
                                                   labels=[1,2,3,4,5])
            logging.info("Starting spliiting")

            strat_train_set=None
            strat_test_set=None

            split=StratifiedShuffleSplit(test_size=0.2,random_state=42,n_splits=1)

            for train_index,test_index in split.split(housing_dataframe,housing_dataframe["income_cat"]):
                strat_train_set=housing_dataframe.loc[train_index].drop(["income_cat"],axis=1)
                strat_test_set=housing_dataframe.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path=os.path.join(self.data_igention_config.ingested_train_dir,housing_file_name)
            test_file_path=os.path.join(self.data_igention_config.ingested_test_dir,housing_file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_igention_config.ingested_train_dir,exist_ok=True)
                logging.info(f"exporting training data")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_igention_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting testing data")
                strat_test_set.to_csv(test_file_path,index=False)
            data_igenestion_artifact=DataIgenstionArtifact(traine_file_path=train_file_path,test_file__path=test_file_path,
                                                           is_igested=True,message="data igenstion completed successfully")
            
            return data_igenestion_artifact
        except Exception as e:
            raise Exception(e,sys) from e
        
    def initate_data_igenetion(self)->DataIgenstionArtifact:
            try:
                tgz_file_path=self.download_housing_data()
                self.exctract_tgz_file(tgz_file_path=tgz_file_path)
                return self.split_data_as_train_test()
            except Exception as e:
                raise Exception(e,sys) from e
            
    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")