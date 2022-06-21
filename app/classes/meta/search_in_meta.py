import logging
import pydicom.valuerep
from pydicom import FileDataset
from app.models.patient_model import PatientModel
from app.classes.meta.helper import stringSplitter, valueSplitter, getMetaThreshold
from app.classes.services.helper import similarity


logger = logging.getLogger('file')


class SearchInMeta:
    def search_for_patient_info(dicom: FileDataset, patientInfo: PatientModel, replacement=None):
        '''Zoekt in de metagegevens naar achternaam en id van patient.'''
        count = 0
        itemsSearched = 0
        itemsFound = 0
        patientName: pydicom.valuerep.PersonName = patientInfo.patient_name

        threshold = getMetaThreshold()

        anonimyzedFields = []
        fieldsToSkip = ["AE", "AS", "AT", "DA", "DT", "FL", "FD", "IS", "OB",
                        "OD", "OF", "OW", "SL", "SQ", "SS", "TM", "UI", "UL", "US", "UN"]

        for elem in dicom.iterall():
            count += 1

            if elem.VR not in fieldsToSkip:
                itemsSearched += 1

                values = valueSplitter(stringSplitter(str(elem.value)))

                for value in values:
                    # Als de gevonden waarde (deels) overeenkomt met de achternaam van de patient, dan moet deze worden vervangen.
                    try:
                        if patientName.family_name != '' and similarity(value, patientName.family_name) > threshold:
                            # if patientName.family_name != "" and patientName.family_name in value:
                            itemsFound += 1

                            anonimyzedFields.append(
                                [elem.tag,
                                    value])
                    except Exception as e:
                        logger.warning(e)

                    # Als de gevonden waarde (deels) overeenkomt met de voornaam van de patient, dan moet deze worden vervangen.
                    try:
                        if patientName.given_name != '' and similarity(value, patientName.given_name) > threshold:
                            # if patientName.given_name != "" and patientName.given_name in value:
                            itemsFound += 1

                            if str(elem.tag) == '(0010, 0010)':

                                anonimyzedFields.append(
                                    [elem.tag,
                                     value]
                                )
                            else:
                                anonimyzedFields.append(
                                    [elem.tag,
                                     value]
                                )
                    except Exception as e:
                        logger.warning(e)

                    # Als de gevonden waarde (deels) overeenkomt met het ID van de patient, dan moet deze worden vervangen.
                    try:
                        if patientInfo.patient_id != '' and similarity(value, patientInfo.patient_id) > threshold:
                            # if patientInfo.patient_id != "" and patientInfo.patient_id in value:
                            itemsFound += 1

                            # newString = str(elem.value).replace(
                            #     value, idReplacement)

                            anonimyzedFields.append(
                                [elem.tag,
                                 value]
                            )
                    except Exception as e:
                        logger.warning(e)

        logger.debug("Aantal loops: " + str(count))
        logger.debug("Aantal items doorzocht: " +
                     str(itemsSearched))
        logger.debug(
            "Aantal items met persoonsgegevens gevonden: " + str(itemsFound))

        return anonimyzedFields
