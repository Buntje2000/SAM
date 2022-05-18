import argparse
import logging
import time

from app.services.pipeline import start

logging.basicConfig(filename='logging.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input DICOM file to be anonimyzed")
ap.add_argument("-s", "--search", required=False,
                help="search in image")
args = vars(ap.parse_args())

# Start pipeline
start(args["image"], args["search"])

logging.info("--- Looptijd: %s seconden ---" %
             round(time.time() - start_time, 3))
