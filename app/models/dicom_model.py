from pydantic import BaseModel
from pydicom import FileDataset

class DicomModel(BaseModel):
    dicom: FileDataset