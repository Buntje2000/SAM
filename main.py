import argparse
import time
from app.services.pipeline import start


start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input DICOM file to be anonimyzed")
args = vars(ap.parse_args())

# Start pipeline
start(args["image"])

print("--- Looptijd: %s seconden ---" % round(time.time() - start_time, 3))
