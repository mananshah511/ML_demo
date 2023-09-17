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

#Data transformation related variables

DATA_TRANSFORMATION_CONFIG_KEY="data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR_KEY="data_tranformation"
DATA_TRANSFORMATION_ADD_BEDROOM_KEY="add_bedroom_per_room"
DATA_TRANSFORMATION_TRANSFORMATION_DIR_KEY="transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_KEY="transformed_train_dir"
DATA_TRANSFORMATION_TEST_DIR_KEY="transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY="preprocessing_dir"
DATA_TRANSFORMATION_OBJECT_FILENAME="preprocessed_object_file_name"



COLUMN_TOTAL_ROOMS = "total_rooms"
COLUMN_POPULATION = "population"
COLUMN_HOUSEHOLDS = "households"
COLUMN_TOTAL_BEDROOM = "total_bedrooms"
DATASET_SCHEMA_COLUMNS_KEY=  "columns"

NUMERICAL_COLUMN_KEY="numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"


TARGET_COLUMN_KEY="target_column"

#model training related variables

MODEL_TRAINER_CONFIG_KEY="model_trainer_config"
MODEL_TRAINER_ARTIFACT_DIR="model_trainer"
MODEL_TRAINER_ARTIFACT_TRAINED_MODEL_DIR_KEY="trained_model_dir"
MODEL_TRAINER_MODEL_FILE_NAME_KEY="model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY="base_accuracy"
MODEL_TRAINER_CONFIG_DIR_KEY="model_config_dir"
MODEL_TRAINER_CONFIG_FILENAME_KEY="model_config_file_name"


#model evulation realetd variables

MODEL_EVULATiON_CONFIG_KEY="model_evaluation_config"
MODEL_EVULATION_ARTIFACT_DIR="model_evulation"
MODEL_EVULATION_FILE_NAME="model_evaluation_file_name"



BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"
