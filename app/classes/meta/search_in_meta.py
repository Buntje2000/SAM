import pydicom
import pydicom.valuerep
from app.models.patient_model import PatientModel
import logging


class SearchInMeta:
    def search_for_patient_info(dicom: pydicom.FileDataset, patientInfo: PatientModel):
        count = 0
        itemsSearched = 0
        itemsFound = 0
        patientName: pydicom.valuerep.PersonName = patientInfo.patient_name

        anonimyzedFields = []
        fieldsToSkip = ["AE", "AS", "AT", "DA", "DT", "FL", "FD", "IS", "OB",
                        "OD", "OF", "OW", "SL", "SQ", "SS", "TM", "UI", "UL", "US", "UN"]

        for elem in dicom.iterall():
            count += 1

            if elem.VR not in fieldsToSkip:
                itemsSearched += 1

                if patientName.family_name in str(elem.value):
                    itemsFound += 1

                    if str(elem.tag) == '(0010, 0010)':
                        newString = str(elem.value).replace(
                            str(patientName), '**name**')

                        anonimyzedFields.append(
                            [elem.tag,
                             newString]
                        )
                    else:
                        newString = str(elem.value).replace(
                            patientName.family_name, '**name**')

                        anonimyzedFields.append(
                            [elem.tag,
                             newString]
                        )

                if patientInfo.patient_id in str(elem.value):
                    itemsFound += 1

                    newString = str(elem.value).replace(
                        patientInfo.patient_id, '**id**')

                    anonimyzedFields.append(
                        [elem.tag,
                         newString]
                    )

        print("--- Aantal loops:", count, "---")
        print("--- Aantal items doorzocht:", itemsSearched, "---")
        print("--- Aantal items met persoonsgegevens gevonden:", itemsFound, "---")

        return anonimyzedFields
