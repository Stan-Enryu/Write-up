#!/usr/bin/python3
import random as ciwi

p = 101 #redacted
q = 211 # redacted

enc2 = open("enc").readline()

ciwi.seed(q)

enc1 = ""
for i in range(10, len(enc2) + 10):
    i -= 1
    z = p + q - i
    enc1 += chr(ord(enc2[i - 9]) ^ ciwi.randint(i, z))

flag=""
for i in enc1:
	if (ord(i)-1)%5==0:
		flag+=chr(int((ord(i)-1)/5))
	elif (ord(i)-2)%5==0:
		flag+=chr(int((ord(i)-2)/5))
	elif (ord(i)-3)%5==0:
		flag+=chr(int((ord(i)-3)/5))
	elif (ord(i)-4)%5==0:
		flag+=chr(int((ord(i)-4)/5))

print (flag)

