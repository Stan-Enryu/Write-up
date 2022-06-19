flag = list('dba26326890556fc59a948495167a374a01e183ae043a4147c7f569a7fb875c0474a90bac51c'.decode("hex"))

test = 'abcdefghijklmnopqrstuvwxyzabcdefghijkl'

enc =list('dcac6125975a03a306a047470b3fad37b5085d2ca453e65e363707c17fb829c51043c8e1cc0d'.decode("hex"))

key = []
for e in range(len(enc)):
	for i in range(255):
		try:
			if ord(enc[e])^i == ord(test[e]):
				key.append(i)
				break
		except:
			continue


# print key
real_flag=''
print len(flag)
print len(key)
for i in range(len(flag)):
	real_flag += chr(ord(flag[i])^key[i])

# for i in range(255):
# 	try:
# 		if ord(flag[0])+i == ord('f'):
# 			print i
# 			break
# 	except:
# 		continue

# for i in range(255):
# 	try:
# 		if ord(enc[0])+i == ord('a'):
# 			print i
# 			break
# 	except:
# 		continue



print real_flag



