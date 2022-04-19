import numpy as np
from pydicom import FileDataset
import pydicom.encaps


class ManipulatePixels:
    def manipulate_pixels(image, ds: FileDataset):
        np_image = image
        ds.PhotometricInterpretation = "MONOCHROME1"
        ds.SamplesPerPixel = 1
        ds.BitsStored = 8
        ds.BitsAllocated = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.PixelData = np_image.tobytes()
        ds.save_as('result_gray.dcm')
