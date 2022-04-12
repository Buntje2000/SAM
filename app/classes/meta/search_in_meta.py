import pydicom

from app.models.patient_model import PatientModel


class SearchInMeta:
    def search_for_patient_info(dicom: pydicom.FileDataset, patientInfo: PatientModel):
        count = 0

        for elem in dicom.iterall():
            count += 1
            if str(patientInfo.patient_name) in str(elem.value):
                print(patientInfo.patient_name,
                      "is gevonden in", elem.tag, elem.keyword)
            elif str(patientInfo.patient_id) in str(elem.value):
                print(patientInfo.patient_id,
                      "is gevonden in", elem.tag, elem.keyword)

        print("Aantal loops", count)

        return patientInfo
