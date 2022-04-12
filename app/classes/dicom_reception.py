from pydicom import dcmread


class DicomReception:
    def get_dicom(path):
        dicomFile = dcmread(path)

        return dicomFile
