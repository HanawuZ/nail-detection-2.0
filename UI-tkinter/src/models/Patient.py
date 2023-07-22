class Patient:
    def __init__(self, patient_id=None, first_name=None, last_name=None, age=None) -> None:
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.data = None

    def set_patient_data(self,patient_id, first_name, last_name, age):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def set_intensity(self,data):
        self.data = data


