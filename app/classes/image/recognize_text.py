from pydicom import FileDataset
from pytesseract import Output
import pytesseract
import cv2
from collections import defaultdict
import difflib


from app.models.patient_model import PatientModel


class RecognizeText:
    def recognize_text(processed_image, patientInfo: PatientModel, image, search):
        # # EASYOCR

        # start_time = time.time()
        # reader = Reader(['en'], gpu=False)
        # print("--- Looptijd READER: %s seconden ---" %
        #       round(time.time() - start_time, 3))
        # start_time = time.time()
        # results = reader.readtext(processed_image)
        # print("--- Looptijd RECOGNITION: %s seconden ---" %
        #       round(time.time() - start_time, 3))

        # searchResults = defaultdict(list)

        # # loop over the results
        # for (bbox, text, prob) in results:
        #     if str.lower("y") in str.lower(text):
        #         # display the OCR'd text and associated probability
        #         print("Confidence {:.2f}: {}".format(prob, text))
        #         # unpack the bounding box
        #         (tl, tr, br, bl) = bbox
        #         tl = (int(tl[0]), int(tl[1]))
        #         tr = (int(tr[0]), int(tr[1]))
        #         br = (int(br[0]), int(br[1]))
        #         bl = (int(bl[0]), int(bl[1]))

        #         searchResults["text"].append(text)
        #         searchResults["topLeft"].append(tl)
        #         searchResults["topRight"].append(tr)
        #         searchResults["bottomLeft"].append(bl)
        #         searchResults["bottomRight"].append(br)
        #         searchResults["conf"].append(prob)
        #         # cleanup the text and draw the box surrounding the text along
        #         # with the OCR'd text itself
        #         # text = cleanup_text(text)
        #         cv2.rectangle(image, tl, br, (0, 255, 0), 2)
        #         cv2.putText(image, text, (tl[0], tl[1] - 10),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        def similarity(word, pattern):
            return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()

        # Spell mistakes acceptance ratio
        threshold = 0.6

        # TESSERACT
        results = pytesseract.image_to_data(
            processed_image, config='--psm 12 --oem 3', output_type=Output.DICT)

        searchResults = defaultdict(list)

        for i in range(0, len(results["text"])):
            # extract the bounding box coordinates of the text region from
            # the current result
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
            w = int(searchResults["width"][i])
            h = int(searchResults["height"][i])
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
                print("Gezochte tekst: {}".format(search))
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
                              (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN,
                            1.5, (0, 255, 255), 2)

        # show the output image
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

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
                x = str(coordinates["left"][i])
                y = str(coordinates["top"][i])
                w = str(coordinates["width"][i])
                h = str(coordinates["height"][i])

                spotLine: str = "\n  coordinates " + x + "," + y + "," + w + "," + h
                file_object.write(spotLine)
