
enc = 'J\x05\x06\x07\x1a\x07a\x03JN]\\Y\x08:0\x0112^l9\t=\r2Y_Z_\t8;Ub\x0c(\x12Tc6;<\x0b\\X\x00\t\x0b\tTN'
enc = list(enc)

print len(enc)

flag = 'J'
for i in range(1,len(enc)):
    temp= chr(ord(enc[i]) ^ ord(enc[i-1]))
    enc[i] = temp
    flag +=temp

print flag
