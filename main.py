import argparse
import logging.config
import time

from app.services.pipeline import start

logging.config.fileConfig('logging.conf')

logger = logging.getLogger('file')


start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input DICOM file to be anonimyzed")
ap.add_argument("-s", "--search", required=False,
                help="search in image")
args = vars(ap.parse_args())

# Start pipeline
start(args["image"], args["search"])

logger.info("--- Looptijd: %s seconden ---\n" %
             round(time.time() - start_time, 3))
