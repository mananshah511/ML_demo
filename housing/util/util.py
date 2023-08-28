import yaml
from housing.exception import HousingException
import os
import sys

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as config_yaml:
            return yaml.safe_load(config_yaml)
    except Exception as e:
        raise HousingException(e,sys) from e