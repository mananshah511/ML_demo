from housing.pipeline.pipeline import Pipeline
from housing.config.configuration import Configuration
from housing.config.configuration import DataTransformationConfig
import os
def main():
    pipeline = Pipeline()
    pipeline.run_pipeline()

if __name__=="__main__":
    main()
