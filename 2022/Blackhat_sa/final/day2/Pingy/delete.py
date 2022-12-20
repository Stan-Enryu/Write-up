import requests

url = 'https://blackhat4-c0e5b86386483f1ae2059909d76cd00c-0.chals.bh.ctf.sa'
uri = '/delete?id='
for i in range(10):
	requests.post(url+uri+str(0))
	print(i)