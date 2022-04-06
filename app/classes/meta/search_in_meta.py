from pipelayer import Filter
from pydicom import dcmread
from app.models.patient_model import PatientModel

class SearchInMeta(Filter):
    def run(self, data, context):
        
        _patientInfo = self.get_patient_info(data)
        _patientInfo.patient_name

        dicom = data

        return _patientInfo

    def get_patient_info(self, data) -> PatientModel:

        dicom = dcmread(data)

        return PatientModel(
            patient_name = dicom.PatientName,
            patient_id = dicom.PatientID
        )