import logging
from deid.dicom import DicomCleaner, get_files
from app.config import config

logger = logging.getLogger('file')


class ManipulatePixels:
    def manipulate_pixels(tmpDir):

        dicom_file = list(get_files(tmpDir))[0]

        dir = None
        try:
            # Output folder
            dir = config("PIXEL", "output_folder")
        except Exception as e:
            logger.warning(e)

        if dir == None:
            dir = 'output'
            logger.warning(
                "Pixel threshold is niet goed ingesteld. Standaard map wordt gebruikt (output). Controleer config.ini")

        outputDir = dir

        deidFiles = ['dicom', 'app/data/deid.custom']
        client = DicomCleaner(output_folder=outputDir,
                              deid=deidFiles)
        client.detect(dicom_file)
        client.clean()
        client.save_dicom()

        logger.info(
            f"Afbeelding schoongemaakt en opgeslagen in de map '{outputDir}'")
