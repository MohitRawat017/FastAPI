from fastapi import FastAPI, Path , HTTPException , Query
import json
app = FastAPI()

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

# to run the app use the command: uvicorn main:app --reload
    
