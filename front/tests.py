import requests
login_url="http://127.0.0.1:8000/login"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
user_info={'username': 'jose2@email.com',
        'password': 'password123'}

response = requests.post(login_url, data=user_info, headers=headers)
token_info = response.json()
print(token_info)