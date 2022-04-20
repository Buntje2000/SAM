from PIL import Image
import io
import numpy as np
from pydicom import FileDataset
import cv2
from pydicom.encaps import encapsulate


class ManipulatePixels:
    def save_image(image, ds: FileDataset):
        num_frames = 1
        # Convert to PIL
        imlist = []
        # convert the multiframe image into RGB of single frames (Required for compression)
        for i in range(num_frames):
            imlist.append(Image.fromarray(image))

        # Save the multipage tiff with jpeg compression
        f = io.BytesIO()
        imlist[0].save(f, format='tiff', append_images=imlist[1:],
                       save_all=True, compression='jpeg')
        # The BytesIO object cursor is at the end of the object, so I need to tell it to go back to the front
        f.seek(0)
        img = Image.open(f)

        # Get each one of the frames converted to even numbered bytes
        img_byte_list = []
        for i in range(num_frames):
            try:
                img.seek(i)
                with io.BytesIO() as output:
                    img.save(output, format='jpeg')
                    img_byte_list.append(output.getvalue())
            except EOFError:
                # Not enough frames in img
                break

        ds.PixelData = encapsulate([x for x in img_byte_list])
        ds['PixelData'].is_undefined_length = True
        ds.is_implicit_VR = False
        ds.LossyImageCompression = '01'
        ds.LossyImageCompressionRatio = 10  # default jpeg
        ds.LossyImageCompressionMethod = 'ISO_10918_1'
        ds.file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.4.70'

        ds.save_as("output-jpeg.dcm", write_like_original=True)

        print("Image saved")
