import logging
from random import randint
import os


logging.basicConfig(
    filename=os.getenv('LOG_PATH', '/var/log/monitor/temp.log'), 
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


if __name__ == '__main__':
    logging.info(f'{randint(0,1000) / 10}\'C')