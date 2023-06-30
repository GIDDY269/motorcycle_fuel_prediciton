import os
import sys
sys.path.append('C:/Users/user/motorcycle_fuel_consumption')
import pandas as pd
import numpy as np
from dataclasses import dataclass
from SRC.logger import logging
from SRC.exception import CustomException



@dataclass
class DATA_TRANSFORMATION_CONFIG:
    transformed_data_path = os.path.join('artifacts','cleaned_data.csv')

class DATA_TRANSFORMATION:
    def __init__(self):

        self.data_transformation_config = DATA_TRANSFORMATION_CONFIG()

    def initiate_data_transformation(self,filepath):
        logging.info('Initiating data transformation')

        # reading ingested data

        ingested_data = pd.read_csv(filepath) # reads ingested csv file




