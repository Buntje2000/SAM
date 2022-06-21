from pydicom import FileDataset, dcmread


file = "testDicom2.dcm"

try:
    if isinstance(file, FileDataset):
        dicomFile = file
    elif isinstance(file, str):
        dicomFile = dcmread(file)
except Exception as e:
    print(e)

dicomFile.PatientName = "Bunt^Alexander"
dicomFile.PatientID = "184950"
dicomFile.PatientComments = "Bunq184951"

dicomFile.save_as("nameTestDicom2.dcm")
