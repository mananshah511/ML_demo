import yaml
from housing.exception import HousingException
import os
import sys
import numpy as np
import pandas as pd
import dill

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as config_yaml:
            return yaml.safe_load(config_yaml)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def load_numpy_array(file_path:str)-> np.array:
    try:
        with open(file_path,"rb") as np_file:
            return np.load(np_file)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def load_object(file_path:str):
    try:
        with open(file_path,"rb") as object_file:
            return dill.load(object_file)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def save_object(file_path:str, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as object_file:
            dill.dump(obj, object_file)
    except Exception as e:
        raise HousingException(e,sys) from e       