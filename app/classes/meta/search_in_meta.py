import difflib
from pydicom import FileDataset
import pydicom.valuerep
from app.models.patient_model import PatientModel


class SearchInMeta:
    def search_for_patient_info(dicom: FileDataset, patientInfo: PatientModel):
        count = 0
        itemsSearched = 0
        itemsFound = 0
        patientName: pydicom.valuerep.PersonName = patientInfo.patient_name

        def similarity(word, pattern):
            return difflib.SequenceMatcher(a=word.lower(), b=pattern.lower()).ratio()

        # Spell mistakes acceptance ratio
        threshold = 0.8

        anonimyzedFields = []
        fieldsToSkip = ["AE", "AS", "AT", "DA", "DT", "FL", "FD", "IS", "OB",
                        "OD", "OF", "OW", "SL", "SQ", "SS", "TM", "UI", "UL", "US", "UN"]

        for elem in dicom.iterall():
            count += 1

            if elem.VR not in fieldsToSkip:
                itemsSearched += 1

                if similarity(str(elem.value), patientName.family_name) > threshold:
                    itemsFound += 1

                    if str(elem.tag) == '(0010, 0010)':
                        newString = str(elem.value).replace(
                            str(patientName), '**NAME**')

                        anonimyzedFields.append(
                            [elem.tag,
                             newString]
                        )
                    else:
                        newString = str(elem.value).replace(
                            patientName.family_name, '**NAME**')

                        anonimyzedFields.append(
                            [elem.tag,
                             newString]
                        )

                if patientInfo.patient_id in str(elem.value):
                    itemsFound += 1

                    newString = str(elem.value).replace(
                        patientInfo.patient_id, '**ID**')

                    anonimyzedFields.append(
                        [elem.tag,
                         newString]
                    )

        print("--- Aantal loops:", count, "---")
        print("--- Aantal items doorzocht:", itemsSearched, "---")
        print("--- Aantal items met persoonsgegevens gevonden:", itemsFound, "---")

        return anonimyzedFields
