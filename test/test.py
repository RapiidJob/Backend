import requests
from getpass import getpass

token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNTQzMDQwLCJpYXQiOjE3MjA1NDEyNDAsImp0aSI6IjFmOTYwN2E2MGVmNjRkNzA4ZWU4M2QyNTM2MDViMGZlIiwidXNlcl9pZCI6MjR9.vEILCtF4uk0mc2-qctbyCbNiF3UhMbFNWEYRd-LAKBA"
endpoint = " http://localhost:8000/accounts/worker/create/"
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
data =  {"email": "123@gmail.com","account_type" : "Worker", "phone_number":"123456789", "password": "123456789_", "gender":"Female", "first_name":"abdu", "middle_name": "hussen", "last_name": "Ali", "user":24}
data.update({
    "birth_date": None,  # Not provided in the data
    "verification_type": None,  # Not provided in the data
    "is_identity_verified": False,  # Default assumption
    "is_email_verified": False,  # Default assumption
    "is_phone_verified": False,  # Default assumption
    "rating": None,  # Not provided in the data
    "created_at": None,  # Not provided in the data
})

files = {
    'profile_image' : open(r"C:/Users/user/Pictures/associative.png", "rb"), # path for picture
    'verification_document' : open(r"C:/Users/user/Pictures/associative.png", "rb") # path for Verification document
}

headers = {
    "Authorization" : f"Bearer {token}"
}

get_response = requests.post(endpoint, headers=headers, data=data, files=files)
print(get_response.json())

get_response = requests.put(endpoint, headers=headers, data=data, files=files)
print(get_response.json())


