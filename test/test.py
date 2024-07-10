import requests
from getpass import getpass

token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwOTMzMjQxLCJpYXQiOjE3MjA2MzMyNDEsImp0aSI6IjVkOGFmZWQwZjIyMTRmOGNhMzIwOWNjMjlhYmI2MTdiIiwidXNlcl9pZCI6NX0.ZnhlP5kMCEu46KUxylKzYZJGcL3j53etp3Z0frucrhQ"
endpoint = " http://localhost:8000/accounts/worker/create/"
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



