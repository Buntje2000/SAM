import random
from app.classes.services.dicom_reception import DicomReception
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.search_in_meta import SearchInMeta
from app.services.generate_dicom import generate_file_with_specifics
from tests.helper import Helper

_helper = Helper()
_patient = _helper.create_fake_patient()

generate_file_with_specifics("unitTestDicom.dcm", _patient)

_dicom = DicomReception.get_dicom("unitTestDicom.dcm")
patientInfo = PatientInfoExtraction.get_patient_info(_dicom)
foundFields = SearchInMeta.search_for_patient_info(
    _dicom, patientInfo)


def test_search_in_meta():
    for x in foundFields:
        if str(x[0]) == '(0010, 0010)':
            assert x[1] == _patient.patient_name
        elif str(x[0]) == '(0010, 0020)':
            assert x[1] == _patient.patient_id
