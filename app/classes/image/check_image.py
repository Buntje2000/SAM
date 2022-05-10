import os
from deid.dicom import DicomCleaner, get_files


class CheckImage:
    def check_image_for_known_burnedinpixels(tmpDir, dicomFile):
        # dataset = get_dataset('tmp')
        # print("Dataset:", dataset)
        dicom_file = list(get_files(tmpDir))[0]
        print("Dicom file:", dicom_file)

        outputDir = 'output'
        if not os.path.isdir(outputDir):
            try:
                os.mkdir(outputDir)
            except OSError:
                print("Creation of the directory %s failed" % outputDir)
            else:
                print("Successfully created the directory %s " % outputDir)

        client = DicomCleaner(output_folder=outputDir)
        detectionData = client.detect(dicom_file)

        return detectionData
