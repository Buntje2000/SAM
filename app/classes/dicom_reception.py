from pipelayer import Filter
from pydicom import dcmread

class DicomReception(Filter):
    def run(self, data, context):
        dicom = dcmread('testDicom.dcm')

        return dicom