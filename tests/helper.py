from faker import Faker
from app.models.patient_model import PatientModel
import random


class Helper:
    '''
        This class provides all required entities that are needed for testing.
    '''

    _fake = Faker('nl_NL')

    def create_patient(self) -> PatientModel:
        '''
            Returns a PatientModel with fake data
        '''
        return PatientModel(
            patient_name=self._fake.first_name(),
            patient_id=str(random.randint(10, 999999))
        )
