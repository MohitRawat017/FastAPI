from fastapi import FastAPI, Path , HTTPException , Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse
# literal is used to restrict a variable to specific string values . here Gender: male female or other .
import json
app = FastAPI()
class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description="ID of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., description="Height of the patient in meters", gt=0 , lt=3)]
    weight: Annotated[float, Field(..., description="Weight of the patient in kg" , gt=0)]

    # we need to calculate the bmi and the verdict based on the bmi value
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"

# new pydantic for PUT method
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Name of the patient")]
    city: Annotated[Optional[str], Field(None, description='City where the patient is living')]
    age: Annotated[Optional[int], Field(None, description="Age of the patient", gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(None, description="Height of the patient in meters", gt=0 , lt=3)]
    weight: Annotated[Optional[float], Field(None, description="Weight of the patient in kg" , gt=0)]
    


def save_data(data):
    with open('patients.json', 'w') as file:
        json.dump(data, file)

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data
# earlier we used to return data directly but as our patients.json was a dictionary of dictionaries
# we converted it to a list of dictionaries using list(data.values())
# this will make it easier to work with the data in our endpoints because we can iterate over a list of dictionaries directly.

@app.get("/")
async def home():
    return {"message": "Welcome to the Home Page!"}

@app.get("/about")
async def about():
    return {"message": "This is the About Page."}

@app.get("/view")
async def view_patients():
    data = load_data()
    return {"patients": data}
 
@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    # patient = next((item for item in data if item["id"] == patient_id), None)
    # next is basically one liner clear version of this loop 
    # patient = None
    # for item in data:
    #     if item["id"] == patient_id:
    #         patient = item
    #        break
    patient = data.get(patient_id)
    if patient:
        return {"patient": patient}
    else:
        raise HTTPException(status_code=404, detail="Patient not found")
    
@app.get("/sort")
def sort_patients(sort_by : str = Query(..., description="Field to sort by height , weight, bmi"), # here the ... means mandatory field
                        order : str = Query("asc", description="Sort order: asc or desc")): # we have set a default value for order
    
    if sort_by not in ["height", "weight", "bmi"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by field")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order value")
    
    data = load_data()
    data = list(data.values())
    reverse = True if order == "desc" else False
    sorted_data = sorted(data, key=lambda x: x.get(sort_by, 0), reverse=reverse)
    # can you explain this line?
    # the sorted() function sorts the data based on the specified sort_by field.
    # it takes in three arguments: the data to be sorted, a key function that extracts the sort_by field from each item, and a reverse flag that determines the sort order .
    # the key function is defined using a lambda expression, which allows us to specify the sorting logic in a concise way.
    return {"sorted_patients": sorted_data}


@app.post('/create')
def create_patient(patient: Patient):
    
    # load the existing data 
    data = load_data()
    # check if patient with same id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    # add the new patient to the database
    data[patient.id] = patient.model_dump(exclude=['id']) #type: ignore
    # what model_dump does is it converts the pydantic model instance to a dictionary .
    # save into json file
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": patient.model_dump()})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing_patient_data = data[patient_id]
    # lets convert the pydantic model to dictionary 
    update_data = patient_update.model_dump(exclude_unset=True)
    # exclude_unset = True means only include fields that were explicitly set when creating the model
    for key, value in update_data.items():
        existing_patient_data[key] = value
    existing_patient_data["id"] = patient_id # as there was id missing in the existing_patient_data
    # existing_patient_info -> pydantic object -> we get the updated bmi + verdict -> pydantic object -> dictionary
    patient_pydantic_object = Patient(**existing_patient_data)
    patient_pydantic_model_dict = patient_pydantic_object.model_dump(exclude=['id']) #type: ignore 
    # i have dumped we don't need the id value in the dictionary now .
    data[patient_id] = patient_pydantic_model_dict
    save_data(data)
    return {"message": "Patient updated successfully", "patient": patient_pydantic_model_dict}

# Delete endpoint 
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return {"message": "Patient deleted successfully"}

# to run the app use the command: uvicorn main:app --reload
    
