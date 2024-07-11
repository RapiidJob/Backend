import requests
from getpass import getpass

token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMDE1MjgxLCJpYXQiOjE3MjA3MTUyODEsImp0aSI6IjNmYWMxMzVhN2QyNjRhZjM5NmM1NWE5ZmY3ZWFhMTBhIiwidXNlcl9pZCI6M30.q_iGWhHDl5V_DAMU8NE0gGSbMiHukhNUGJkZkqR-9t4"
endpoint = " http://localhost:8000/api/accounts/worker/create/"

data =  {
    "email": "feben@gmail.com",
    "account_type": "Worker",
    "phone_number": "123456789",
    "password": "123456789_",
    "gender": "Female",
    "first_name": "abdu",
    "middle_name": "hussen",
    "last_name": "Ali",
    "country": "Ethiopia",
    "region": "Addis Ababa",
    "city": "Addis Ababa",
    "kebele": "01",
    "house_number": "123",
    "latitude": 9.03,
    "longitude": 38.74,
    "is_permanent": True,
    "user": 5,
}

files = {
    'profile_image' : open(r"C:/Users/user/Pictures/associative.png", "rb"), # path for picture
    'verification_document' : open(r"C:/Users/user/Pictures/associative.png", "rb") # path for Verification document
}

headers = {
    "Authorization" : f"Bearer {token}"
}

get_response = requests.post(endpoint, headers=headers, data=data, files=files)
print(get_response.json())



