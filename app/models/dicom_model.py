from typing import Any
from pydantic import BaseModel

class DicomModel(BaseModel):
    dicom: Any
