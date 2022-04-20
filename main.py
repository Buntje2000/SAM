import logging
import time

from app.services.pipeline import start

logging.basicConfig(filename='logging.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

start_time = time.time()

# Start pipeline
start()

logging.info("--- Looptijd: %s seconden ---" % round(time.time() - start_time, 3))
