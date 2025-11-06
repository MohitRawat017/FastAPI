from pydantic import BaseModel, Field , field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated
from pydantic import EmailStr, AnyUrl

class Patient(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    # if we want to create a data validation where we would require multiple fields to validate together , for this we would require model_validator
    @model_validator(mode='after')
    @classmethod

    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency_contact' not in model.contact_details:
            raise ValueError('Emergency contact is required for patients over 60 years old.')
        return model
    
    # we can also perform COMPUTED FIELDS
    @computed_field
    @property
    def bmi(self) -> float:
        if self.height > 0:
            return self.weight / (self.height ** 2)
        return 0.0


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted successfully")
    print(f"BMI: {patient.bmi}")
patientInfo = {'name': 'John Doe', 'age': 30, 'weight': 70.5, 'height': 1.75, 'married': True, 'allergies': ['penicillin'], 'contact_details': {'email': 'john.doe@example.com'}}
patient1 = Patient(**patientInfo)
insert_patient_data(patient1)



