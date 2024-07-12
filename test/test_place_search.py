import requests
from getpass import getpass


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwOTQzNDkyLCJpYXQiOjE3MjA2NDM0OTIsImp0aSI6IjE2ZGY5OWQ4MDI4MTQzYzhhNWJkYmJmMjBjMjE0NWY0IiwidXNlcl9pZCI6NX0.QiHMKQkHh83xlluvevBHu7fiU4ULinOfF2VTMP2LNP8"
endpoint = "http://127.0.0.1:8000/api/jobs/search_by_place/"


data = {
    'country': 'Ethiopia',
    'city': 'Adama',
    'region': 'Oromia',
    'category': 'Transport & Delivery',  
    'title':   'Transport & Delivery',
}

headers = {
    "Authorization" : f"Bearer {token}"
}

get_response = requests.post(endpoint, headers=headers, data=data)
print(get_response.json())


