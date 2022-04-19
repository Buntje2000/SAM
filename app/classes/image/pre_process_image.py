from pydicom import FileDataset
from PIL import Image
import numpy as np
from turtle import width
import cv2


class PreProcessImage:
    def image_to_array(dicom: FileDataset):
        new_image = dicom.pixel_array.astype(float)
        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        scaled_image = np.uint8(scaled_image)
        final_image = Image.fromarray(scaled_image)

        image = np.array(final_image)

        return image

    def pre_process_image(image):
        scale_percent = 250  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        image = rgb

        return image
