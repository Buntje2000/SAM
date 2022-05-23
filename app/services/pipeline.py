import time
from pydicom import FileDataset
from app.classes.services.dicom_reception import DicomReception
from app.classes.image.manipulate_pixels import ManipulatePixels
from app.classes.image.pre_process_image import PreProcessImage
from app.classes.image.recognize_text import RecognizeText
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta
import logging


def meta_cleaner(file) -> FileDataset:
    '''Verwijder persoonsnaam, id & geboortedatum uit alle metavelden'''

    start_time = time.time()

    # Dicom verwerken
    dicomFile = DicomReception.get_dicom(file)
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Meta
    metaFields = SearchInMeta.search_for_patient_info(
        dicomFile, patientInfo)
    cleanMeta = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicomFile)

    logging.debug("Looptijd meta-pipeline: %s seconden" %
                  round(time.time() - start_time, 3))

    return cleanMeta


def pixel_search(file, search, profile) -> dict:
    '''Zoek in de afbeelding naar persoonsnaam & id'''
    # Image
    start_time = time.time()

    # Dicom verwerken
    dicomFile = DicomReception.get_dicom(file)
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Tekstherkenning
    image = PreProcessImage.image_to_array(dicomFile)
    processed_image = PreProcessImage.pre_process_image(image)
    result = RecognizeText.recognize_text(
        processed_image, patientInfo, image, search, profile, dicomFile)

    logging.debug("Looptijd image-pipeline: %s seconden" %
                  round(time.time() - start_time, 3))

    return dict(result)


def pixel_cleaner(path, search, profile):
    '''
    Verwijder persoonsnaam & id uit de afbeelding. Heeft pad en profiel nodig. 
    Slaat schone afbeelding op in map. Zie config.ini -> output_folder.
    '''
    start_time = time.time()

    # Dicom verwerken
    dicomFile = DicomReception.get_dicom(path)
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Tekstherkenning
    image = PreProcessImage.image_to_array(dicomFile)
    processed_image = PreProcessImage.pre_process_image(image)
    coordinates = RecognizeText.recognize_text(
        processed_image, patientInfo, image, search, profile, dicomFile)

    # Pixels schoonmaken
    RecognizeText.add_coordinates_to_file(
        coordinates=coordinates, dicomFile=dicomFile)
    ManipulatePixels.manipulate_pixels(path)

    logging.debug("Looptijd imagecleaner-pipeline: %s seconden" %
                  round(time.time() - start_time, 3))
