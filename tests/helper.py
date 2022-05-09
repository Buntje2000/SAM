from faker import Faker
from pydicom import FileDataset
from app.models.patient_model import PatientModel
import random
from app.services.generate_dicom import generate_file_with_specifics


class Helper:
    '''
        This class provides all required entities that are needed for testing.
    '''

    _fake = Faker('nl_NL')

    def create_fake_patient(self) -> PatientModel:
        '''
            Returns a PatientModel with fake data
        '''
        return PatientModel(
            patient_name=self._fake.first_name(),
            patient_id=str(random.randint(10, 999999))
        )
