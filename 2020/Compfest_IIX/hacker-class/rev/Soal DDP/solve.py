enkrip =120290679218832191630163797978118096998325980286646140214484761791004452553
panjang= str(bin(enkrip))[2:]
panjang=len(panjang)/8+1

data=[]
for i in range(panjang)[::-1]:
	temp = enkrip >> (i << 3)
	data.append(temp)
	enkrip = enkrip - (temp << (i << 3))

for i in range(len(data)):
	temp=str(bin(data[i]))[2:].rjust(8,"0")
	temp=temp[4:] + temp[:4]
	data[i]=int(temp,2)

for i in range(len(data)):
	data[i]-=(i + 0b1) if (i & 0o1) else (i | 0x1)

flag=""
for i in data:
	flag += chr(i)

print(flag)
