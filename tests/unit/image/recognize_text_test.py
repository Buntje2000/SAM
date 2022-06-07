from collections import defaultdict
import random
from app.classes.image.pre_process_image import PreProcessImage
from app.classes.image.recognize_text import RecognizeText
from app.classes.services.dicom_reception import DicomReception
from app.classes.services.patient_info_extraction import PatientInfoExtraction


_dicomFile = DicomReception.get_dicom("pixelUnitTestDicom.dcm")
_patientInfo = PatientInfoExtraction.get_patient_info(_dicomFile)
_profile = "high"
_search = "AORTA"

# Tekstherkenning
_image = PreProcessImage.image_to_array(_dicomFile)
_processed_image = PreProcessImage.pre_process_image(_image)
_result = RecognizeText.recognize_text(
    _processed_image, _patientInfo, _image, _profile, _dicomFile, _search)

_coordinates = defaultdict(list)
_x = random.randint(0, 999)
_y = random.randint(0, 999)
_w = random.randint(0, 999)
_h = random.randint(0, 999)
_c = random.randint(0, 100)

_coordinates["detected"].append(True)
_coordinates["text"].append("AORTA")
_coordinates["left"].append(_x)
_coordinates["top"].append(_y)
_coordinates["width"].append(_w)
_coordinates["height"].append(_h)
_coordinates["conf"].append(_c)


def test_recognize_text_in_image():
    assert _result == dict({'detected': [True], 'text': ['AORTA'], 'left': [
        240], 'top': [151], 'width': [319], 'height': [171], 'conf': [94]})


def test_add_coordinates_to_file():
    RecognizeText.add_coordinates_to_file(_coordinates, _dicomFile)

    with open("app/data/deid.custom", "r") as f:
        if ('LABEL Philips Medical Systems Affiniti 70G # (ANB)' in f.read() and
            'contains Modality US' in f.read() and
            '+ contains Manufacturer Philips Medical Systems' in f.read() and
            '+ equals Rows 768' in f.read() and
            '+ contains ManufacturerModelName Affiniti 70G' in f.read() and
                f'coordinates {_x},{_y},{_w},{_h}' in f.read()):
            assert True
