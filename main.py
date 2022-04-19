import logging
import time

from app.services.pipeline import start

logging.basicConfig(filename='test.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

start_time = time.time()

# Start pipeline
start()

logging.info("--- Looptijd: %s seconden ---" % round(time.time() - start_time, 3))
