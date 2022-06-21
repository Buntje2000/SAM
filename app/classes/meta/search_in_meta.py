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

        foundValues = []
        fieldsToSkip = ["AE", "AS", "AT", "DA", "DT", "FL", "FD", "IS", "OB",
                        "OD", "OF", "OW", "SL", "SQ", "SS", "TM", "UI", "UL", "US", "UN"]
        dataToFind = [patientName.family_name,
                        patientName.given_name, patientInfo.patient_id]

        for elem in dicom.iterall():
            count += 1

            if elem.VR not in fieldsToSkip:
                itemsSearched += 1

                values = valueSplitter(stringSplitter(str(elem.value)))

                for value in values:
                    # Als de gevonden waarde (deels) overeenkomt met de gezochte waarde, dan moet deze worden vervangen.
                    try:
                        for i in range(len(dataToFind)):
                            if dataToFind[i] != '' and similarity(value, dataToFind[i]) > threshold:
                                itemsFound += 1

                                foundValues.append(
                                    [elem.tag,
                                        value])
                            elif dataToFind[i] != '' and dataToFind[i] in value:
                                itemsFound += 1

                                foundValues.append(
                                    [elem.tag,
                                        value])
                    except Exception as e:
                        logger.warning(e)

        logger.debug("Aantal loops: " + str(count))
        logger.debug("Aantal items doorzocht: " +
                     str(itemsSearched))
        logger.debug(
            "Aantal items met persoonsgegevens gevonden: " + str(itemsFound))

        print(foundValues)

        return foundValues
