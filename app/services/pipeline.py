import time
from app.classes.services.dicom_reception import DicomReception
from app.classes.image.manipulate_pixels import ManipulatePixels
from app.classes.image.pre_process_image import PreProcessImage
from app.classes.image.recognize_text import RecognizeText
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta
from app.classes.image.check_image import CheckImage
import os
import shutil


def start(path, search):
    # Get Dicom
    dicomFile = DicomReception.get_dicom(path)
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    tmpDir = 'tmp'
    if not os.path.isdir(tmpDir):
        try:
            os.mkdir(tmpDir)
        except OSError:
            print("Creation of the directory %s failed" % tmpDir)
        else:
            print("Successfully created the directory %s " % tmpDir)

    # Meta
    start_time = time.time()
    metaFields = SearchInMeta.search_for_patient_info(
        dicomFile, patientInfo)
    cleanMeta = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicomFile)
    dicomFileName = os.path.basename(dicomFile.filename)
    cleanMeta.save_as("tmp/" + dicomFileName)

    print("Saved image", dicomFileName, "in folder", tmpDir)
    print("--- Looptijd meta-pipeline: %s seconden ---" %
          round(time.time() - start_time, 3))

    # Image
    start_time = time.time()

    detectionData = CheckImage.check_image_for_known_burnedinpixels(
        tmpDir, dicomFile)

    hasKnownBurnedInPixels: bool = list(detectionData.items())[0][1]
    if not hasKnownBurnedInPixels or 'blacklist' in detectionData:
        print("Unknown file")
        image = PreProcessImage.image_to_array(dicomFile)
        processed_image = PreProcessImage.pre_process_image(image)
        coordinates = RecognizeText.recognize_text(
            processed_image, patientInfo, image, search)
        RecognizeText.add_coordinates_to_file(
            coordinates, dicomFile)
        ManipulatePixels.manipulate_pixels(tmpDir)
    else:
        print("Knowm file")
        ManipulatePixels.manipulate_pixels(tmpDir)

    # ManipulatePixels.save_image(recognized, cleanMeta)
    print("--- Looptijd image-pipeline: %s seconden ---" %
          round(time.time() - start_time, 3))

    # Delete all files in tmp directory
    for files in os.listdir(tmpDir):
        path = os.path.join(tmpDir, files)
        try:
            os.remove(path)
        except OSError:
            shutil.rmtree(path)
