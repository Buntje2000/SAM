from pydicom import FileDataset
import logging


class ManipulateMeta():
    def delete_patient_info_from_meta(metaFields, dicomFile: FileDataset):
        dicom = dicomFile

        itemsChanged = 0

        for x in metaFields:
            itemsChanged += 1

            tag = str(x[0])
            tag1, tag2 = tag.split(", ")
            tagD1 = "0x" + tag1.replace("(", "")
            tagD2 = "0x" + tag2.replace(")", "")

            dicom[tagD1, tagD2].value = x[1]

        logging.info("--- Aantal items geannonimiseerd: " + str(itemsChanged) + " ---")

        return dicom
