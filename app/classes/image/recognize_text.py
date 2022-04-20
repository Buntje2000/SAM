from turtle import width
from pytesseract import Output
import pytesseract
import argparse
import cv2
from collections import defaultdict

from app.models.patient_model import PatientModel


class RecognizeText:
    def recognize_text(processed_image, patientInfo: PatientModel, image):
        results = pytesseract.image_to_data(
            processed_image, config='--psm 11 --oem 3', output_type=Output.DICT)

        searchResults = defaultdict(list)

        for i in range(0, len(results["text"])):
            # extract the bounding box coordinates of the text region from
            # the current result
            if str.lower('64') in str.lower(results["text"][i]):
                t = results["text"][i]
                x = results["left"][i]
                y = results["top"][i]
                w = results["width"][i]
                h = results["height"][i]
                c = results["conf"][i]

                searchResults["text"].append(t)
                searchResults["left"].append(x)
                searchResults["top"].append(y)
                searchResults["width"].append(w)
                searchResults["height"].append(h)
                searchResults["conf"].append(c)
                # extract the OCR text itself along with the confidence of the
                # text localization

        # loop over each of the individual text localizations
        for i in range(0, len(searchResults["text"])):
            # extract the bounding box coordinates of the text region from
            # the current result
            x = int(searchResults["left"][i] / 2.5)
            y = int(searchResults["top"][i] / 2.5)
            w = int(searchResults["width"][i] / 2.5)
            h = int(searchResults["height"][i] / 2.5)
            # extract the OCR text itself along with the confidence of the
            # text localization
            text = searchResults["text"][i]
            conf = int(float(searchResults["conf"][i]))

        # filter out weak confidence text localizations
            if conf > 50:
                # display the confidence and text to our terminal
                # print(searchResults)
                print("Confidence: {}".format(conf))
                print("Text: {}".format(text))
                print("Coördinates:", x, y, w, h, "(x, y, w, h)")
                print("")
                # strip out non-ASCII text so we can draw the text on the image
                # using OpenCV, then draw a bounding box around the text along
                # with the text itself
                text = "".join(
                    [c if ord(c) < 128 else "" for c in text]).strip()
                cv2.rectangle(image, (x, y),
                              (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN,
                            1.5, (0, 255, 255), 2)

        # show the output image
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

        return image
