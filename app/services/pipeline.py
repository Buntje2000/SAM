import time
from app.classes.services.dicom_reception import DicomReception
from app.classes.image.manipulate_pixels import ManipulatePixels
from app.classes.image.pre_process_image import PreProcessImage
from app.classes.image.recognize_text import RecognizeText
from app.classes.services.patient_info_extraction import PatientInfoExtraction
from app.classes.meta.manipulate_meta import ManipulateMeta
from app.classes.meta.search_in_meta import SearchInMeta


def start(path, search):
    # Get Dicom
    dicomFile = DicomReception.get_dicom(
        path
        # "../../DICOM/MRI/1.3.6.1.4.1.40744.65.16031967164511444248270689772770998964-1-8-lfjc9z.dcm"
        # "../../DICOM/CT/2_Thorax_Blanco_1.5_Br38_2_ax_MS/1.3.6.1.4.1.40744.65.101120006751829385571428157359899373831.dcm"
    )
    patientInfo = PatientInfoExtraction.get_patient_info(dicomFile)

    # Meta
    start_time = time.time()
    metaFields = SearchInMeta.search_for_patient_info(
        dicomFile, patientInfo)
    # print(metaFields)
    cleanMeta = ManipulateMeta.delete_patient_info_from_meta(
        metaFields, dicomFile)
    cleanMeta.save_as("testDicomAnonimyzed.dcm")
    print("--- Looptijd meta-pipeline: %s seconden ---" %
          round(time.time() - start_time, 3))

    # Image
    image = PreProcessImage.image_to_array(dicomFile)

    start_time = time.time()
    processed_image = PreProcessImage.pre_process_image(image)
    recognized = RecognizeText.recognize_text(
        processed_image, patientInfo, image, search)
    # ManipulatePixels.save_image(recognized, cleanMeta)
    print("--- Looptijd image-pipeline: %s seconden ---" %
          round(time.time() - start_time, 3))
