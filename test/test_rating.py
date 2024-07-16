import requests

endpoint = 'http://127:0.0.1/api/accounts/employer/rate/1/'

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMzgxNTE5LCJpYXQiOjE3MjEwODE1MTksImp0aSI6IjNhYjVkOTIwNjRjNDRiZmE5M2UxOThhNDc3ZmMxYTNhIiwidXNlcl9pZCI6MTd9.iZ2VW7DISJvcZXgrgUfEPeeMNAivny4l0KEmz_fmmIY"

headers = {
    "Authorization": f"Bearer {token}"
}
data = {'rating': 5}
get_response = requests.put(endpoint, headers=headers, data=data)

print(get_response.json())