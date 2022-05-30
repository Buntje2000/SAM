import pytest
from app.classes.services.dicom_reception import DicomReception
from app.services.generate_dicom import generate_file_with_specifics
from tests.helper import Helper


_helper = Helper()
_patient = _helper.create_fake_patient()
generate_file_with_specifics("unitTestDicom.dcm", _patient)
_dicom = DicomReception.get_dicom("unitTestDicom.dcm")


def test_dicom_reader():
    assert _dicom.PatientName == _patient.patient_name
    assert _dicom.PatientID == _patient.patient_id

    # Read unknown DICOM
    with pytest.raises(Exception):
        assert DicomReception.get_dicom() == None
