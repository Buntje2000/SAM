from pydicom import FileDataset
from app.models.patient_model import PatientModel
import logging


logger = logging.getLogger('file')


class PatientInfoExtraction:
    def get_patient_info(dicomFile: FileDataset) -> PatientModel:

        dicom = dicomFile

        if "PatientBirthDate" in dicom:
            if(dicom.PatientBirthDate != ''):
                dob = dicom[0x0010, 0x0030].value
            else:
                dob = None
        else:
            dob = None

        try:
            patientModel = PatientModel(
                patient_name=dicom[0x0010, 0x0010].value,
                patient_id=dicom[0x0010, 0x0020].value,
                patient_dob=dob
            )
        except:
            logger.fatal("PatientModel kon niet worden gevuld!")

        logger.debug("PatientModel gevuld")
        return patientModel
