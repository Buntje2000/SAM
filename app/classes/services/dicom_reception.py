from pydicom import dcmread


class DicomReception:
    def get_dicom(path):
        '''
        This function receives a dicom file from a certain path and returns a FileDataset
        '''

        dicomFile = dcmread(path)

        return dicomFile
