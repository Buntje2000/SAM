from dicomgenerator.exporter import export
from dicomgenerator.factory import CTDatasetFactory
from app.models.patient_model import PatientModel


def generate_file_with_specifics(output_path, patient: PatientModel):
    """Generate a dicom file, set specific tags. All tags supported by pydicom
    can be set here"""

    export(dataset=CTDatasetFactory(
        PatientName=patient.patient_name,
        PatientID=patient.patient_id,
        PatientComments=patient.patient_name+patient.patient_id),
        path=output_path)
