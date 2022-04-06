from pipelayer import Pipeline

from app.classes.dicom_reception import DicomReception
from app.classes.meta.search_in_meta import SearchInMeta

def startPipeline():
    pipeline = Pipeline([
        DicomReception, # Gives back DICOM file
        SearchInMeta
    ])

    output = pipeline.run()

    print(f"Pipeline Output: {output}")