from collections import namedtuple

DataIgenstionArtifact = namedtuple("DataIgenstionArtifact",
                                   ["traine_file_path","test_file__path","is_igested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["True_or_not"])