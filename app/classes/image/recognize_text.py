import logging
import difflib
import cv2
import pytesseract
import pydicom.valuerep
from pydicom import FileDataset
from pytesseract import Output
from collections import defaultdict
from app.config import config
from app.models.patient_model import PatientModel


class RecognizeText:
    def recognize_text(processed_image, patientInfo: PatientModel, image, profile, dicomFile: FileDataset, search=None):

        def similarity(word, pattern):
            return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()

        cft = None
        try:
            # Spelfouten acceptatie ratio
            cft = float(config("PIXEL", "similarity_threshold"))
        except Exception as e:
            logging.warning(e)

        if cft != None and cft < 0.3:
            threshold = cft
            logging.warning(
                "Pixel threshold is erg laag ingesteld (< 0.3). Dit verhoogt de kans op foutieve waarden. Controleer config.ini")
        elif cft != None:
            threshold = cft
        else:
            threshold = 0.6
            logging.warning(
                "Pixel threshold is niet goed ingesteld. Standaardwaarde wordt gebruikt (0.6). Controleer config.ini")

        cnf = None
        try:
            # Minimale zekerheid van herkenning
            cnf = int(config("PIXEL", "min_confidence"))
        except Exception as e:
            logging.warning(e)

        if cnf != None and cnf < 30:
            threshold = cft
            logging.warning(
                "Minimale 'confidence' is erg laag ingesteld (< 30). Dit verhoogt de kans op foutieve waarden. Controleer config.ini")
        elif cnf != None:
            conf = cnf
        else:
            conf = 60
            logging.warning(
                "Minimale 'confidence' is niet goed ingesteld. Standaardwaarde wordt gebruikt (60). Controleer config.ini")

        # TESSERACT
        results = pytesseract.image_to_data(
            processed_image, config='--psm 12 --oem 3', output_type=Output.DICT)

        searchResults = defaultdict(list)

        patientName: pydicom.valuerep.PersonName = patientInfo.patient_name

        # Profielen -> welke data moet er worden gezocht in de afbeelding.
        low = [patientName.family_name,
               patientInfo.patient_id, patientInfo.patient_dob]
        medium = [patientName.family_name,
                  patientInfo.patient_id, patientInfo.patient_dob, dicomFile.StudyDate]
        high = [patientName.family_name,
                patientInfo.patient_id, patientInfo.patient_dob,
                dicomFile.SeriesDate, dicomFile.StudyDate,
                dicomFile.ContentDate]

        if len(results["text"]) > 0:
            searchResults["detected"].append(True)
        else:
            searchResults["detected"].append(False)

        # extract the bounding box coordinates of the text region from
        # the current result
        try:
            for filter in locals()[profile]:
                if filter != None:
                    for i in range(0, len(results["text"])):
                        if similarity(results["text"][i], filter) > threshold:
                            if float(results["conf"][i]) > cnf:
                                t = results["text"][i]
                                x = results["left"][i]
                                y = results["top"][i]
                                w = int(results["width"][i]) + \
                                    int(results["left"][i])
                                h = int(results["height"][i]) + \
                                    int(results["top"][i])
                                c = int(float(results["conf"][i]))

                                searchResults["text"].append(t)
                                searchResults["left"].append(x)
                                searchResults["top"].append(y)
                                searchResults["width"].append(w)
                                searchResults["height"].append(h)
                                searchResults["conf"].append(c)
                                # extract the OCR text itself along with the confidence of the
                                # text localization
        except:
            logging.error("Profiel niet gevonden")

        if search != None:
            for i in range(0, len(results["text"])):
                if similarity(results["text"][i], search) > threshold:
                    if float(results["conf"][i]) > cnf:
                        t = results["text"][i]
                        x = results["left"][i]
                        y = results["top"][i]
                        w = int(results["width"][i]) + \
                            int(results["left"][i])
                        h = int(results["height"][i]) + \
                            int(results["top"][i])
                        c = int(float(results["conf"][i]))

                        searchResults["text"].append(t)
                        searchResults["left"].append(x)
                        searchResults["top"].append(y)
                        searchResults["width"].append(w)
                        searchResults["height"].append(h)
                        searchResults["conf"].append(c)
                        # extract the OCR text itself along with the confidence of the
                        # text localization
        items = 0
        # loop over each of the individual text localizations
        for i in range(0, len(searchResults["text"])):
            # extract the bounding box coordinates of the text region from
            # the current result
            x = int(searchResults["left"][i])
            y = int(searchResults["top"][i])
            w = int(searchResults["left"][i])
            h = int(searchResults["top"][i])
            # extract the OCR text itself along with the confidence of the
            # text localization
            text = searchResults["text"][i]
            conf = int(float(searchResults["conf"][i]))

        # filter out weak confidence text localizations
            if conf > 40:
                items += 1
                # display the confidence and text to our terminal
                # print(searchResults)
                logging.debug(f"HERKEND ITEM {items}:")
                if search != None:
                    logging.debug("Gezochte tekst: {}".format(search))
                logging.debug("Gevonden tekst: {}".format(text))
                logging.debug("Confidence: {}".format(conf))
                logging.debug(f"Coordinates: {x},{y},{w},{h} (x, y, w, h)")
                # strip out non-ASCII text so we can draw the text on the image
                # using OpenCV, then draw a bounding box around the text along
                # with the text itself
                text = "".join(
                    [c if ord(c) < 128 else "" for c in text]).strip()
                cv2.rectangle(image, (x, y),
                              (w, h), (0, 255, 255), 2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN,
                            1.5, (0, 255, 255), 2)

        if len(searchResults["text"]) == 0:
            logging.info('Geen gevoellige data gevonden in afbeelding')
        else:
            length = len(searchResults["text"])
            logging.info(
                f'Aantal gevoellige items gevonden in afbeelding: {length}')

        return searchResults

    def add_coordinates_to_file(coordinates: defaultdict, dicomFile: FileDataset):
        """Add custom coordinates to file 'custom.dicom'"""

        first_part: str = "FORMAT dicom\n\n%filter customlist\n\n# Flags Only\n"
        label: str = f"LABEL {dicomFile.Manufacturer} {dicomFile.ManufacturerModelName} # (ANB)"
        modality: str = f"  contains Modality {dicomFile.Modality}"
        manufacturer: str = f"  + contains Manufacturer {dicomFile.Manufacturer}"
        rows: str = f"  + equals Rows {dicomFile.Rows}"
        modelName: str = f"  + contains ManufacturerModelName {dicomFile.ManufacturerModelName}"

        lines_to_append = [first_part, label, modality,
                           manufacturer, rows, modelName]
        # LABEL Philips Affiniti 70G # (ANB)
        # contains Modality US
        # + contains Manufacturer Philips
        # + equals Rows 768
        # + contains ManufacturerModelName Affiniti 70G
        # coordinates 0,0,1024,22

        # Open the file in append & read mode ('a+')
        with open("app/data/deid.custom", "a+") as file_object:
            appendEOL = False
            # Move read cursor to the start of file.
            file_object.seek(0)
            file_object.truncate()

            data = file_object.read(100)
            if len(data) > 0:
                appendEOL = True
            # Iterate over each string in the list
            for line in lines_to_append:
                if appendEOL == True:
                    file_object.write("\n")
                else:
                    appendEOL = True
                file_object.write(line)

            for i in range(0, len(coordinates["text"])):
                x = int(coordinates["left"][i])
                y = int(coordinates["top"][i])
                w = int(coordinates["width"][i])
                h = int(coordinates["height"][i])

                spotLine: str = f"\n  coordinates {x},{y},{w},{h}"
                file_object.write(spotLine)
