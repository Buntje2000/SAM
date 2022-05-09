from PIL import Image
import io
import numpy as np
from pydicom import FileDataset
import cv2
from pydicom.encaps import encapsulate


class ManipulatePixels:
    def manipulate_pixels(image, ds: FileDataset):
        print("test")
