import os
from deid.dicom import get_files, has_burned_pixels
import logging

logger = logging.getLogger('file')


class CheckImage:
    def check_image_for_known_burnedinpixels(tmpDir):
        # dataset = get_dataset('tmp')
        # print("Dataset:", dataset)
        dicom_file = list(get_files(tmpDir))[0]
        print("Dicom file:", dicom_file)

        outputDir = 'output'
        if not os.path.isdir(outputDir):
            try:
                os.mkdir(outputDir)
            except OSError:
                print("Creation of the directory %s failed" % outputDir)
            else:
                print("Successfully created the directory %s " % outputDir)

        deidFiles = ['dicom', 'app/data/deid.custom']
        results = has_burned_pixels(
            dicom_files=dicom_file, deid=deidFiles)

        return results
