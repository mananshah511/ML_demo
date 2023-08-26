from setuptools import setup
from typing import List

def get_requirements_list()->List[str]:
    pass

PORJECT_NAME="housing-prediction"
VERSION="0.0.1"
AUTHOR="Manan Shah"
DESCRIPTION="This is project to predict housing prices"
PACKAGES=["housing"]
REQUIREMENT_FILE_NAME="requirements.txt"

def get_requirements_list()->List[str]:
    """
    Function is going to return list of requirements mentioned in
    requirements.txt file
    return type is str
    """
    with open(REQUIREMENT_FILE_NAME) as requiremnets_file:
        return requiremnets_file.readlines()
setup(
name=PORJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESCRIPTION,
packages=PACKAGES,
install_requires=get_requirements_list()
)

