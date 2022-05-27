import string
import math

a = string.ascii_letters + string.digits + '}-_+{ '

flag = [250, 238, 6, 102, 39, 227, 26, 102, 173, 214, 102, 27, 6, 95, 241, 102, 246, 41, 250, 250,182]

flag_real=list("COMPFEST12{")
for i in range(len(flag)):
	one=False
	for j in a:
		temp =(math.pow(ord(j),128))%251
		if  temp == flag[i] and one==False:
			flag_real.append(j)
			one=True
		elif temp == flag[i] and one==True:
			print (i+11,j)

flag_real[11]='t'
flag_real[19]='1'
flag_real[24]='r'
flag_real[28]='u'
flag_real[29]='t'
print "".join(flag_real)

# COMPFEST12{tH3_c4T_15_v3rY_Cute}