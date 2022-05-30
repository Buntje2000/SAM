import difflib
from pydicom import FileDataset
import pydicom.valuerep
from app.models.patient_model import PatientModel
from app.config import config
import logging


class SearchInMeta:
    def search_for_patient_info(dicom: FileDataset, patientInfo: PatientModel, replacement):
        '''Zoekt in de metagegevens naar achternaam en id van patient.'''

        count = 0
        itemsSearched = 0
        itemsFound = 0
        patientName: pydicom.valuerep.PersonName = patientInfo.patient_name

        if replacement == None:
            nameReplacement = str(config("META", "name_replacement"))
            idReplacement = str(config("META", "id_replacement"))
        else:
            nameReplacement = replacement
            idReplacement = replacement

        def similarity(word, pattern):
            return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()

        cft = None
        try:
            # Spelfouten acceptatie ratio
            cft = float(config("META", "similarity_threshold"))
        except Exception as e:
            logging.warning(e)

        if cft != None and cft < 0.4:
            threshold = cft
            logging.warning(
                "Meta threshold is erg laag ingesteld (< 0.4). Dit verhoogt de kans op foutieve waarden. Controleer config.ini")
        elif cft != None:
            threshold = cft
        else:
            threshold = 0.8
            logging.warning(
                "Meta threshold is niet goed ingesteld. Standaardwaarde wordt gebruikt (0.8). Controleer config.ini")

        anonimyzedFields = []
        fieldsToSkip = ["AE", "AS", "AT", "DA", "DT", "FL", "FD", "IS", "OB",
                        "OD", "OF", "OW", "SL", "SQ", "SS", "TM", "UI", "UL", "US", "UN"]

        for elem in dicom.iterall():
            count += 1

            if elem.VR not in fieldsToSkip:
                itemsSearched += 1

                # Als de gevonden waarde (deels) overeenkomt met de achternaam van de patient, dan moet deze worden vervangen.
                if similarity(str(elem.value), patientName.family_name) > threshold:
                    itemsFound += 1

                    if str(elem.tag) == '(0010, 0010)':
                        newString = str(elem.value).replace(
                            str(patientName), nameReplacement)

                        anonimyzedFields.append(
                            [elem.tag,
                             newString]
                        )
                    else:
                        newString = str(elem.value).replace(
                            patientName.family_name, nameReplacement)

                        anonimyzedFields.append(
                            [elem.tag,
                             newString]
                        )

                # Als de gevonden waarde (deels) overeenkomt met het ID van de patient, dan moet deze worden vervangen.
                if similarity(str(elem.value), patientInfo.patient_id) > threshold:
                    itemsFound += 1

                    newString = str(elem.value).replace(
                        patientInfo.patient_id, idReplacement)

                    anonimyzedFields.append(
                        [elem.tag,
                         newString]
                    )

        logging.debug("Aantal loops: " + str(count))
        logging.debug("Aantal items doorzocht: " +
                      str(itemsSearched))
        logging.debug(
            "Aantal items met persoonsgegevens gevonden: " + str(itemsFound))

        return anonimyzedFields
