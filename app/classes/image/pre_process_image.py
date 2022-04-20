from pydicom.pixel_data_handlers.util import apply_voi_lut
import pydicom
from pydicom import FileDataset
import pydicom.pixel_data_handlers as pdh
from PIL import Image
import numpy as np
from turtle import width
import cv2
import matplotlib.pyplot as plt


class PreProcessImage:
    def image_to_array(dicom: FileDataset):

        new_image = dicom.pixel_array

        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        scaled_image = np.uint8(scaled_image)
        final_image = Image.fromarray(scaled_image)
        # ds = pdh.util.convert_color_space(
        #     new_image, current='RGB', desired='YBR_FULL')

        gray = cv2.cvtColor(scaled_image, cv2.COLOR_RGB2GRAY)
        gray, img_bin = cv2.threshold(
            gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gray = cv2.bitwise_not(img_bin)
        # cv2.imshow("Image", gray)
        # cv2.waitKey(0)

        # final_image.show()

        image = np.array(gray)

        return image

    def pre_process_image(image):
        scale_percent = 250  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        processed_image = rgb

        return processed_image
