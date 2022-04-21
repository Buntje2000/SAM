from app.classes.dicom_reception import DicomReception
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta
from app.classes.patient_info_extraction import PatientInfoExtraction
from app.services.generate_dicom import generate_file_with_specifics
from tests.helper import Helper


class TestPipeline:

    _helper = Helper()
    _patient = _helper.create_patient()

    generate_file_with_specifics("unitTestDicom.dcm", _patient)

    _dicom = DicomReception.get_dicom("unitTestDicom.dcm")
    patientInfo = PatientInfoExtraction.get_patient_info(_dicom)
    metaFields = SearchInMeta.search_for_patient_info(
        _dicom, patientInfo)

    def test_dicom_reader(self):
        assert self._dicom.PatientName == self._patient.patient_name
        assert self._dicom.PatientID == self._patient.patient_id

    def test_patient_info(self):
        assert self.patientInfo.patient_name == self._patient.patient_name
        assert self.patientInfo.patient_id == self._patient.patient_id
        assert self.patientInfo.patient_dob == None

    def test_search_in_meta(self):
        print(self._patient.patient_id)
        print(self.metaFields)

        for x in self.metaFields:
            if str(x[0]) == '(0010, 0010)':
                assert x[1] == '**name**'
            elif str(x[0]) == '(0010, 0020)':
                assert x[1] == '**id**'

    def test_manipulate_meta(self):
        ManipulateMeta.delete_patient_info_from_meta(
            self.metaFields, self._dicom)
        foundPatientInfo = SearchInMeta.search_for_patient_info(
            self._dicom, self.patientInfo)

        assert foundPatientInfo == []
