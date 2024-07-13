import requests

token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMjAzNzI5LCJpYXQiOjE3MjA5MDM3MjksImp0aSI6ImQzOTkyOWUxNDRmMjQxMzU5YjFmMmQzMjY4MTgxNjA5IiwidXNlcl9pZCI6MTN9.t4sMB5IQ5yEkJhSGV4V7T7ENpS5CBuDk_VwaC5Iyg1M"
endpoint = "http://localhost:8000/api/accounts/employer/verify/6/"

headers = {
    "Authorization" : f"Bearer {token}"
}   
get_response = requests.post(endpoint, headers=headers)
print(get_response.json())



