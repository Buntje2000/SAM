from pipelayer import Filter
from app.models.patient_model import PatientModel

class SearchInMeta(Filter):
    def run(self, data, context):
        
        _meta = self.search_for_patient_info(data)

        return _meta

    def search_for_patient_info(self, data):

        meta = data

        return meta