with open("flag.slashroot.old","rb") as f:
    data = f.read()

script = ''
for i in data:
    script += chr((ord(i)-2)^5)

print (script)