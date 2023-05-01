import requests

url = 'http://192.168.204.164:5030/sfhand'
headers = {'Content-Type': 'application/json'}
json_config2 = {
    'FN' : 'B11832476009603A.txt',
    'MBSN': 'B11832476009603A', 
    'Request': 'UUTConfig2',
    'Model' : 'NetApp'
}

json_linkall = {
    'FN' : 'B11832476009603A.txt',
    'MBSN': 'B11832476009603A', 
    'Request': 'Linkall',
    'Model' : 'NetApp'
}


json_status = {
    'FN' : 'B11832476009603A.txt',
    'MBSN': 'B11832476009603A', 
    'Request': 'Status',
    'Model' : 'NetApp',
    'Station' : 'FAT',
    'Status' : 'DMESG check Fail ===T6UA-2U-MILAN FAT test FAIL==='
}

ret = requests.post(url, headers=headers, json=json_config2)
print(ret.status_code)
print(ret.text)
