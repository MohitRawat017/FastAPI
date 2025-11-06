from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
import pickle
from typing import Literal, Annotated, Optional
import pandas as pd 

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = FastAPI()

# Pydantic model to validate incoming data
class UserInputs(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description= "Age of the person in years")]
    weight: Annotated[float, Field(..., gt=0, description= "Weight of the person in pounds")]
    height: Annotated[float, Field(..., gt=0, description= "Height of the person in inches")]
    income_lpa: Annotated[float, Field(..., ge=0, description= "Income in LPA")]
    smoker: Annotated[bool, Field(..., description= "Is the person a smoker? True or False")]
    city: Annotated[str, Field(..., description= "City of residence")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'buisness_owner', 'unemployed', 'private_job'], Field(..., description= "Occupation of the person")]

    @computed_field
    @property
    def bmi(self) -> float:
        return (self.weight / (self.height ** 2))
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif 25 <= self.age < 45:
            return "adult"
        elif 45 <= self.age < 65:
            return "middle_aged"
        else:
            return "senior"
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2   
        else:
            return 3
        

@app.post("/predict")
def predict_premium(data: UserInputs):
    # Convert the data to a DataFrame
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])
    # Make prediction
    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={'predicted_category': prediction})


