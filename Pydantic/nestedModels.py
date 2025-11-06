# kisi ek model ko kisi dusre model ke andar as a Field use karna .

from pydantic import BaseModel 

class Address(BaseModel):
    city: str
    state: str
    pincode: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address  # Nested Model

address_dict = {'city': 'New York', 'state': 'NY', 'pincode': '10001'}
address1 = Address(**address_dict)

patient_dict = {
    'name': 'Alice Smith',
    'gender': 'Female',
    'age': 28,
    'address': address1
}
patient1 = Patient(**patient_dict)
print(patient1)
print(patient1.address.city)  # Accessing nested model field


temp = patient1.model_dump()
# model_dump() method se hame pura data dictionary format me mil jata hai including nested models
temp2 = patient1.model_dump_json()
# model_dump_json() method se hame pura data json format me mil jata hai including nested models

# we can also control kon kon se field hame export karne hai , using the include and exclude parameters
temp3 = patient1.model_dump(include={'name', 'address'})

# there is also exclude_unset parameter , agar hame sirf wahi fields chahiye jo explicitly set kiye gaye hai to hum ise True kar sakte hai
temp4 = patient1.model_dump(exclude_unset=True)