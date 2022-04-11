from pipelayer import Pipeline

from app.classes.dicom_reception import DicomReception
from app.classes.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta

def startPipeline():
    pipeline = Pipeline([
        DicomReception, # Gives back DICOM file
        PatientInfoExtraction,
        SearchInMeta,
        ManipulateMeta
    ])

    output = pipeline.run()

    print(f"Pipeline Output: {output}")