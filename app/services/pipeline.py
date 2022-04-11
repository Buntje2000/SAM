from pipelayer import Pipeline

from app.classes.dicom_reception import DicomReception
from app.classes.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta


def startPipeline():
    dicomFile = DicomReception.get_dicom(path="testDicom.dcm")
    metaPipeline(dicomFile)


def metaPipeline(data):
    meta_pipeline = Pipeline([
        PatientInfoExtraction.run(data),
        SearchInMeta,
        ManipulateMeta
    ])
