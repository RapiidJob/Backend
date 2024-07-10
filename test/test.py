import requests
from getpass import getpass

token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwODk4NTk0LCJpYXQiOjE3MjA1OTg1OTQsImp0aSI6IjZkYWJkMTkzMGFhOTQzMWE4ZDU1N2M5NDE3MTMxYjIzIiwidXNlcl9pZCI6NX0.cQ40DfI6M4HhIdyNMfdN3zYUVBKT3IwfvlWVluWjLvI"
endpoint = " http://localhost:8000/accounts/worker"
default_address = {
    "country": "Ethiopia",
    "region": "Addis Ababa",
    
    "city": "Addis Ababa",
    "kebele": "01",
    "house_number": "123",
    "latitude": 9.03,  # Example latitude value
    "longitude": 38.74,  # Example longitude value
    "is_permanent": True
}
data =  { "phone_number":"123456789", "password": "123456789_", "gender":"Female", "first_name":"abdu", "middle_name": "hussen", "last_name": "Ali", "user":24}
data.update({
    "birth_date": None,  # Not provided in the data
    "verification_type": None,  # Not provided in the data
    "is_identity_verified": False,  # Default assumption
    "is_email_verified": False,  # Default assumption
    "is_phone_verified": False,  # Default assumption
    "rating": 0,  # Not provided in the data
    "created_at": None,  # Not provided in the data
})

files = {
    'profile_image' : open(r"C:/Users/Abdi/Downloads/test.png", "rb"), # path for picture
    'verification_document' : open(r"C:/Users/Abdi/Downloads/test.png", "rb") # path for Verification document
}

headers = {
    "Authorization" : f"Bearer {token}"
}

get_response = requests.post(endpoint, headers=headers, data=data, files=files)
print(get_response.json())

get_response = requests.put(endpoint, headers=headers, data=data, files=files)
print(get_response.json())


