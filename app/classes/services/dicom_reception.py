import logging
from pydicom import FileDataset, dcmread


class DicomReception:
    def get_dicom(file) -> FileDataset:
        '''
        Deze functie ontvangt een dicom-bestand van een bepaald pad en retourneert een FileDataset.
        Als de opgegeven variabele al een FileDataset is, stuurt hij die door.
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
