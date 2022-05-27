
f=open("pesan","r").readline()

result=f.replace("\\x","")

result = result.decode("hex")
	
print result