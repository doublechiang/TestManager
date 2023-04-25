import requests

url = 'http://127.0.0.1:5000/sfhand'
headers = {'Content-Type': 'application/json'}
json = {
    'MBSN': '123456778', 
    'Request': 'UUTConfig2'
}

requests.post(url, headers=headers, json=json)

