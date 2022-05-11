from deid.dicom import DicomCleaner, get_files


class ManipulatePixels:
    def manipulate_pixels(tmpDir):
        dicom_file = list(get_files(tmpDir))[0]
        outputDir = 'output'
        deidFiles = ['app/data/deid.dicom', 'app/data/deid.custom']
        client = DicomCleaner(output_folder=outputDir,
                              deid=deidFiles)
        client.detect(dicom_file)
        client.clean()
        # client.save_dicom(handler_name="gdcm")
        client.save_dicom()
        # client.save_png()

        # DEID ADD - deid/dicom/pixels/clean.py
        # dicom.decompress(handler_name='gdcm')
        # pixel_data_handlers.convert_color_space(
        #     dicom.pixel_array, 'YBR_FULL', 'RGB')
