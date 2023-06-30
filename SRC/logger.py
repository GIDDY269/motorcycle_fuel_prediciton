import logging
import os
from datetime import datetime

# create logging directory
LOG_FILE = ' {}.log'.format(datetime.now().strftime('%m_%d_%Y_%H_%M_%S'))
log_path = os.path.join(os.getcwd(),'log')

try:
    os.makedirs(log_path)

except FileExistsError:
    pass

LOG_FILE_PATH =  os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    filename= LOG_FILE_PATH,
    format=  '[ %(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level= logging.INFO

)

if __name__ == '__main__' :
    logging.info('Logging has started')

