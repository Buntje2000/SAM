import logging
from datetime import datetime
from pydicom import dcmread


class DicomReception:
    def get_dicom(path):
        dicomFile = dcmread(path)

        logging.info('file is succesfully received')
        return dicomFile
