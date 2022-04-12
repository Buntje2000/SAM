from datetime import datetime
from pydicom import dcmread


class DicomReception:
    def get_dicom(path):
        dicomFile = dcmread(path)
        # print("---", datetime.now(), "DICOM bestand gelezen ---")

        return dicomFile
