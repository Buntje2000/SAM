import logging
from pydicom import FileDataset, dcmread


class DicomReception:
    def get_dicom(file) -> FileDataset:
        '''
        This function receives a dicom file from a certain path and returns a FileDataset.
        If the given variable is already a FileDataset, it just sends that through.
        '''
        try:
            if isinstance(file, FileDataset):
                dicomFile = file
            elif isinstance(file, str):
                dicomFile = dcmread(file)
                logging.info("Bestand: " + file)
        except Exception as e:
            logging.fatal(e)

        logging.debug('Bestand ontvangen')
        return dicomFile
