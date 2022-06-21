import argparse
from app.services.pipelines import meta_cleaner, pixel_search, pixel_cleaner


ap = argparse.ArgumentParser()
ap.add_argument("-a", "--action", required=True,
                default="m", help="which pipeline should be runned")
ap.add_argument("-i", "--image", required=True,
                help="path to input DICOM file to be anonimyzed")
ap.add_argument("-s", "--search", required=False,
                help="keyword to search for in image")
ap.add_argument("-p", "--profile", required=False,
                help="low/medium/high profile of anonymization")
ap.add_argument("-r", "--replacement", required=False,
                help="pseudonym for patiënt data")
args = vars(ap.parse_args())

# Start pipelines
action = args["action"]

if action == "m":
    meta_cleaner(args["image"], args["replacement"])
elif action == "ps":
    pixel_search(args["image"], args["search"], args["profile"])
elif action == "pc":
    pixel_cleaner(args["image"], args["search"], args["profile"])
