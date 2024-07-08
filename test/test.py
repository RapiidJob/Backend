import requests
from getpass import getpass

'''
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMTE2NzkxNywiaWF0IjoxNzIwMzAzOTE3LCJqdGkiOiI4NGQwN2M2YjNlYmE0Mjk1OWU2YzE2MDEzMjk1YWIxYSIsInVzZXJfaWQiOjF9.myCpKRrv-ocJhF3-PkUlPQreDxdE7VMPIpqgDxOur8o",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNTYzMTE3LCJpYXQiOjE3MjAzMDM5MTcsImp0aSI6ImQzMjE0ZThiNjA1ODQwZTFiYTUyYjc4MDg2MDQxNjg1IiwidXNlcl9pZCI6MX0.Qt_2R9OO-Oug-XCdejwoTPJl9J8odHdYW9CFkhuGO68"
}
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMTE2ODI2MSwiaWF0IjoxNzIwMzA0MjYxLCJqdGkiOiI4ZmQyMjc0NmIyMjg0ODVkODUwNGY2YTcwZTQ3NzNmOSIsInVzZXJfaWQiOjJ9.6BRF3adXdUo6eeH9BOeKRr0xQuHk8KgKLen3eSV7wgc",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNTYzNDYxLCJpYXQiOjE3MjAzMDQyNjEsImp0aSI6IjU1NzY4MWE3NzJlZjQyZjE4MmE3NGNmMzFmNjNmMTgzIiwidXNlcl9pZCI6Mn0.sItAViw52F1Kpf93UNCpNIs34Y-u5ctc-6itiMy2sH8"
}
'''
# auth_endpoint = "http://localhost:8000/auth/users/me/"
# email = input("what is your email?\n")

# password = getpass("what is your pass?\n")

# auth_response = requests.post(auth_endpoint, json={"email": email,"password": password})
# print(auth_response.json())
# print(auth_response.status_code)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNTYzNDYxLCJpYXQiOjE3MjAzMDQyNjEsImp0aSI6IjU1NzY4MWE3NzJlZjQyZjE4MmE3NGNmMzFmNjNmMTgzIiwidXNlcl9pZCI6Mn0.sItAViw52F1Kpf93UNCpNIs34Y-u5ctc-6itiMy2sH8"
headers = {
    "Authorization" : f"Bearer {token}"
}

endpoint = "http://localhost:8000/accounts/employer/create/"

get_response = requests.post(endpoint, headers=headers, json={"user": {"email": "sam@gmail.com","phone_number":"0994934835", "password": "123456789_", "gender":"Female","rating":3, "is_identity_verified":True, "address":{"country":"ethiopia", "region":"Oromia"}}}
)
print(get_response.json())
#     data = get_response.json()
#     next_url = data['next']
#     if next_url is not None:
#         print("next url\n")
#         get_response = requests.get(next_url, headers=headers)
#         print(get_response.json())
