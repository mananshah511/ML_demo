from collections import namedtuple

DataIgenstionArtifact = namedtuple("DataIgenstionArtifact",
                                   ["traine_file_path","test_file__path","is_igested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["schema_file_path","report_file_path","report_file_page_path","is_validated","message"])