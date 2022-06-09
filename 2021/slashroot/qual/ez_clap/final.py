def check2(a2):
    uVar1 = a2 * 10 & 0xff;
    uVar2 = (uVar1 + 0x539) * 0x10;
    return uVar2 * uVar1 + (uVar1 ^ uVar2 ^ a2) * a2 ;

keys = []

for i in range(1,256):
    keys.append(check2(i))

print keys

from pwn import *
io = process("./chall")
for key in keys:
    sleep(0.1)
    io.sendline(str(key))
    print key 
io.interactive()