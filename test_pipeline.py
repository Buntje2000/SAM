from app.classes.dicom_reception import DicomReception
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta
from app.classes.patient_info_extraction import PatientInfoExtraction
from app.services.generate_dicom import generate_file_with_specifics

generate_file_with_specifics("unitTestDicom.dcm")

dicom = DicomReception.get_dicom("unitTestDicom.dcm")
patientInfo = PatientInfoExtraction.get_patient_info(dicom)
metaFields = SearchInMeta.search_for_patient_info(
    dicom, patientInfo)


def test_dicom_reader():
    assert dicom.SpecificCharacterSet == "ISO_IR 100"
    assert dicom.PatientSex == "M"
    assert dicom.PatientName == "Smith^Harry"
    assert dicom.PatientID == "138920"
    assert dicom.PatientIdentityRemoved == 'NO'


def test_patient_info():
    assert patientInfo.patient_name == "Smith^Harry"
    assert patientInfo.patient_id == "138920"


def test_search_in_meta():
    assert metaFields[0][1] == '**name**'
    assert metaFields[1][1] == '**id**'


def test_manipulate_meta():
    ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicom)
    foundPatientInfo = SearchInMeta.search_for_patient_info(
        dicom, patientInfo)

    assert foundPatientInfo == []
