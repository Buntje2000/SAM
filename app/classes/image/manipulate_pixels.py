from deid.dicom import DicomCleaner, get_files


class ManipulatePixels:
    def manipulate_known_pixels(tmpDir):
        dicom_file = list(get_files(tmpDir))[0]
        outputDir = 'output'
        client = DicomCleaner(output_folder=outputDir)
        # client.detect('tmp/testDicom.dcm')
        client.detect(dicom_file)
        client.clean()
        client.save_dicom(handler_name="gdcm")

    def manipulate_unknown_pixels(tmpDir, spots):
        dicom_file = list(get_files(tmpDir))[0]
        outputDir = 'output'
        client = DicomCleaner(output_folder=outputDir)
        # client.detect('tmp/testDicom.dcm')
        client.detect(dicom_file)
        client.clean(spots)
        client.save_dicom(handler_name="gdcm")

        # DEID ADD - deid/dicom/pixels/clean.py
        # dicom.decompress(handler_name='gdcm')
        # pixel_data_handlers.convert_color_space(
        #     dicom.pixel_array, 'YBR_FULL', 'RGB')
