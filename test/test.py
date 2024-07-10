import requests
from getpass import getpass

token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNjEyMjQ1LCJpYXQiOjE3MjA2MTA0NDUsImp0aSI6ImMzNDUwOWQ2ZjVlNzQ5MmVhNzU0YzYzYTM1OTI2NjcxIiwidXNlcl9pZCI6Mjh9.SJl3T6oWG9Ui287y1OaUKuxPrueeRK0ErOksw2jo1a8"
endpoint = " http://localhost:8000/accounts/employer/create/"
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

data = {
    "email": "feben@gmail.com",
    "account_type": "Employer",
    "phone_number": "123456789",
    "password": "123456789_",
    "gender": "Female",
    "first_name": "abdu",
    "middle_name": "hussen",
    "last_name": "Ali",
    "address.country": "Ethiopia",
    "address.region": "Addis Ababa",
    "address.city": "Addis Ababa",
    "address.kebele": "01",
    "address.house_number": "123",
    "address.latitude": 9.03,  # Example latitude value
    "address.longitude": 38.74,  # Example longitude value
    "address.is_permanent": True,
    "user": 28,
}

files = {
    'profile_image' : open(r"C:/Users/user/Pictures/search2.png", "rb"), # path for picture
    'verification_document' : open(r"C:/Users/user/Pictures/search1.png", "rb") # path for Verification document
}

headers = {
    "Authorization" : f"Bearer {token}"
}

get_response = requests.post(endpoint, headers=headers, data=data, files=files)
print(get_response.json())


