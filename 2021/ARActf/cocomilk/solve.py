out1 = "[.Q9khIZWkkfG22`a"
out1 = out1[::-1]

real1 = ""

for i in range(0,len(out1)):
    real1 += chr(ord(out1[i]) ^ i)

print (real1)

out2 = "1c:0c:7f:46:77:56:04:34:1e:31:78:07:5b:42:63:1c:29"
out2 = out2.split(":")

# print (out2)

real2=""
for i in range(len(out2)):
    real2 += chr(int(out2[i],16) ^ i ^ ord(real1[i]))

real2 = real2[::-1]

print (real2)

flag = ""
for i in range(len(out1)):
	flag += real1[i] + real2[i]

print (flag)

