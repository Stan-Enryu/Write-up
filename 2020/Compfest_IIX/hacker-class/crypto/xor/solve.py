from Crypto.Util.number import long_to_bytes
from pwn import *
import gmpy2

c = "5c50524f595a4c4b2e2d647a5e2a664047704d2c7b407c4d466f2862".decode("hex")

def xor_string (string, key):
	result =""
	for i in string:
		result += chr(ord(i) ^ key)
	return result

# for i in range(0,255):
# 	print i,xor_string(c,i)

print xor_string(c,31)