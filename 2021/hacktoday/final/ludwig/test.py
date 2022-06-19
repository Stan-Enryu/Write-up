with open("./bin.lua","r") as f:
	data=f.read().split("\n")

print data[0]
code = ''
with open("./crackme.lua","a") as f:
	for i in data:
		code += i[2:].decode('hex')[::-1]
		
	f.write(code)