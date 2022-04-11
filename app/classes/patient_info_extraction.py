from pipelayer import Filter
from app.models.patient_model import PatientModel


class PatientInfoExtraction(Filter):
    def run(self, dicom):

        _patientInfo = self.get_patient_info(dicom)

        return _patientInfo

    def get_patient_info(self, data) -> PatientModel:

        dicom = data

        return PatientModel(
            patient_name=dicom.PatientName,
            patient_id=dicom.PatientID,
            patient_dob=dicom.PatientBirthDate
        )
