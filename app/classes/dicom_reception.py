from datetime import datetime
from pydicom import dcmread


class DicomReception:
    def get_dicom(path):
        dicomFile = dcmread(path)

        if dicomFile.file_meta.TransferSyntaxUID.is_compressed is True:
            dicomFile.decompress()

        return dicomFile
