from multiprocessing.connection import wait
from app.classes.dicom_reception import DicomReception
from app.classes.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta


def start():
    # Get Dicom
    dicomFile = DicomReception.get_dicom("testDicom2.dcm")
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Meta
    metaFields = SearchInMeta.search_for_patient_info(
        dicomFile, patientInfo)
    print(metaFields)
    cleanMeta = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicomFile)
    cleanMeta.save_as("testDicomAnonimyzed.dcm")

    # Image
