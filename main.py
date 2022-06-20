import argparse
import logging.config
import time
from app.services.pipelines import meta_cleaner, pixel_search, pixel_cleaner

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('file')


start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input DICOM file to be anonimyzed")
ap.add_argument("-s", "--search", required=False)
ap.add_argument("-p", "--profile", required=False)
ap.add_argument("-r", "--replacement", required=False)
args = vars(ap.parse_args())

# Start pipelines
meta_cleaner(args["image"], args["replacement"])
# pixel_search(args["image"], args["search"], args["profile"])
# pixel_cleaner(args["image"], args["search"], args["profile"])

logger.info("Looptijd totaal: %s seconden\n" %
            round(time.time() - start_time, 3))
