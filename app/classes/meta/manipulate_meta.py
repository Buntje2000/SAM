from pipelayer import Filter


class ManipulateMeta(Filter):
    def run(self, data, context):

        _patientName = data.meta

        return _patientName
