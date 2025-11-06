from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Annotated
from pydantic import EmailStr, AnyUrl

# Step 1: Define a Pydantic model
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title="Name of the patient" )]  # name must be a non-empty string
    age: Annotated[int, Field(ge=0)]  # age must be a non-negative integer
    weight: Annotated[float, Field(gt=0,lt=120,strict=True)]  # weight must be greater than 0 and less than 120
    github_url: Optional[Annotated[AnyUrl, Field(title="GitHub URL")]] = None  # optional field
    email: Annotated[EmailStr, Field(title="Email Address")]  # email must be a valid email address
    married: Annotated[bool, Field(title="Marital Status", default=False)]  # married must be a boolean
    allergies: Optional[List[str]] = None  # default empty list
    contact_details: Annotated[Dict[str, str], Field(default_factory=dict)]  # default empty dict
    # we have defined our schema using Pydantic's BaseModel

def insert_patient_data(patient: Patient):
    # the patient parameter is of type Patient i.e. it must conform to the schema defined in the Patient model
    print(patient.name)
    print(patient.age)
    print("inserted successfully")

# Step 2: Create an instance of the model
patientInfo = {'name': 'John Doe', 'age': 30, 'weight': 70.5, 'married': True, 'allergies': ['penicillin'], 'contact_details': {'email': 'john.doe@example.com'}}
patient1 = Patient(**patientInfo)

insert_patient_data(patient1)

# As we can see We can do type validation easily using Pydantic models.
#----------------------------------------------------------------------------------------

# For data validation, Pydantic gives us some built-in data types like EmailStr, HttpUrl, etc.
# there is also the field function to provide additional validation and metadata for model fields.
# for adding metadata we use Annotated from typing module and Field from pydantic module. we can also set default values for fields.
# using the Field function we can also suppress the type coercion ('0' is accepted as int 0 by default) by setting strict=True in the Field function.