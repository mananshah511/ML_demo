from collections import namedtuple

DataIgenstionArtifact = namedtuple("DataIgenstionArtifact",
                                   ["traine_file_path","test_file__path","is_igested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["schema_file_path","report_file_path","report_file_page_path","is_validated","message"])

DataTranformArtifact = namedtuple("DataTranformArtifact",
                                  ["transformed_train_file_path","transformed_test_file_path","preprocessed_object_file_path",
                                   "is_transformed","message"])

