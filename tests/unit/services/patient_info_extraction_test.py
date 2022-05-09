from app.classes.services.dicom_reception import DicomReception
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.services.generate_dicom import generate_file_with_specifics
from tests.helper import Helper

_helper = Helper()
_patient = _helper.create_fake_patient()

generate_file_with_specifics("unitTestDicom.dcm", _patient)

_dicom = DicomReception.get_dicom("unitTestDicom.dcm")
patientInfo = PatientInfoExtraction.get_patient_info(_dicom)


def test_patient_info():
    assert patientInfo.patient_name == _patient.patient_name
    assert patientInfo.patient_id == _patient.patient_id
    assert patientInfo.patient_dob == None
