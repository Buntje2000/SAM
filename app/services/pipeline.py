import time

from pydicom import FileDataset
from app.classes.services.dicom_reception import DicomReception
from app.classes.image.manipulate_pixels import ManipulatePixels
from app.classes.image.pre_process_image import PreProcessImage
from app.classes.image.recognize_text import RecognizeText
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta
from app.classes.image.check_image import CheckImage
import logging


def meta_cleaner(path) -> FileDataset:
    start_time = time.time()

    logging.info("Bestand: " + path)

    # Get Dicom
    dicomFile = DicomReception.get_dicom(path)
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Meta
    metaFields = SearchInMeta.search_for_patient_info(
        dicomFile, patientInfo)
    cleanMeta = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicomFile)

    logging.debug("Looptijd meta-pipeline: %s seconden" %
                  round(time.time() - start_time, 3))

    return cleanMeta


def pixel_cleaner(path, search, profile):
    # Image
    start_time = time.time()

    dicomFile = DicomReception.get_dicom(path)
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    image = PreProcessImage.image_to_array(dicomFile)
    processed_image = PreProcessImage.pre_process_image(image)
    coordinates = RecognizeText.recognize_text(
        processed_image, patientInfo, image, search, profile, dicomFile)

    # print(coordinates)

    # ManipulatePixels.save_image(recognized, cleanMeta)
    logging.debug("Looptijd image-pipeline: %s seconden" %
                  round(time.time() - start_time, 3))
