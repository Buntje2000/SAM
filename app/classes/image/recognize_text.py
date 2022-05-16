import configparser
from pydicom import FileDataset
import pydicom.valuerep
from pytesseract import Output
import pytesseract
import cv2
from collections import defaultdict
import difflib
from app.config import config


from app.models.patient_model import PatientModel


class RecognizeText:
    def recognize_text(processed_image, patientInfo: PatientModel, image, search, profile, dicomFile: FileDataset):

        def similarity(word, pattern):
            return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()

        # Spell mistakes acceptance ratio
        threshold = float(config("PIXEL", "similarity_threshold"))

        # TESSERACT
        results = pytesseract.image_to_data(
            processed_image, config='--psm 12 --oem 3', output_type=Output.DICT)

        searchResults = defaultdict(list)

        patientName: pydicom.valuerep.PersonName = patientInfo.patient_name

        low = [patientName.family_name,
               patientInfo.patient_id, patientInfo.patient_dob]
        medium = [patientName.family_name,
                  patientInfo.patient_id, patientInfo.patient_dob]
        high = [patientName.family_name,
                patientInfo.patient_id, patientInfo.patient_dob,
                dicomFile.SeriesDate, dicomFile.StudyDate,
                dicomFile.ContentDate]

        for i in range(0, len(results["text"])):
            # extract the bounding box coordinates of the text region from
            # the current result
            if profile == 'low':
                for filter in low:
                    if filter != None:
                        if similarity(results["text"][i], filter) > threshold:
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

            if profile == 'medium':
                for filter in medium:
                    if filter != None:
                        if similarity(results["text"][i], filter) > threshold:
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

            if profile == 'high':
                for filter in high:
                    if filter != None:
                        if similarity(results["text"][i], filter) > threshold:
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

            if search != None:
                if similarity(results["text"][i], search) > threshold:
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
            x = int(searchResults["left"][i])
            y = int(searchResults["top"][i])
            w = int(searchResults["left"][i]) + int(searchResults["width"][i])
            h = int(searchResults["top"][i]) + int(searchResults["height"][i])
            # extract the OCR text itself along with the confidence of the
            # text localization
            text = searchResults["text"][i]
            conf = int(float(searchResults["conf"][i]))

        # filter out weak confidence text localizations
            if conf > 40:
                # display the confidence and text to our terminal
                # print(searchResults)
                print("")
                print("LOGGING AFBEELDINGSHERKENNING")
                print("Gezochtte tekst: {}".format(search))
                print("Gevonden tekst: {}".format(text))
                print("Confidence: {}".format(conf))
                print("Coördinates:", x, y, w, h, "(x, y, w, h)")
                print("")
                # strip out non-ASCII text so we can draw the text on the image
                # using OpenCV, then draw a bounding box around the text along
                # with the text itself
                text = "".join(
                    [c if ord(c) < 128 else "" for c in text]).strip()
                cv2.rectangle(image, (x, y),
                              (w, h), (0, 255, 255), 2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN,
                            1.5, (0, 255, 255), 2)

        # show the output image
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

        if len(searchResults["text"]) == 0:
            print('Geen gevoellige data gevonden in afbeelding')

        return searchResults

    def add_coordinates_to_file(coordinates: defaultdict, dicomFile: FileDataset):
        """Append new scanner as a new item at the end of file"""

        label: str = "LABEL " + dicomFile.Manufacturer + \
            " " + dicomFile.ManufacturerModelName + " # (ANB)"
        modality: str = "  contains Modality " + dicomFile.Modality
        manufacturer: str = "  + contains Manufacturer " + dicomFile.Manufacturer
        rows: str = "  + equals Rows " + str(dicomFile.Rows)
        modelName: str = "  + contains ManufacturerModelName " + \
            dicomFile.ManufacturerModelName

        lines_to_append = [label, modality,
                           manufacturer, rows, modelName]
        # LABEL Philips Affiniti  # (AMB)
        # contains Modality US
        # + contains Manufacturer Philips
        # + equals Rows 768
        # + contains ManufacturerModelName Affiniti 70G
        # coordinates 0,0,1024,22

        # Open the file in append & read mode ('a+')
        with open("app/data/deid.custom", "a+") as file_object:
            appendFirstEOL = False
            appendEOL = False
            # Move read cursor to the start of file.
            file_object.seek(0)
            # Check if file is not empty
            data = file_object.read(100)
            if len(data) > 0:
                appendFirstEOL = True
            # Iterate over each string in the list
            for line in lines_to_append:
                # If file is not empty then append '\n' before first line for
                # other lines always append '\n' before appending line
                if appendEOL == True:
                    file_object.write("\n")
                elif appendFirstEOL == True:
                    file_object.write("\n\n")
                    appendFirstEOL = False
                    appendEOL = True
                else:
                    appendEOL = True
                # Append element at the end of file
                file_object.write(line)

            for i in range(0, len(coordinates["text"])):
                x = int(coordinates["left"][i])
                y = int(coordinates["top"][i])
                w = int(coordinates["width"][i])
                h = int(coordinates["height"][i])

                spotLine: str = "\n  coordinates " + \
                    str(x) + "," + str(y) + "," + str(x + w) + "," + str(y + h)
                file_object.write(spotLine)
