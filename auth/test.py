import requests, hashlib

# url = 'http://127.0.0.1:5000/login'
url = 'http://127.0.0.1:5000/register'

# Send POST request
print(
    requests.post(url, json={
        'username': 'barbie', 
        'password': hashlib.sha256('barbie2'.encode('utf-8')).hexdigest()
    }).status_code
)