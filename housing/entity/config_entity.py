from collections import namedtuple

DataIngetionConfig = namedtuple("DataIngetionConfig",
["dataset_download_url","tgz_download_url","raw_data_dir","ingested_train_dir","ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig",["schmea_file_path"])

DataTranformationConfig = namedtuple("DataTranformationConfig" , ["add_bedroom_per_room","transfored_train-dir"
"transformed_test_dir","preprocessed_object_file_path"])

ModelTrainerConfig = namedtuple("ModelTrainerConfig",["trained_model_file_path","base_accuracy"])

ModelEvalutionConfig = namedtuple("ModelEvulationConfig",["model_evulation_file_path","time_stamp"])

ModelPusherConfig = namedtuple("ModelPusherConfig",["export_dir_path"]) 

