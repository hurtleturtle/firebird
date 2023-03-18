import logging
from random import randint

logging.basicConfig(filename='/var/log/monitor/temp.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    logging.info(f'{randint(0,1000) / 10}\'C')