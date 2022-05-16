import argparse
import time
from app.services.pipeline import meta_cleaner, pixel_cleaner


start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input DICOM file to be anonimyzed")
ap.add_argument("-s", "--search", required=False)
ap.add_argument("-p", "--profile", required=True)
args = vars(ap.parse_args())

# Start pipeline
# meta_cleaner(args["image"])
pixel_cleaner(args["image"], args["search"], args["profile"])

# Logging
print("--- Looptijd: %s seconden ---" % round(time.time() - start_time, 3))
