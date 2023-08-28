import os
from datetime import datetime

def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

ROOT_DIR=os.getcwd()
CONFIG_DIR="config"
CONFIG_FILE_NAME="config.yaml"
CONFIG_PATH_NAME=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

CURRENT_TIME_STAMP=get_current_time_stamp()

#Training pipeline related variables

TRAINING_PIPELINE_CONFIG_KEY="training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY="artifact_dir"
TRAINING_PIPELINE_NAME_KEY="pipeline_name"


#Data igenstion related variables

DATA_IGENSTION_CONFIG_KEY="data_ingestion_config"
DATA_IGENSTION_ARTIFACT_DIR_KEY="data_ingestion"
DATA_IGENSTION_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_IGENSTION_RAW_DATASET_DOWNLOAD_DIR_KEY="raw_data_dir"
DATA_IGENSTION_TGT_DOWNLOAD_DIR_KEY="tgz_download_dir"
DATA_IGENSTION_IGNESTED_DIR_KEY="ingested_dir"
DATA_IGENSTION_IGNESTED_TRAIN_DIR_KEY="ingested_train_dir"
DATA_IGENSTION_IGNESTED_TEST_DIR_KEY="ingested_test_dir"

#Data validation realted variables

DATA_VALIDATION_CONFIG_KEY="data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR_KEY="data_validation"
DATA_VALIDATION_SCHEMA_DIR_KEY="schema_dir"
DATA_VALIDATION_SCHEMA_FILENAME_KEY="schema_file_name"
DATA_VALIDATION_REPORT_FILE_DIR_KEY="report_file_name"
DATA_VALIDATION_REPORT_FILE_PAGE_DIR_KEY="report_page_file_name"