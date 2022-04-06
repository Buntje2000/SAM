from pydantic import BaseModel
from pydicom import dataset

class DicomModel(BaseModel):
    dicom: dataset