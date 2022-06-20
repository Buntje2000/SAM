from pydicom import FileDataset
import numpy as np
import cv2
import logging

logger = logging.getLogger('file')


class PreProcessImage:
    def image_to_array(dicom: FileDataset):
        if dicom.file_meta.TransferSyntaxUID.is_compressed is True:
            dicom.decompress()

        new_image = dicom.pixel_array

        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        scaled_image = np.uint8(scaled_image)

        image = np.array(scaled_image)

        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

        return image

    def pre_process_image(image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        gray, img_bin = cv2.threshold(
            gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gray = cv2.bitwise_not(img_bin)

        img_resized = cv2.resize(
            gray, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)

        # kernel = np.ones((1, 1), np.uint8)
        # img = cv2.dilate(img_resized, kernel, iterations=1)
        # img = cv2.erode(img, kernel, iterations=1)

        threshold = cv2.adaptiveThreshold(img_resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)

        binary_img = cv2.bitwise_not(threshold)

        # cv2.imshow("Image", binary_img)
        # cv2.waitKey(0)

        processed_image = threshold

        return processed_image
