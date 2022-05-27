import string 
import base64

def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number,base):
    if number < 0:
        return '-' + str_base(-number, base)
    (d, m) = divmod(number, base)
    if d > 0:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)

def fun_1(b):
	return ''.join([chr((ord(i)-97+1+(1^2))%26+97) for i in b])

njir=string.ascii_lowercase
temp=str_base(16166842727364078278681384436557013,36)

last=""
for la in temp:
	for i,j in zip(njir,fun_1(njir)):
		if j == la:
			last += str(i)
			break

print 'COMPFEST12{' + last + '}'