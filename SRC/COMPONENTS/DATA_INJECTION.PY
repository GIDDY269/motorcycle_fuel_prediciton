import os
import sys
sys.path.append('C:/Users/user/motorcycle_fuel_consumption')
import pandas as pd
import numpy as np
from dataclasses import dataclass
import pyodbc
from SRC.logger import logging
from SRC.exception import CustomException
import requests

@dataclass
class DATA_INGESTION_CONFIG:
    data_filepath = os.path.join('artifacts','ingested_data.csv') # file path of the ingested data 

class DATA_INGESTION:
    def __init__(self) :
        self.data_injection = DATA_INGESTION_CONFIG()

    def initiates_data_ingestion(self):
        logging.info('Initiating data ingestion')
        try:
            server_name = os.environ.get('SERVER_NAME')
            database_name = os.environ.get('DATABASE_NAME')
            

            logging.info('Connecting to sql server')

            connection_string = 'Driver={SQL Server};' + f'Server={server_name};Database={database_name};Trusted_Connection=yes;'

            cnxn = pyodbc.connect(connection_string)
            cursor = cnxn.cursor()
            logging.info('Connection successful')
    

            logging.info('Fetching data from RapidAPI')

            url = "https://motorcycles-by-api-ninjas.p.rapidapi.com/v1/motorcycles"

            moto_makes = ['Kawasaki','Harley-Davidson','Hartford','Ducati','Suzuki','Triumph',
                     'Yamaha','Aprilia','KTM','Buell','BMW','Honda','Victory','Piaggio',
                     'Moto Guzzi','Zero','MV Agusta','Hildebrand','AJS','Ariel','BSA','Baotian','Benelli','Chang Jiang','Evoke',
                     'JAWA','Alta','Casal','D-Rad','DKW','Norton','Bajaj','Hero']
            
            offset = [0,31,61,91,121]

            data = []

            for make in moto_makes:
                for num in offset:
                    querystring = {'make':make,'offset':num}

                    headers = {
	                "X-RapidAPI-Key": "d3b44d85f3msh15e2a600cf5f10ep137983jsn115d3b9c9ee2",
	                "X-RapidAPI-Host": "motorcycles-by-api-ninjas.p.rapidapi.com"
                    }

                    response = requests.get(url, headers=headers, params=querystring)

                    response = response.json()
                    data.extend(response)

                    print(response)

            logging.info('Data fetched from API')


            logging.info('Initiating Creating database table')

            column_list = []
            values = []

            for dictionary in data:
                for key,value in dictionary.items():
                    column_list.append(key)
                    values.append(value)
            column_list = set(column_list)

            column_definition = ', '.join([f'{column} varchar(2000)' for column in column_list])

            logging.info(column_definition)
            logging.info(column_list)

            create_table =  f'''
                CREATE TABLE Motorcycle_fuel_consumption (
                Id INT PRIMARY KEY IDENTITY(1,1),
                {column_definition}
                )
                '''
            # Execute the create table query
            cursor.execute(create_table)
            cnxn.commit()
            logging.info('Table created')

            logging.info('Inserting data features')

            # Insert the values into the table
            for dictionary in data:
            # Filter the dictionary keys that match the table columns
                column_names = [column for column in dictionary.keys() if column in column_list]
    
                # Construct the column names and values for the insert query
                columns = ', '.join(column_names)
                values = ', '.join([f"'{dictionary[column]}'" if dictionary[column] is not None else 'NULL' for column in column_names])
    
                # Construct and execute the insert query
                insert_query = f"INSERT INTO Motorcycle_fuel_consumption ({columns}) VALUES ({values})"
                cursor.execute(insert_query)
                cnxn.commit()



            logging.info('Data read into sql database')

            select_query = 'SELECT * FROM Motorcycle_fuel_consumption'
            cursor.execute(select_query)
            data_result = cursor.fetchall() # returns a list of tuples

            logging.info(data_result[0])

            column_desc = [desc[0] for desc in cursor.description] # get the column names

            logging.info(column_desc)

            data = {column: [] for column in column_desc} # creates an empyth dictionary with each column names as keys and a list to store the data

            for tup in data_result:
                for i , value in enumerate(tup):
                    data[column_desc[i]].append(value) # appends the values to the emp[ty dictionary


            dataframe = pd.DataFrame(data)

            #making directories
            os.makedirs('artifacts',exist_ok=True)
            os.makedirs(os.path.dirname(self.data_injection.data_filepath),exist_ok=True)

            dataframe.to_csv(self.data_injection.data_filepath,header=True,index=False)

            logging.info('data ingestion complete')

            return self.data_injection.data_filepath

        except Exception as e :
            raise CustomException(e,sys)
        
if __name__ == '__main__':
    obj = DATA_INGESTION()
    obj.initiates_data_ingestion()

