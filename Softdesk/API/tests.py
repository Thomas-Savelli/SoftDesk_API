import requests

url = 'http://localhost:8000/api/project/create/'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3MTAzOTY2LCJpYXQiOjE2OTcxMDM2NjYsImp0aSI6IjFmZmViMTU5YTI5YTQ0MmU5YmY4ZjI4MWIxOWY3ZTZlIiwidXNlcl9pZCI6MTF9.EkYCp46T1Gu6zwqbVx7gBrSM1INuB2LdCH4vGQyi930'  # Remplacez par votre token JWT valide
}

data = {
    "name": "Nouveau projet",
    "description": "Description du nouveau projet",
    "type": "back-end"
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())
