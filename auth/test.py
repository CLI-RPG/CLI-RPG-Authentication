import requests, hashlib

# url = 'http://127.0.0.1:5000/login'
# url = 'http://127.0.0.1:8000/auth/register'
url = 'http://127.0.0.1:8000/auth/login'

print(
    requests.post(url, json={
        'username': 'barbie',
        'password': hashlib.sha256('barbie'.encode('utf-8')).hexdigest()
    }).status_code
)