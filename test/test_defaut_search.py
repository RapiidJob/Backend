import requests
from getpass import getpass

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwOTMzMjQxLCJpYXQiOjE3MjA2MzMyNDEsImp0aSI6IjVkOGFmZWQwZjIyMTRmOGNhMzIwOWNjMjlhYmI2MTdiIiwidXNlcl9pZCI6NX0.ZnhlP5kMCEu46KUxylKzYZJGcL3j53etp3Z0frucrhQ"
endpoint = "http://127.0.0.1:8000/api/jobs/search/"

data = {
    'country': 'Ethiopia',
    'city': 'Addis Ababa',
    'region': 'Addis Ababa',
    'latitude': 9.02045,
    'longitude': 38.75278,
}

headers = {
    "Authorization" : f"Bearer {token}"
}

get_response = requests.post(endpoint, headers=headers, data=data)
print(get_response.json())


