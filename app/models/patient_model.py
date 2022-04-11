from typing import Any, Optional
from pydantic import BaseModel

class PatientModel(BaseModel):
    patient_name: Any
    patient_id: Any
    patient_dob: Optional[Any]