from dicomgenerator.exporter import export
from dicomgenerator.factory import CTDatasetFactory


def generate_file_with_specifics(output_path):
    """Generate a dicom file, set specific tags. All tags supported by pydicom
    can be set here"""
    export(dataset=CTDatasetFactory(
        SpecificCharacterSet="ISO_IR 100",
        PatientSex='M',
        PatientName='Smith^Harry',
        PatientID='138920',
        PatientIdentityRemoved='NO'),
        path=output_path)
