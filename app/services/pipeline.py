from app.classes.dicom_reception import DicomReception
from app.classes.image.manipulate_pixels import ManipulatePixels
from app.classes.image.pre_process_image import PreProcessImage
from app.classes.image.recognize_text import RecognizeText
from app.classes.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta


def start():
    # Get Dicom
    dicomFile = DicomReception.get_dicom("testDicom.dcm")
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Meta
    metaFields = SearchInMeta.search_for_patient_info(
        dicomFile, patientInfo)
    print(metaFields)
    cleanMeta = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicomFile)
    cleanMeta.save_as("testDicomAnonimyzed.dcm")

    # Image
    image = PreProcessImage.image_to_array(dicomFile)
    processed_image = PreProcessImage.pre_process_image(image)
    recognized = RecognizeText.recognize_text(
        processed_image, patientInfo, image)
    ManipulatePixels.manipulate_pixels(recognized, cleanMeta)
