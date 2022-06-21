import random
from app.classes.services.dicom_reception import DicomReception
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.search_in_meta import SearchInMeta
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.services.generate_dicom import generate_file_with_specifics
from tests.helper import Helper

_helper = Helper()
_patient = _helper.create_fake_patient()
_replacement = str(random.randint(100, 999999))


generate_file_with_specifics("unitTestDicom.dcm", _patient)

_dicom = DicomReception.get_dicom("unitTestDicom.dcm")
patientInfo = PatientInfoExtraction.get_patient_info(_dicom)
metaFields = SearchInMeta.search_for_patient_info(
    _dicom, patientInfo)


def test_manipulate_meta():
    dicom = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, _dicom, replacement=_replacement)
    foundPatientInfo = SearchInMeta.search_for_patient_info(
        _dicom, patientInfo)

    assert dicom.PatientName == _replacement
    assert foundPatientInfo == []
