from collections import namedtuple

DataIgenstionArtifact = namedtuple("DataIgenstionArtifact",
                                   ["traine_file_path","test_file__path","is_igested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["schema_file_path","report_file_path","report_file_page_path","is_validated","message"])

DataTranformArtifact = namedtuple("DataTranformArtifact",
                                  ["transformed_train_file_path","transformed_test_file_path","preprocessed_object_file_path",
                                   "is_transformed","message"])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact",
                                  ["is_trained","message","trained_model_file_path","train_rmse","test_rmse","train_accuracy","test_accuracy","model_accyracy"]
                                  )

ModelEvulationArtifact = namedtuple("ModelEvulationArtifact",["is_model_accepted", "evaluated_model_path"])

ModelPusherArtifact = namedtuple("ModelPusherArtifact", ["export_dir_path"])

