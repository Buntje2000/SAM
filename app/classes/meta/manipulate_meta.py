from pydicom import FileDataset
import logging
from app.classes.meta.helper import getReplacement

logger = logging.getLogger('file')


class ManipulateMeta():
    def delete_patient_info_from_meta(metaFields, dicomFile: FileDataset, replacement=None):
        dicom = dicomFile

        itemsChanged = 0

        replacement = getReplacement(replacement)

        for x in metaFields:
            itemsChanged += 1

            tag = str(x[0])
            tag1, tag2 = tag.split(", ")
            tagD1 = "0x" + tag1.replace("(", "")
            tagD2 = "0x" + tag2.replace(")", "")

            oldString = str(dicom[tagD1, tagD2].value)

            newString = oldString.replace(
                x[1], replacement)

            if str(x[0]) == '(0010, 0010)':
                newString = replacement

            dicom[tagD1, tagD2].value = newString

        logger.info("Aantal items geannonimiseerd: " + str(itemsChanged))

        return dicom
