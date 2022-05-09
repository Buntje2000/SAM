import os
import time
from app.classes.services.dicom_reception import DicomReception
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta


def start(path):
    # Get Dicom
    dicomFile = DicomReception.get_dicom(path)
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Meta
    start_time = time.time()
    metaFields = SearchInMeta.search_for_patient_info(
        dicomFile, patientInfo)
    cleanMeta = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicomFile)

    isExist = os.path.exists("anonimyzed")
    if not isExist:
        os.makedirs("anonimyzed")
        print("--- Map '/anonymized' aangemaakt ---")

    # Opslaan DICOM bestand
    fileName = dicomFile.filename.replace(".dcm", "")
    cleanMeta.save_as("anonimyzed/" + fileName + "_anonimizedMeta" + ".dcm")

    # Logging
    print("")
    print("                LOOPTIJDEN")
    print("--- Looptijd meta-pipeline: %s seconden ---" %
          round(time.time() - start_time, 3))
