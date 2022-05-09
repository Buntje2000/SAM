from pydicom import FileDataset
from app.models.patient_model import PatientModel


class PatientInfoExtraction:
    def get_patient_info(dicomFile: FileDataset) -> PatientModel:

        dicom = dicomFile

        if(dicom.PatientBirthDate != ''):
            dob = dicom.dicom[0x0010, 0x0030].value
        else:
            dob = None

        return PatientModel(
            patient_name=dicom[0x0010, 0x0010].value,
            patient_id=dicom[0x0010, 0x0020].value,
            patient_dob=dob
        )
