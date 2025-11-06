from pydantic import BaseModel, Field , field_validator
from typing import List, Dict, Optional, Annotated
from pydantic import EmailStr, AnyUrl

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    married: bool
    allergies: List[str]
    email: EmailStr
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        valid_domains = {'example.com', 'test.com'}
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f'Email domain {domain} is not allowed.')
        return value
    # Custom validator for email , if the email domain is not in the allowed list it raises a ValueError.
    @field_validator('name', mode='after')
    # mode='after' (default is 'before') then value hame type coersion ke baad ki value milegi 
    # mode='before' then value hame original input ki value milegi bina kisi type coersion ke
    @classmethod
    def validate_name(cls, value):
        if not value.replace(' ', '').isalpha():
            raise ValueError('Name must contain only alphabetic characters and spaces.')
        return value
    # Custom validator for name , if the name contains non-alphabetic characters it raises a ValueError.

    # we can also perform cross-field validation
    @field_validator('weight', mode='before')
    @classmethod
    def validate_weight(cls, value):
        if value <= 0 or value >= 120:
            raise ValueError('Weight must be greater than 0 and less than 120.')
        return value
    
    # if we want to create a data validation where we would require multiple fields to validate together , for this we would require model_validator
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted successfully")
patientInfo = {'name': 'John Doe', 'age': 30, 'weight': 70.5, 'married': True, 'allergies': ['penicillin'], 'contact_details': {'email': 'john.doe@example.com'}}
patient1 = Patient(**patientInfo)
insert_patient_data(patient1)

